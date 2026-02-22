import base64
import json
from flask import Flask, render_template, request
from worker import speech_to_text, text_to_speech, openai_process_message
from flask_cors import CORS
import os

app = Flask(__name__)
# Sets up CORS policy set allowing requests to any domain (not just host of webpage)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    print("Processing speech to text")
    
    # Get user's speech from their request
    audio_binary = request.data
    
    # Call speech_to_text
    text = speech_to_text(audio_binary)

    # Return the response in JSON format
    response = app.response_class(
        response = json.dumps({'text': text}),
        status = 200,
        mimetype = 'application/json'    
    )

    # Output response text for troubleshooting
    print(response)
    print(response.data)

    return response


@app.route('/process-message', methods=['POST'])
def process_prompt_route():
    # Get user's message from their request
    user_message = request.json['userMessage']
    print('user_message:', user_message)

    # Get user's preferred voice from their request
    voice = request.json['voice']
    print('voice:', voice)

    # Call openai_process_message to process user's message
    openai_response_text = openai_process_message(user_message)

    # Clean the response to remove any empty lines
    openai_response_text = os.linesep.join([s for s in openai_response_text.splitlines() if s])

    # Call our text_to_speech function to convert response to speech
    openai_response_speech = text_to_speech(openai_response_text, voice)

    # Convert to base64 string so it can be sent back in JSON response
    openai_response_speech = base64.b64encode(openai_response_speech).decode('utf-8')

    # Send a JSON response back to the user containing the response in both text and speech formats
    response = app.response_class(
        response=json.dumps({"openaiResponseText": openai_response_text, "openaiResponseSpeech": openai_response_speech}),
        status=200,
        mimetype='application/json'
    )
    print(response)
    return response


if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
