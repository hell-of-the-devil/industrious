import json as _json, time, sys, asyncio

from typing import Dict, Any, Optional

__version__ = "0.0.2"
__author__ = 'Hell of the Devil'
__credits__ = 'Myself :)'

__all__ = [
    "time_duration",
    "AttrDict",
    "asyncio_windows_monkey_patch",
]

def time_duration(epoch_seconds: int, now: Optional[int] = None) -> str:
    if not now:
        now = int(time.time())
    diff = epoch_seconds - now
    
    if diff == 0:
        return "now"

    periods = (
        ("year", 31536000), ## 60 * 60 * 24 * 365
        ("month", 2592000), ## 60 * 60 * 24 * 30
        ("day", 86400),     ## 60 * 60 * 24
        ("hour", 3600),     ## 60 * 60
        ("minute", 60),
        ("second", 1),
    )

    is_future = diff > 0
    diff = abs(diff)

    for period_name, period_seconds in periods:
        if diff >= period_seconds:
            value = int(diff / period_seconds)
            s = "" if value == 1 else "s"
            return f"{'in' if is_future else ''} {value} {period_name}{s} {'ago' if not is_future else ''}".strip()
    
    return "just now"

class AttrDict(Dict):
    """
        Attributed Dictionaries

        This allows for dictionaries to become attributional

        :example:
        ```python
        a = AttrDict({"hello": "world", "goodbye": {"to": "universe"}})

        a.hello = "python"
        print(a["hello"])

        a["get_fucked"] = {"to": "visa/mastercard", "from": "gaben"}
        print(a.get_fucked.from)
        ```
    """
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
        
        for key, value in kwargs.items():
            if isinstance(value, dict) and not isinstance(value, AttrDict):
                self[key] = AttrDict(value)
            else:
                self[key] = value
    
    def __bool__(self):
        return len(self) > 0

    def __getattr__(self, key: str) -> Any:
        return self.get(key, None)

    def __setattr__(self, key: str, value: Any):
        if isinstance(value, dict) and not isinstance(value, AttrDict):
            self[key] = AttrDict(value)
        else:
            self[key] = value

    def __delattr__(self, key: str):
        try:
            del self[key]
        except KeyError:
            return
        
    def tuple_filter(self, values: list[str]) -> tuple:
        """

        """
        def _get_single_value(d, key_string):
            keys = key_string.split('.')
            current_value = d
            try:
                for key in keys:
                    current_value = current_value[key]
                return current_value
            except (KeyError, TypeError):
                return None

        results = [_get_single_value(self, key) for key in values]
        return tuple(results)
    
    def filter(self, values: list[str]) -> 'AttrDict':
        """
            values: ["song.background, "profile.gradient", "section"]
        """
        def _get_single_value(d, key_string):
            keys = key_string.split('.')
            current_value = d
            try:
                for key in keys:
                    current_value = current_value[key]
                return current_value
            except (KeyError, TypeError):
                return None
        results = AttrDict()

        for key in values:
            results[key] = _get_single_value(self, key)

        return results

    @staticmethod
    def test():
        return AttrDict(**{
            "abc": "def",
            "hello": "world",
            "bye": {
                "type": 1,
                "name": "the name",
                "visible": False
            },
            "good": ["This", "is", "a", "list", "of", "strings"]
        })

    @staticmethod
    def from_json_file(file_path: str):
        try:
            with open(file_path, "r") as f:
                return AttrDict(_json.load(f))
        except Exception as e:
            raise e

def asyncio_windows_monkey_patch(loop_policy: Optional[asyncio.events.BaseDefaultEventLoopPolicy] = None):
    ## if we define our defaults for loop_policy in the definition arguments, 
    ## we risk the possibility of poisoning any subsequent calls with a previously modified policy 
    if not loop_policy:
        loop_policy = asyncio.WindowsProactorEventLoopPolicy()
    
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(loop_policy)