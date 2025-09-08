import asyncio
from quart import Quart, jsonify
from industrious.quart import IndustriousQuart
from industrious.console_service import ConsoleService
app = Quart(__name__)

console_service = ConsoleService(prompt="Hello> ")

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


async def main():
    tasks = [
        asyncio.create_task(console_service.start()),
        asyncio.create_task(app.run_task())
    ]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
