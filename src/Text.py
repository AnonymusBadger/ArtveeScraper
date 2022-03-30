class Decorator:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

    def decorate(self, text, color="", bold=False, underline=False):
        if color == "purple":
            color = self.PURPLE
        elif color == "cyan":
            color = self.CYAN
        elif color == "darkCyan":
            color = self.DARKCYAN
        elif color == "blue":
            color = self.BLUE
        elif color == "green":
            color = self.GREEN
        elif color == "yellow":
            color = self.YELLOW
        elif color == "red":
            color = self.RED
        else:
            raise ValueError(f"Invalid color: { color }")

        if bold:
            bold = self.BOLD
        else:
            bold = ""

        if underline:
            underline = self.UNDERLINE
        else:
            underline = ""

        return f"{color}{bold}{underline}{text}{self.END}"


    def warning(self, text):
        return f"{self.RED}{self.BOLD}{text}{self.END}"

    def alert(self, text):
        return f"{self.YELLOW}{self.BOLD}{text}{self.END}"

    def info(self, text):
        return f"{self.DARKCYAN}{self.BOLD}{text}{self.END}"

    def bold(self, text):
        return f"{self.BOLD}{text}{self.END}"

decorate = Decorator();
