import threading
import time
import pyperclip


class ClipboardWatcher(threading.Thread):
    def __init__(self, callback, pause=0.1):
        """
        Watches the clipboard for changes.

        :param callback: function that will be called with the new clipboard text.
        :param pause: delay between checks (seconds)
        """
        super().__init__()
        self.callback = callback
        self.pause = pause
        self._running = True
        try:
            self._last_clipboard = pyperclip.paste()
        except Exception:
            self._last_clipboard = ""
        self.daemon = True  # lets it run in background

    def run(self):
        while self._running:
            try:
                current = pyperclip.paste()
                if current != self._last_clipboard:
                    self._last_clipboard = current
                    self.callback(current)
            except Exception as e:
                print(f"Error: {e}")

            time.sleep(self.pause)

    def stop(self):
        self._running = False
