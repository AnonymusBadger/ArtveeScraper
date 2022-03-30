from src.Terminal import terminal
from src.Text import decorate
import sys


class ProgresBar:
    def __init__(self, text="Progress"):
        self.target = 0
        self.current = 0
        self.text = text

    def setText(self, text):
        self.text = text

    def print(self):
        sys.stdout.write('\033[2K\033[1G')
        if self.target > 0:
            print(f"[ {decorate.decorate(self.text, 'blue', True)} ] [{self.current}/{self.target}]                                  ", end="\r");
        if self.current == self.target:
            print(f"[ {decorate.decorate(self.text, 'blue', True)} ] {decorate.decorate('Done', 'green', True)}                    ")

    def addToTarget(self):
        self.target += 1
        self.print()

    def increment(self):
        self.current += 1
        self.print()


progresBar = ProgresBar()
