import asyncio
from industrious.json import JSONClassProvider
from quart import Quart, jsonify

app = Quart(__name__)
app.json = JSONClassProvider(app)

@app.route('/')
def index():
    class Test:
        def __json__(self):
            return {
                'message': 'This is a JSON response from a custom provider!',
                'list_of_numbers': [1, 2, 3],
                # 'set_of_characters': {'a', 'b', 'c'},
                # 'decimal_value': Decimal('123.45'),
                'boolean_value': True
            }
    
    return jsonify(Test())

if __name__ == '__main__':
    asyncio.run(app.run_task())
