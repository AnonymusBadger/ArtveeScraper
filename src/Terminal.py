import os
from src.Text import decorate

class Terminal:
    def __init__(self):
        self._width = 0
        self.setWidth()

    def setWidth(self):
        _, width = os.popen("stty size", "r").read().split()
        self._width = int(width)

    def getWidth(self):
        return self._width

    def printDecorator(self, new_line=False):
        self.setWidth()
        if new_line:
            print()
        print("".join(["=" for _ in range(self._width)]))

    def print(self, text, new_line=False):
        if new_line:
            text = f"\n{text}"
        print(text)

    def clear(self):
        os.system("clear")

    def warning(self, text, new_line=False):
        warning = f"[ {decorate.warning('WARNING')} ]"
        self.print(f"{warning} {text}", new_line)

    def alert(self, text, new_line=False):
        alert = f"[ {decorate.alert('ALERT')} ]"
        self.print(f"{alert} {text}", new_line)

    def info(self, text, new_line=False):
        alert = f"[ {decorate.info('INFO')} ]"
        self.print(f"{alert} {text}", new_line)

terminal = Terminal();
