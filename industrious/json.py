from importlib.util import find_spec
from json import JSONEncoder




class JSONClassEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, '__json__'):
            return o.__json__()
        return super().default(o)

def json_class_monkey_patch():
    JSONEncoder.default = JSONClassEncoder ## type: ignore

## TODO: find a better way to optionally implement flask/quart stuff
try:
    from flask.json.provider import DefaultJSONProvider
    class JSONClassProvider(DefaultJSONProvider):
        def default(self, o):
            if hasattr(o, "__json__"):
                return o.__json__()
            return super().default(o)
except ImportError as e:
    pass
