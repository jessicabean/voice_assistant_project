import requests
import json
from LlamaChatbot.llama_chatbot import load_model, generate_reply

print("Loading Llama 3.2 chatbot...")
load_model()
print("Voice assistant ready!")

# Store conversation history
conversation_history = [
    {
        "role": "system",
        "content": (
            "Act like a personal assistant. "
            "You can respond to questions, translate sentences, summarize news, and give recommendations. "
            "Keep responses concise - 2 to 3 sentences maximum."
        )
    }
]

def speech_to_text(audio_binary):
    # Set up Watson STT API URL    
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = base_url+'/speech-to-text/api/v1/recognize'

    # Set up parameters for HTTP request
    params = {'model': 'en-US_Multimedia'}
    
    # Send an HTTP POST request
    response = requests.post(api_url, params=params, data=audio_binary).json()

    # Parse the response to get transcribed text
    text = 'null'    
    if response.get('results'):
        print('speech to text response:', response)
        text = response['results'][0]['alternatives'][0]['transcript']
        print('recognized text: ', text)
        return text
    return None


def text_to_speech(text, voice=""):
    # Set up Watson TTS API URL    
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'

    # Adding voice parameter in api_url if user has selected a preferred voice
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice
    
    # Set the headers for the HTTP request
    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json'
    }

    # Set the body of the HTTP request
    json_data = {
        'text': text
    }
    
    # Send HTTP POST request to Watson TTS Service
    response = requests.post(api_url, headers=headers, json=json_data)
    print('text to speech response:', response)
    return response.content

def openai_process_message(user_message):
    '''
    Process message with Llama 3.21 chatbot instead of GPT3
    '''

    # Implement Llama chatbot
    response_text = generate_reply(conversation_history, user_message)
    return response_text
