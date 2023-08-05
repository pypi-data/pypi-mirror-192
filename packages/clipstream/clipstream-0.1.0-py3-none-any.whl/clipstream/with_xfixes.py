import asyncio
from typing import AsyncIterator, Iterator, Literal

import pyperclip
from asynkets import PeriodicPulse

from Xlib.ext.randr import BadRRCrtcError
from Xlib import X
from Xlib.display import Display
from Xlib.ext import xfixes
from Xlib.error import DisplayNameError


async def xfixes_clipboard_stream(
    yield_initial: bool = False,
    selection: Literal["PRIMARY", "SECONDARY", "CLIPBOARD"] = "CLIPBOARD",
) -> AsyncIterator[str]:

    display = Display()

    sel_name = selection
    sel_atom = display.get_atom(sel_name)

    if not display.has_extension("XFIXES"):
        if display.query_extension("XFIXES") is None:
            raise RuntimeError(
                "The display does not support the XFIXES extension, "
                "required for lightweight selection monitoring."
            )

    display.xfixes_query_version()

    screen = display.screen()
    mask = (
        xfixes.XFixesSetSelectionOwnerNotifyMask
        | xfixes.XFixesSelectionWindowDestroyNotifyMask
        | xfixes.XFixesSelectionClientCloseNotifyMask
    )
    display.xfixes_select_selection_input(screen.root, sel_atom, mask)

    if yield_initial:
        yield pyperclip.paste()

    # Poll on a 0.01s period with display.pending_events.
    # The alternative is to call the blocking display.next_event
    # directly, but since it's not guaranteed to unblock in any
    # amount of time, it becomes impossible to stop the function
    # even if it's run on a thread, as Python has no way of forcibly
    # killing threads. Still, polling here with the asyncio event
    # loop is much cheaper than polling by creating a process on
    # each check, so this is quite preferable.
    timer = PeriodicPulse(period=0.01)
    async for _ in timer:
        for _ in range(display.pending_events()):
            e = display.next_event()
            w = e.window
            d = w.display
            data_atom = d.get_atom("SEL_DATA")
            target_atom = d.get_atom("TARGETS")
            w.convert_selection(sel_atom, target_atom, data_atom, X.CurrentTime)

            if (e.type, e.sub_code) == display.extension_event.SetSelectionOwnerNotify:
                yield pyperclip.paste()


def check_xfixes_supported() -> bool:
    """Check if the XFixes extension is supported."""
    try:
        display = Display()
    except DisplayNameError:
        return False
    if not display.has_extension("XFIXES"):
        if display.query_extension("XFIXES") is None:
            return False
    try:
        display.xfixes_query_version()
    except:
        return False
    return True


if __name__ == "__main__":

    async def main() -> None:
        async for item in xfixes_clipboard_stream():
            print(f"Got {item!r}")

    asyncio.run(main(), debug=True)
