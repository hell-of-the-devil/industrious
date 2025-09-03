import json
from industrious.json import json_monkey_patch
json_monkey_patch()

class test:
    def __json__(self):
        return {"silly": ["little", "things"], "around": "us"}
    
print(json.dumps(test()))