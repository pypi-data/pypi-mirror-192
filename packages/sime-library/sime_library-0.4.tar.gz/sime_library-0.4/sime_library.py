import time
from colorama import Fore
import ctypes
import pyshorteners
class Sime_Library(Exception):
    pass
def sleep(time: int):
    try:
        time.sleep(time)
    except:
        raise Sime_Library("ERROR")
def color(color):
    try:
        return Fore.color.upper()
    except:
        raise Sime_Library("Most likely, this color is not supported by the library, or you entered it incorrectly")
def setNameWindow(name: str):
    try:
        ctypes.windll.kernel32.SetConsoleTitleW(f"{name}")
    except:
        raise Sime_Library("ERROR")
def spaces(kolvo: int):
    try:
        for x in range(kolvo):
            print()
    except:
        raise Sime_Library("ERROR")
def shortURL(url: str):
    try:
        s=pyshorteners.Shortener()
        return str(s.tinyurl.short(url))