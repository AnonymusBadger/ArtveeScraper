import sys
import requests
from src.Text import decorate
from src.UserInput import userInput
from src.FileSystem import filesystem
from src.Terminal import terminal
from urllib.parse import quote_plus
import pathlib
import platform
import configparser

def isFrozen():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return True
    else:
        return False

class Config:
    def __init__(self):
        self.osType = platform.system()
        self.homePath = str(pathlib.Path().home())
        self.saveConfDir = self.getSaveConfDir()
        self.configparser = configparser.ConfigParser()
        self.confFile = "artvee.ini"
        self.confFilePath = None
        self.checkConfFileExists()

    def getSaveConfDir(self):
        if self.osType == "Darwin":
            return f"{self.homePath}/Library/Preferences/artvee/"
        elif self.osType == "Linux":
            return f"{self.homePath}/.config/artvee/"

    def checkConfDirExists(self):
        exists = filesystem.exists(self.saveConfDir)
        if not exists:
            filesystem.mkdir(self.saveConfDir)

    def checkConfFileExists(self):
        self.confFilePath = self.saveConfDir + self.confFile
        exists = filesystem.exists(self.confFilePath)
        if exists:
            self.readConfig()
        else:
            self.checkConfDirExists()
            self.createConfFile()

    def createConfFile(self):
        config = self.configparser

        config['BASIC'] = {
            "SavePath": "None"
        }

        with open(self.confFilePath, "w") as configfile:
            config.write(configfile)

    def readConfig(self):
        config = self.configparser
        config.read(self.confFilePath)
        savePath = config['BASIC']['SavePath']
        if savePath == "None":
            savePath = None
        scraperConfig.savePath = savePath

    def writePath(self, savePath):
        config = self.configparser

        config['BASIC'] = {
            "SavePath": str(savePath)
        }

        with open(self.confFilePath, "w") as configfile:
            config.write(configfile)


class ScraperConfig:
    def __init__(self):
        self.searchQuery = None
        self.savePath = None
        self.newDir = None
        self.newDirPath = None

    def serializeQuery(self):
        return quote_plus(self.searchQuery)

    def setSavePath(self):
        path = userInput.query_folder()
        if path != None:
            self.savePath = path
            config.writePath(path)
        if self.newDirPath != None:
            self.setNewDir(self.searchQuery)

    def setSearchQuery(self):
        terminal.printDecorator(True)
        query = userInput.query_text("Query (E.g. Mondrian): ")

        if query:
            self.searchQuery = query
            self.setNewDir(query)

    def setNewDir(self, dirName):
        terminal.printDecorator(True)
        terminal.info("Creating save directry")

        newDirPath = f"{self.savePath}/{dirName}"
        exists = filesystem.exists(newDirPath)
        if exists:
            terminal.warning(f"{decorate.bold('Path')}: { newDirPath }");
            resp = userInput.query_yes_no(
                "Alerady exists! Do you want to override?", "no"
            )
            if resp:
                self.newDir = dirName
                self.newDirPath = newDirPath
            else:
                createUnique = userInput.query_yes_no(
                    "Create new unique direcotry for this search?", "yes"
                )
                if createUnique:
                    newDirPath, newDir = filesystem.createUniquePath(newDirPath)
                    self.newDir = newDir
                    self.newDirPath = newDirPath
                else:
                    self.searchQuery = None
                    self.newDir = None
                    self.newDirPath = None
        else:
            self.newDir = dirName
            self.newDirPath = newDirPath

    def getDataAsString(self):
        return {
            "savePath": f"{decorate.bold('Save at')}: {self.savePath}",
            "searchQuery": f"{decorate.bold('Search for')}: {self.searchQuery}",
            "newDir": f"{decorate.bold('New folder')}: {self.newDir}",
        }


def init():
    global isExe
    isExe = isFrozen()
    global scraperConfig
    scraperConfig = ScraperConfig()
    global config
    config = Config()
