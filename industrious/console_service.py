import asyncio, sys, logging

from functools import wraps
from concurrent.futures import ThreadPoolExecutor

from rich.console import Console
from rich.table import Table
from rich.markup import escape

class ConsoleService:
    """
    :credits:
    https://github.com/aiortc/aiortc/issues/774#issuecomment-1325092053 - pointed towards a better read functionality, another github/stackoverflow W
    https://stackoverflow.com/questions/31510190/aysncio-cannot-read-stdin-on-windows/36785819#36785819 - the above forementioned stackoverflow post
    """

    def __init__(self):
        self.running = False
        self.console = Console()
        self.prompt = "Console» "
        self.commands = {
            "help": {
                "name": "help",
                "description": "Help Command",
                "aliases": ["?", "help"],
                "usage": "[command]",
                "func": self.help_command
            },

            "exit": {
                "name": "exit",
                "description": "Exit Command",
                "aliases": ["exit"],
                "usage": "",
                "func": self.exit_command
            }
        }

    async def exit_command(self, command):
        self.running = False
        self.console.log(f"Stopping {__name__}, requested by user")


    async def help_command(self, command):
        _help_table = Table(title="Command Help")
        _help_table.add_column("name")
        _help_table.add_column("description")
        _help_table.add_column("aliases")
        _help_table.add_column("usage")
        _help_table.add_column("func")

        for name, cmd in self.commands.items():
            if len(command) == 1 or any(alias.startswith(command[1]) for alias in cmd["aliases"]):
                _help_table.add_row(cmd["name"], cmd["description"], ", ".join(cmd["aliases"]), 'None' if "usage" not in cmd or cmd["usage"] == None else escape(cmd["usage"]), cmd["func"].__name__)

        self.console.print(_help_table)


    def add_command(self, name: str, description: str, func, aliases: list | None = None, usage: str | None = None):
        ## check if the command already exists
        if name in self.commands:
            self.console.log(f"[ConsoleService] Failed to register command {name} as it already exists!")
            return

        ## fix aliases
        new_aliases = []

        if aliases:
            for alias in aliases:
                new_aliases.append(alias.lower())
        new_aliases.append(name.lower())
        aliases = new_aliases

        ## add our command to our command table
        self.commands[name] = {
            "name": name,
            "description": description,
            "aliases": aliases,
            "usage": usage or "",
            "func": func
        }

    def command(self, name: str, description: str, aliases: list | None = None, usage: str | None = None):
        new_aliases = []

        if aliases:
            for alias in aliases:
                new_aliases.append(alias.lower())

        new_aliases.append(name.lower())
        aliases = new_aliases

        def decorator(func):
            ## check if our command already exists
            if name in self.commands:
                self.console.log(f"[ConsoleService] Failed to register command {name} as it already exists!",)
                return

            ## add our command to our command table
            self.commands[name] = {
                "name": name,
                "description": description,
                "aliases": aliases,
                "usage": usage,
                "func": func
            }

            @wraps(func)
            def wrapper(*args, **kwargs):
                ## TODO: pre_execution command stuff

                ## execute our function
                a = func(*args, **kwargs)

                ## TODO: post_execution command stuff
                return a

            return wrapper
        return decorator

    async def start(self):
        self.running = True
        loop = asyncio.get_event_loop()
        while self.running:
            try:
                data = await loop.run_in_executor(None, self.console.input, self.prompt)

                if not data:
                    continue

                split = data.rstrip("\n").split(" ", 1)

                if not split[0]:
                    continue

                cmd_found = False
                for name, cmd in self.commands.items():
                    if split[0].lower() in cmd["aliases"]:
                        await cmd["func"](split)
                        cmd_found = True
                        break

                if not cmd_found:
                    self.console.log(f"[Console] unknown command {split[0]}")
            except asyncio.CancelledError:
                self.console.log("user exited.")
                break
            except Exception as e:
                self.console.print_exception()