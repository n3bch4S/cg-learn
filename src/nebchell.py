from typing import Callable

DEFAULT_SHELL_NAME = "n3bch4LL"
DEFAULT_SHELL_QUITS = ["quit", "exit", "\\q"]


class Nebchell:
    """Quick Setup
    \nsh = Nebchell()
    \nfns = {
    \n  "help": sh.showHelp,
    \n  "": sh.dummy,
    \n  ...
    \n }
    \nhlps = {
    \n  "print": "print [text]",
    \n  ...
    \n}
    \nsh.functions = fns
    \nsh.helps = hlps
    \nsh.startShell()
    """

    def __init__(
        self,
        name: str = DEFAULT_SHELL_NAME,
        functions: dict[str, Callable] = {},
        helps: dict[str, str] = {},
        quits: list[str] = DEFAULT_SHELL_QUITS,
    ):
        self.name = name
        self.functions = functions
        self.helps = helps
        self.quits = quits

    def dummy(self):
        pass

    def extractPrompt(self, prompt: str) -> tuple[str, list]:
        """Extracts the command and arguments from a given input string"""
        args = prompt.split()
        if len(args) == 0:
            return "", []
        cmdName = args.pop(0)
        return (cmdName, args)

    def runCommand(self, cmdName: str, args: list) -> None:
        """Runs the specified command with the provided arguments"""
        func = self.functions[cmdName]
        func(*args)

    def showHelp(self, cmdName: str = "") -> None:
        """Shows help on either all topics or just one specific topic"""
        if len(cmdName) == 0:
            # Show general help
            for cmd in self.helps:
                print("-> " + self.helps[cmd])
            print(f"-> {self.quits}")
        elif cmdName in self.helps:
            # Show detailed help on one topic
            print("-> " + self.helps[cmdName])
        else:
            # cmd not found
            print(f"-> '{cmdName}' not found")

    def startShell(self) -> None:
        """Starts an interactive shell session"""
        prompt = input(
            f"\nRunning nebchell...\ntype 'help' for commands usage\n{self.name} > "
        )
        cmdName, args = self.extractPrompt(prompt)
        while cmdName not in self.quits:
            try:
                self.runCommand(cmdName, args)
            except KeyError:
                print(f"-> '{cmdName}' not found in {self.name}")
            except TypeError:
                self.showHelp(cmdName)
            prompt = input(f"{self.name} > ")
            cmdName, args = self.extractPrompt(prompt)
        print(f"-> bye.\n")
