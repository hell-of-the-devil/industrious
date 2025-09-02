__version__ = "0.0.1"
__author__ = 'Hell of the Devil'
__credits__ = 'Myself :)'

from json import JSONEncoder
def json_monkey_patch():
    """
        This is a json patch to allow __json__ functions within class structures for json output


        :example:
        ```python
            def __json__(self):
                return self.__dict__()
        ```
    """
    def _default(self, o):
        return getattr(o.__class__, "__json__", _default.default)(o)
    _default.default = JSONEncoder().default
    JSONEncoder.default = _default

