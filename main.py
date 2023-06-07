import config
import open_ai_model
from flask import Flask, jsonify, request, send_from_directory
from fpdf import FPDF
import time
import requests

app = Flask(__name__)


@app.route('/file/<filename>')
def send_file(filename):
    return send_from_directory('file', filename)

@app.route("/", methods=['GET'])
def fbverify():
    # global messages
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token")== "chatbot": # Replace "chatbot" with your verify token
            return "Verification token missmatch", 403
        return request.args['hub.challenge'], 200
    return "Hello world", 200

@app.route("/", methods=['POST'])
def fbwebhook():
    data = request.get_json()
    api_key = config.open_ai_key
    file_name = config.dataset 
    file_contents = open_ai_model.load_file_contents(file_name)
    try:
        message = data['entry'][0]['messaging'][0]['message']
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']

        try:
            prompt = message['text']
            chatbot_response = open_ai_model.openai_chatbot(api_key, file_contents, prompt.lower())
            request_body = {
                "recipient": {
                "id": sender_id
                },
                "message": {
                    "text": chatbot_response
                }
            }
            response = requests.post(config.API, json=request_body).json()
            return jsonify(response), 200
        except:
            request_body = {
                "recipient": {
                "id": sender_id
                },
                "message": {
                    "text": "Sorry, I can process only text messages for now."
                }
            }
            response = requests.post(config.API, json=request_body).json()
            return jsonify(response), 200
    except requests.exceptions.RequestException:
        return "not ok", 500 
    
    return "Unhandled request", 400 

if __name__ =='__main__':
    app.run(debug=True, host=config.host, port=config.port)

