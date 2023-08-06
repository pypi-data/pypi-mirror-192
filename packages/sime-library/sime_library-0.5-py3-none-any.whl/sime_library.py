import time
from colorama import Fore
import ctypes
import pyshorteners


class SimeLibraryError(Exception):
    pass


def sleep(t: float) -> None:
    try:
        time.sleep(t)
    except Exception:
        raise SimeLibraryError("Error occurred during sleep")


def color(color_name: str) -> str:
    try:
        return getattr(Fore, color_name.upper())
    except AttributeError:
        raise SimeLibraryError(f"{color_name} is not a valid color name")


def set_window_title(title: str) -> None:
    try:
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    except Exception:
        raise SimeLibraryError("Error occurred during setting window title")


def spaces(n: int) -> None:
    try:
        for i in range(n):
            print()
    except Exception:
        raise SimeLibraryError("Error occurred during adding spaces")


def shorten_url(url: str) -> str:
    try:
        s = pyshorteners.Shortener()
        return str(s.tinyurl.short(url))
    except Exception:
        raise SimeLibraryError("Error occurred during shortening URL")
