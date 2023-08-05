import asyncio
import sys
import threading
from queue import Queue
from typing import AsyncIterator, Iterator

__version__ = "0.1.0"


class Clipstream:
    @staticmethod
    def _get_stream() -> AsyncIterator[str]:

        # Try to use the XFixes extension to get clipboard events
        # in a more efficient way than process polling
        try:
            from .with_xfixes import xfixes_clipboard_stream, check_xfixes_supported

            stream = xfixes_clipboard_stream()
            if not check_xfixes_supported():
                raise RuntimeError("XFixes not supported")

            print("Using XFixes extension for clipboard monitoring.", file=sys.stderr)
            return aiter(stream)

        # Fall back to polling if xfixes is not supported
        except (ImportError, RuntimeError):
            from .stream import clipboard_stream

            print("Using polling for clipboard monitoring.", file=sys.stderr)
            return clipboard_stream()

    def __aiter__(self) -> AsyncIterator[str]:
        """Asynchronously iterate over the clipboard stream."""
        return self._get_stream()

    def __iter__(self) -> Iterator[str]:
        """Synchronously iterate over the clipboard stream.

        Does some magic to make __aiter__ work in a thread.
        """
        queue = Queue()

        def _sync_iterator():
            while True:
                yield queue.get()

        async def _async_iterator():
            async for item in self._get_stream():
                queue.put(item)

        thread = threading.Thread(target=asyncio.run, args=(_async_iterator(),))
        thread.start()

        return _sync_iterator()


clipstream = Clipstream()
