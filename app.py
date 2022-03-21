from email import message
from flask import Flask, render_template, request, jsonify

from chatbot import chatbot_response, get_response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.post('/predict')
def predict():
    text = request.get_json().get("message")
    response = chatbot_response(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
