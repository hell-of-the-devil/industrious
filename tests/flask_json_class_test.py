
from industrious.json import JSONClassProvider
from flask import Flask, jsonify

# Create the Flask application instance.
app = Flask(__name__)

app.json = JSONClassProvider(app)
# Assign the custom JSON provider class to the app.
# app.json_provider_class = JSONClassProvider

@app.route('/')
def index():
    """
    A simple route that returns a JSON response.
    The response includes a 'set' and a 'Decimal' object, which
    are now handled by our CustomEncoder.
    """

    class Test:
        def __json__(self):
            return {
            'message': 'This is a JSON response from a custom provider!',
            'list_of_numbers': [1, 2, 3],
            # 'set_of_characters': {'a', 'b', 'c'},
            # 'decimal_value': Decimal('123.45'),
            'boolean_value': True
        }
    
    # jsonify will now use our custom provider to serialize the data.
    return jsonify(Test())

if __name__ == '__main__':
    # Run the application in debug mode.
    # To test this, you can run the script and then navigate to
    # http://127.0.0.1:5000/ in your web browser.
    app.run(debug=True)
