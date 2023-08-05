import asyncio
from typing import AsyncIterator

import pyperclip
from asynkets import PeriodicPulse


async def clipboard_stream(
    yield_initial: bool = False,
    polling_rate: float = 2,
) -> AsyncIterator[str]:
    if polling_rate <= 0:
        raise ValueError("Polling rate must be positive.")
    timer = PeriodicPulse(period=1 / polling_rate)

    if yield_initial:
        prev_clipboard_contents = None
    else:
        prev_clipboard_contents = pyperclip.paste()

    async for _ in timer:
        clipbpoard_contents = pyperclip.paste()
        if clipbpoard_contents == prev_clipboard_contents:
            continue

        yield clipbpoard_contents
        prev_clipboard_contents = clipbpoard_contents


if __name__ == "__main__":

    async def main() -> None:
        async for update in clipboard_stream():
            print(update)

    asyncio.run(main())
