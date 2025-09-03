import json
from quart import Quart
from quart.json.provider import DefaultJSONProvider

from . import time_duration
from .json import default_json_encoder

__all__ = ["IndustriousQuart", "JSONClassProvider"]

class JSONClassProvider(DefaultJSONProvider):
        default = default_json_encoder ## type: ignore

class IndustriousQuart:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Quart):
        app.industrious = self ## type: ignore
        
        app.json = JSONClassProvider(app)

        app.jinja_env.filters["to_json"] = self.to_pretty_json
        app.jinja_env.filters["time_duration"] = time_duration
    
    ## junja_env filters
    def to_pretty_json(self, value):
        return json.dumps(value, sort_keys=True, indent=4)