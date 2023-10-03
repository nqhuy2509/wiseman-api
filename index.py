from flask import Flask
from flask import request
from controllers.summary_controller import SummaryController
from flask import jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/summary', methods=['POST'])
@cross_origin(supports_credentials=True)
def summary():
    data = request.get_json()

    if 'text' not in data or 'percentage' not in data or 'language' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    result, length = SummaryController(data['text'], data['percentage'], data['language']).summarize()

    return jsonify({
        'summary': result,
        'length': length
    })


if __name__ == '__main__':
    app.run()
