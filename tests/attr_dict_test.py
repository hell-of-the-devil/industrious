import unittest, json
from industrious import AttrDict
test_dict = {
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
        self.test_data = AttrDict(test_dict)

    def test_a(self):
        """
            test if our attrdict source matches our test_dict data
        """
        self.assertDictEqual(self.test_data, test_dict)

    def test_b(self):
        """
            test if our attrdict kwargs works correctly
        """
        self.new_test_data = AttrDict(**test_dict)
        self.assertDictEqual(self.new_test_data, test_dict)

    def test_c(self):
        """
            test if return value of non-existant attributes and items
        """
        self.assertIsNone(self.test_data.nothing)

        with self.assertRaises(KeyError):
            self.test_data["nothing"]
            self.test_data["nothing"]["like"]


        with self.assertRaises(AttributeError):
            self.test_data.nothing.like





if __name__ == '__main__':
    unittest.main()