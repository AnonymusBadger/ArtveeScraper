import sys
import easygui
from src.Terminal import terminal


class UserInput:
    def query_yes_no(self, question, default="yes"):
        valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == "":
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write(
                    "Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n"
                )

    def query_choice(self, choices):
        while True:
            valid = [key for key in choices if choices[key]['isShown']]

            print()
            print(
                *[
                    f"[{key}] {choices[key]['text']} "
                    for key in choices
                    if choices[key]["isShown"]
                ]
            )

            choice = input("Select: ")
            try:
                choice = int(choice)
            except ValueError:
                terminal.printDecorator(True)
                terminal.alert(f"Invalid choice \"{choice}\"", True)
                continue

            if choice in valid:
                return choice
            else:
                terminal.printDecorator(True)
                terminal.alert(f"Invalid choice {choice}", True)

    def query_folder(self):
        return easygui.diropenbox()

    def query_text(self, text):
        resp = input(text)
        if resp:
            return resp
        else:
            return False


userInput = UserInput()
