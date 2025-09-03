import asyncio
from quart import Quart, jsonify
from industrious.quart import IndustriousQuart

app = Quart(__name__)

IndustriousQuart(app)

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
