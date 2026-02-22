from openai import OpenAI
import requests
import json

openai_client = OpenAI()


def speech_to_text(audio_binary):
    # Set up Watson STT API URL    
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = base_url+'/speech-to-text/api/v1/recognize'

    # Set up parameters for HTTP request
    params = {'model': 'en-US_Multimedia'}
    
    # Send an HTTP POST request
    response = request.post(api_url, params=params, data=audio_binary).json()

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
    if voice != "" and voice !+ "default":
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
    response = request.post(api_url, headers=headers, json=json_data)
    print('text to speech response:', response)
    return response.content

def openai_process_message(user_message):
    # Set the prompt for OpenAI API
    prompt = (
        "Act like a personal assistant." 
        "You can respond to questions, translate sentences, summarize news, and give recommendations." 
        "Keep responses concise - 2 to 3 sentences maximum."
    )

    # Call the OpenAI API to process the prompt
    openai_response = openai_client.chat.completions.create(
        model = "gpt-5-nano",
        messages=[
            {"role": "system", "content": prompt}
            {"role": "user", "conent": user_message}
        ],
        max_completion_tokens=1000
    )
    print("open ai response:", openai_response)

    # Parse responses to the message for the prompty
    response_text = openai_response.choices[0].message.content
    resturn response_text
