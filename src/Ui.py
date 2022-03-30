from src.Terminal import terminal
from src.UserInput import userInput
from src.runScrapy import crawler

import sys
import app


class MainWindow:
    def __init__(self, ui):
        self.ui = ui
        self.body = self.getBody()
        self.choices = {
            1: {
                "text": "Set save directory",
                "onChoice": self.setSavePath,
                "isShown": True,
            },
            2: {
                "text": "Search for",
                "onChoice": self.setQuery,
                "isShown": True if app.scraperConfig.savePath != None else False,
            },
            3: {"text": "Run", "onChoice": self.runSpider, "isShown": False},
            0: {"text": "Exit", "onChoice": (lambda: sys.exit()), "isShown": True},
        }

    def setSavePath(self):
        app.scraperConfig.setSavePath()
        self.body = self.getBody()
        if app.scraperConfig.savePath != None:
            self.choices[2]["isShown"] = True

    def setQuery(self):
        app.scraperConfig.setSearchQuery()
        self.body = self.getBody()
        if app.scraperConfig.searchQuery != None:
            self.choices[3]["isShown"] = True
            self.runSpider()
        else:
            self.choices[3]["isShown"] = False

    def runSpider(self):
        try:
            crawler.run()
        except ValueError:
            resp = userInput.query_yes_no("Change query?")
            if resp:
                self.setQuery()
                if not app.scraperConfig.searchQuery == None:
                    self.runSpider()
                else:
                    return
            else:
                return

    def getBody(self):
        data = app.scraperConfig.getDataAsString()
        return "\n".join([data[key] for key in data])

    def show(self):
        while True:
            terminal.clear()
            terminal.printDecorator()
            terminal.print(self.body, True)
            terminal.printDecorator(True)
            choice = userInput.query_choice(self.choices)
            self.handleChoice(choice)

    def handleChoice(self, choice):
        self.choices[choice]["onChoice"]()


class Ui:
    def __init__(self):
        self.window = MainWindow(self)
        self.start()

    def start(self):
        self.window.show()
