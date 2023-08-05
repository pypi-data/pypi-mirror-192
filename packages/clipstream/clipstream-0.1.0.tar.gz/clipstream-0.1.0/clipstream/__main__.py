import argparse
import shlex
import textwrap
import asyncio
import os
import signal
import sys
import typing

import clipstream
from clipstream.stream import clipboard_stream

try:
    from clipstream.with_xfixes import xfixes_clipboard_stream, check_xfixes_supported
except ImportError:
    xfixes_clipboard_stream = None
    check_xfixes_supported = lambda: False  # noqa


def clipstream_to_stdout() -> None:
    parser = argparse.ArgumentParser(
        prog="clipstream",
        description="Write clipboard contents to stdout as they change.",
        epilog="If the XFIXES extension is available, this will be used to "
        "monitor the clipboard. Otherwise, a polling method will be used.",
    )
    parser.add_argument(
        "-n",
        "--newline",
        action=argparse.BooleanOptionalAction,
        help="Print a newline after each clipboard item.",
        default=True,
    )
    parser.add_argument(
        "-1",
        "--one",
        action=argparse.BooleanOptionalAction,
        help="Print one clipboard item, then exit.",
        default=False,
    )
    parser.add_argument(
        "-i",
        "--include-initial",
        action=argparse.BooleanOptionalAction,
        help="Include the initial clipboard item.",
        default=False,
    )
    parser.add_argument(
        "-s",
        "--strip",
        action=argparse.BooleanOptionalAction,
        help="Strip whitespace from clipboard items.",
        default=False,
    )
    parser.add_argument(
        "-r",
        "--polling-rate",
        type=float,
        default=2,
        help=(
            "How often to poll the clipboard, in Hz (times per second). "
            "Not used when XFixes is available (reacts instantly)."
        ),
    )
    parser.add_argument(
        "-0",
        "--null",
        action=argparse.BooleanOptionalAction,
        help="Print a null byte after each clipboard item.",
        default=False,
    )
    parser.add_argument(
        "-u",
        "--unique",
        action=argparse.BooleanOptionalAction,
        help="Only print unique clipboard items.",
        default=False,
    )
    parser.add_argument(
        "-x",
        "--execute",
        help=textwrap.dedent(
            """
            Execute a command with the clipboard contents.
            If `{}` is present (or another symbol specified by -I is), it will be replaced 
            with the contents of the clipboard when running the command. Otherwise, the command
            will be executed with the clipboard contents as the last argument.
            """
        ),
        nargs="+",
        action="append"
    )
    parser.add_argument(
        "-I",
        "--input-symbol",
        help="The symbol to replace with the clipboard contents when using -x.",
        default="{}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print commands executed when running with -x.",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        help="Print the command that would be executed, but don't execute it.",
        default=False,
    )
    parser.add_argument(
        "-S",
        "--shell",
        action=argparse.BooleanOptionalAction,
        help="Execute the command in a shell.",
        default=False,
    )
    parser.add_argument(
        "-j",
        "--max-concurrent-procs",
        type=int,
        help="The maximum number of processes to run in parallel for execute mode.",
        default=0,
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s {}".format(clipstream.__version__),
    )

    args = parser.parse_args()

    # def stop() -> None:
    # Commit seppuku by sending SIGTERM to self on SIGINT (i.e. Ctrl + C)
    # This is a pretty heavy-handed way to do it; properly close everything: Soon™
    # os.kill(os.getpid(), signal.SIGTERM)

    execute_only_args = (
        "execute",
        "shell",
        "dry_run",
        "verbose",
        "input_symbol",
        "max_concurrent_procs",
    )

    if args.execute:
        fn = execute_commands
    else:
        for arg in execute_only_args:
            delattr(args, arg)
        fn = write_stream

    loop = asyncio.get_event_loop()
    task = loop.create_task(fn(**vars(args)))
    loop.add_signal_handler(signal.SIGINT, task.cancel)

    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass


async def write_stream(
    newline: bool = True,
    one: bool = False,
    include_initial: bool = False,
    strip: bool = False,
    polling_rate: float = 2,
    null: bool = False,
    unique: bool = False,
) -> None:
    """Write clipboard items to stdout as they come in."""

    unique_seen = set()

    if check_xfixes_supported():
        stream = xfixes_clipboard_stream(include_initial)
    else:
        stream = clipboard_stream(include_initial, polling_rate)

    def write(it: str) -> None:

        if strip:
            it = it.strip()
        if newline:
            it += "\n"
        if null:
            it += "\0"

        if unique:
            if hash(it) in unique_seen:
                return
            unique_seen.add(hash(it))

        try:
            sys.stdout.write(it)
            sys.stdout.flush()
        except BrokenPipeError:
            exit(0)

    if one:
        if include_initial:
            write(await anext(stream))
        write(await anext(stream))
        return

    async for item in stream:
        write(item)


async def execute_commands(
    newline: bool = True,
    one: bool = False,
    include_initial: bool = False,
    strip: bool = False,
    polling_rate: float = 2,
    unique: bool = False,
    null: bool = False,
    execute: list[str] | None = None,
    input_symbol: str = "{}",
    verbose: bool = False,
    dry_run: bool = False,
    shell: bool = False,
    max_concurrent_procs: int = 0,
) -> None:
    """Continuously monitor the clipboard, and run a command with contents when it changes."""
    unique_seen = set()
    execute_cmds = execute or []
    if max_concurrent_procs:
        semaphore = asyncio.Semaphore(max_concurrent_procs)
    else:
        semaphore = None

    if check_xfixes_supported():
        stream = xfixes_clipboard_stream(include_initial)
    else:
        stream = clipboard_stream(include_initial, polling_rate)

    def do_exec(it: str) -> None:

        if strip:
            it = it.strip()

        if unique:
            if hash(it) in unique_seen:
                return
            unique_seen.add(hash(it))

        try:
            # Prepare the command to run in exec mode
            cmds = []
            if shell:
                it = shlex.quote(it)

            # Substitute the input symbol with the clipboard contents
            substituted = False
            print(execute_cmds)
            for cmd in execute_cmds:
                new_cmd = cmd.replace(input_symbol, it)
                if new_cmd != cmd:
                    substituted = True
                cmds.append(new_cmd)

            # If no substitution was made, add the clipboard contents as the last argument
            if not substituted:
                cmds.append(it)

            # Print the command that would be run
            if verbose or dry_run:
                sys.stdout.write(shlex.join(cmds) + "\n")
                sys.stdout.flush()

            # Run the command
            if not dry_run:
                asyncio.create_task(run_command(cmds, shell, semaphore))

        except BrokenPipeError:
            exit(0)

    if one:
        if include_initial:
            do_exec(await anext(stream))
        do_exec(await anext(stream))
        return

    async for item in stream:
        do_exec(item)


async def run_command(
    cmds: typing.List[str], shell: bool, semaphore: asyncio.Semaphore | None
) -> None:
    if semaphore is not None:
        await semaphore.acquire()
    try:
        if shell:
            cmd_str = cmds[0]
            proc = await asyncio.create_subprocess_shell(cmd_str)
        else:
            proc = await asyncio.create_subprocess_exec(*cmds)
        await proc.wait()
    finally:
        if semaphore is not None:
            semaphore.release()

if __name__ == "__main__":
    clipstream_to_stdout()
