import asyncio, sys, logging

from functools import wraps
from concurrent.futures import ThreadPoolExecutor

from rich import inspect
from rich.console import Console
from rich.table import Table
from rich.markup import escape

from typing import Any, Optional

class ConsoleService:
    """
    :credits:
    https://github.com/aiortc/aiortc/issues/774#issuecomment-1325092053 - pointed towards a better read functionality, another github/stackoverflow W
    https://stackoverflow.com/questions/31510190/aysncio-cannot-read-stdin-on-windows/36785819#36785819 - the above forementioned stackoverflow post
    """

    def __init__(self, *args, **kwargs):
        """
            An command driven input reader for console

            :param prompt: an input prompt
            :type prompt: str

            :param disable_unsafe_commands: disables commands like eval and exec
            :type disable_unsafe_commands: bool

            :param gbls: a set of globals used for things like the eval and exec commands
            :type gbls: dict[str, Any]

            :param lcls: a set of locals used for things like the eval and exec commands
            :type lcls: dict[str, Any]

            ## Example
            ```python
                ## rawdog it
                cs = ConsoleService()
                asyncio.run(cs.start())

                ## a little more sophisticated
                cs = ConsoleService()
                tasks = [asyncio.create_task(cs.start())]
                asyncio.gather(*tasks)

                ## register commands
                @cs.command(name="my_command", description="a test command", aliases=["my_cmd"], usage="[args]")
                async def command(command: list[str]):
                    print(command)
            ```
        """
        self.running = False
        self.console = Console()
        self.prompt = kwargs.get("prompt", "Console» ")

        self.scope = {
            "locals": kwargs.get("lcls", None),
            "globals": kwargs.get("gbls", {})
        }

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

        ## apply unsafe commands if allowed
        # print(kwargs.get("disable_unsafe_commands"))
        if not kwargs.get("disable_unsafe_commands"):
            self.add_command(name="eval", description="Eval Command ([red blink]UNSAFE[/])", usage="[expr]", func=self.eval_command)
            self.add_command(name="exec", description="Exec Command ([red blink]UNSAFE[/])", usage="[source]", func=self.exec_command)

    async def _async_exec(self, source: str, gbls: Optional[dict[str, Any]] = None, lcls: Optional[dict[str, Any]] = None):
        """
            allows asyncronous exec calls
        """

        if not gbls:
            gbls = {
                "console": self,
                "inspect": inspect
            }

        if not lcls:
            lcls = {}
        
        ## TODO: fix this nastyness
        if "__exec__" in lcls:
            recall = lcls.pop("__exec__")

        exec(
            f'async def __exec__(): ' +
            ''.join(f'\n {l}' for l in source.split('\n')),
            gbls,
            lcls
        )

        ## call our lcls.__ex() call
        return await locals()["lcls"]['__exec__']()
    
    async def eval_command(self, command):
        if len(command) < 1:
            self.console.log("usage: eval [expr]")
            return
        
        try:
            ev = eval(command[1], self.scope["globals"], self.scope["locals"])
            self.console.log(f"Evaluation: {ev}")
        except:
            self.console.print_exception()

    async def exec_command(self, command):
        if len(command) < 1:
            self.console.log("usage: eval [expr]")
            return
        
        try:
            ev = await self._async_exec(command[1], self.scope["globals"], self.scope["locals"])
            self.console.log(ev)
        except:
            self.console.print_exception()

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