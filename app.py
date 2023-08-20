from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello world"

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run()
