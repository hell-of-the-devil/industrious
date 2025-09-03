from importlib.util import find_spec
from json import JSONEncoder
from typing import Any
__all__=[
    "default_json_encoder",
    "json_monkey_patch"
]

def default_json_encoder(self, o: Any):
    if hasattr(o, "__json__"):
        return o.__json__()
    
    ## TODO: fix this, i don't really want to import bson if i don't have too
    if o.__class__.__name__ == "ObjectId": 
        return o.__repr__()
    
    return self.super().default(o)


# class JSONClassEncoder(JSONEncoder):
#     def default(self, o):
#         if hasattr(o, '__json__'):
#             return o.__json__()
#         return super().default(o)

def json_monkey_patch():
    """
        allows for __json__ dunder definitions for json output

        :warning: *** Monkey patches are not a good idea for production environments, i just enjoy them ***

        ## Example
        ```python
        import json
        from industrious.json import json_monkey_patch
        json_monkey_patch()

        class test:
            def __json__(self):
                return {"silly": ["little", "things"], "around": "us"}
            
        print(json.dumps(test()))
        ```
    """
    JSONEncoder.default = default_json_encoder

## TODO: find a better way to optionally implement flask/quart stuff
try:
    from quart.json.provider import DefaultJSONProvider
    class JSONClassProvider(DefaultJSONProvider): # type: ignore
            default = default_json_encoder
        
except ImportError as e:
    class JSONClassProvider:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError(f"Usage of {__class__.__name__} requires quart to be installed")
