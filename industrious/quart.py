import json
from . import time_duration

__all__ = ["IndustriousQuart"]

class IndustriousQuart:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.industrious = self

        app.jinja_env.filters["to_json"] = self.to_pretty_json
        app.jinja_env.filters["time_duration"] = time_duration
    
    ## junja_env filters
    def to_pretty_json(self, value):
        return json.dumps(value, sort_keys=True, indent=4)