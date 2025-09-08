import unittest, json
from industrious.json import default_json_encoder

class TestExample:
    def __json__(self):
        return {
            "Hello": "World",
            "Si": ["Lorem", "ipsum", "dolor", "sit", "amet"],
            "obj": {
                "new": "Object",
                "with": "new",
                "data": "in",
                "it": "."
            }
        }

class TestStringMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_data = TestExample()

    def test_a_before_patch(self):
        with self.assertRaises(Exception):
            json.dumps(self.test_data)

    def test_b_after_patch(self):
        self.assertIsInstance(json.dumps(self.test_data, default=default_json_encoder), str)

if __name__ == '__main__':
    unittest.main()