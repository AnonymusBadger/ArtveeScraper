import os
import sys
import app
import pathlib
import shutil
from src.UserInput import UserInput
from src.Terminal import terminal
from src.Text import decorate

class FileSystem:
    def __init__(self):
        self.input = UserInput()

    def getExecDir(self):
        if app.isExe:
            path = os.path.dirname(os.path.abspath(sys.executable))
        else:
            path = os.getcwd()
        return path

    def override(self, path, force=False):
        if force:
            self.rmDir(path)
            self.mkdir(path)
            return True

        if pathlib.Path(path).is_dir():
            terminal.warning(f"{decorate.bold('Path')}: { path }");
            resp = self.input.query_yes_no(
                "Alerady exists! Do you want to override?", "no"
            )
            if resp:
                self.rmDir(path)
                self.mkdir(path)
                return True
            else:
                return False

    def mkdir(self, path, force=False):
        try:
            pathlib.Path(path).mkdir(parents=True)
            return True
        except FileExistsError as exc:
            return self.override(path, force=force)

    def rmDir(self, path):
        shutil.rmtree(path)

    def exists(self, path):
        return pathlib.Path(path).exists()

    def createUniquePath(self, path, count=0):
        if count > 0:
            newPath = f"{path}({count})"
        else:
            newPath = path

        if not self.exists(newPath):
            return newPath, pathlib.Path(newPath).name
        else:
            return self.createUniquePath(path, count + 1)

filesystem = FileSystem()
