from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS

RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    user_message = request.json.get('message', '')

    if not user_message:
        return jsonify({"reply": "Please enter a valid question."})

    try:
        response = requests.post(RASA_SERVER_URL, json={"message": user_message})
        response_data = response.json()

        if response.status_code == 200 and response_data:
            bot_reply = response_data[0].get('text', "I'm not sure how to respond to that.")
        else:
            bot_reply = "Sorry, I couldn't process your request."

    except requests.exceptions.RequestException as e:
        bot_reply = "Error: Unable to reach chatbot server."

    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
