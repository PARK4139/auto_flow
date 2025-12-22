
import ctypes
import threading
import time
from ctypes import wintypes

import win32con
import win32gui

# WinEventProc callback function type
WINEVENTPROC = ctypes.WINFUNCTYPE(
    None,
    wintypes.HANDLE,
    wintypes.DWORD,
    wintypes.HWND,
    wintypes.LONG,
    wintypes.LONG,
    wintypes.DWORD,
    wintypes.DWORD,
)

class WindowMonitor:
    def __init__(self):
        self.hook = None
        self.thread = None
        self.running = False
        self.window_titles = {}  # Using a dict for faster lookup and updates {hwnd: title}
        self._lock = threading.Lock()
        self._wineventproc_callback = WINEVENTPROC(self._event_callback)

    def _event_callback(self, hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
        if not hwnd or idObject != win32con.OBJID_WINDOW or idChild != 0:
            return

        try:
            title = win32gui.GetWindowText(hwnd)
            if not title:
                # If window is destroyed, it might not have a title anymore
                with self._lock:
                    if hwnd in self.window_titles:
                        del self.window_titles[hwnd]
                return

            with self._lock:
                if event == win32con.EVENT_OBJECT_CREATE or event == win32con.EVENT_OBJECT_NAMECHANGE:
                    self.window_titles[hwnd] = title
                elif event == win32con.EVENT_OBJECT_DESTROY:
                    if hwnd in self.window_titles:
                        del self.window_titles[hwnd]
        except Exception as e:
            # This can happen if the window is destroyed between calls
            with self._lock:
                if hwnd in self.window_titles:
                    del self.window_titles[hwnd]

    def _monitor(self):
        self.hook = ctypes.windll.user32.SetWinEventHook(
            win32con.EVENT_OBJECT_CREATE,
            win32con.EVENT_OBJECT_DESTROY,
            0,
            self._wineventproc_callback,
            0,
            0,
            win32con.WINEVENT_OUTOFCONTEXT,
        )
        
        # Also hook name changes
        self.name_change_hook = ctypes.windll.user32.SetWinEventHook(
            win32con.EVENT_OBJECT_NAMECHANGE,
            win32con.EVENT_OBJECT_NAMECHANGE,
            0,
            self._wineventproc_callback,
            0,
            0,
            win32con.WINEVENT_OUTOFCONTEXT,
        )

        self.running = True
        win32gui.PumpMessages()

    def start(self):
        if self.running:
            return
        
        # Initial population
        def _enum_windows_callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    self.window_titles[hwnd] = title
        win32gui.EnumWindows(_enum_windows_callback, None)

        self.thread = threading.Thread(target=self._monitor, daemon=True)
        self.thread.start()
        # Give it a moment to start up
        time.sleep(0.1)

    def stop(self):
        if not self.running:
            return
        if self.hook:
            ctypes.windll.user32.UnhookWinEvent(self.hook)
            self.hook = None
        if self.name_change_hook:
            ctypes.windll.user32.UnhookWinEvent(self.name_change_hook)
            self.name_change_hook = None
        
        # To stop PumpMessages, we need to post a quit message to the thread
        ctypes.windll.user32.PostThreadMessageW(self.thread.ident, win32con.WM_QUIT, 0, 0)
        self.running = False

    def get_titles(self) -> list[str]:
        with self._lock:
            return list(self.window_titles.values())

# Singleton instance
_window_monitor_instance = None
_window_monitor_lock = threading.Lock()

def get_window_monitor():
    """Returns a singleton instance of the WindowMonitor."""
    global _window_monitor_instance
    with _window_monitor_lock:
        if _window_monitor_instance is None:
            _window_monitor_instance = WindowMonitor()
            _window_monitor_instance.start()
    return _window_monitor_instance

if __name__ == '__main__':
    # Example usage and test
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    logging.info("Starting window monitor...")
    monitor = get_window_monitor()

    try:
        for i in range(20):
            time.sleep(1)
            titles = monitor.get_titles()
            logging.info(f"Currently open windows ({len(titles)}): {titles[:5]}") # Print first 5
    except KeyboardInterrupt:
        logging.info("Stopping window monitor...")
    finally:
        monitor.stop()
        logging.info("Monitor stopped.")

