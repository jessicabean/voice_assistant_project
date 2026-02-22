from transformers import pipeline
from flask import Flask, request, render_template
import json

def load_model():
    print("Loading Llama 3.2 chatbot - this may take a moment...")

    # Llama 3.21B - state of the art 2024 chatbot
    model_name = "meta-llama/Llama-3.2-1B-Instruct"

    # Load chatbot pipeline
    global chatbot 
    chatbot = pipeline("text-generation", model=model_name)

def generate_reply(conversation_history, input_text):
    # Add user message to history
    conversation_history.append({"role": "user", "content": input_text})

    # Generate response with conversation context
    response = chatbot(
        conversation_history,
        # 150 tokens equates to roughly 110-120 word response
        max_new_tokens=150,
        # Temperature from 0 (fully deterministic) to 2 (very high randomness)
        temperature=0.7,
        # False would mean always picking the most likely conclusion (low variation)
        do_sample=True,
        # Ignore model's internal generation_config settings (otherwise get informational warnings about conflicts)
        generation_config=None,
        # Set pad_token_id explicitly to eliminate informational warnings about setting it
        pad_token_id=128001
    )

    # Extract chatbot's reply
    chatbot_reply = response[0]['generated_text'][-1]['content']

    # Add chatboth's reply to history
    conversation_history.append({"role": "assistant", "content": chatbot_reply})

    # Print chatbot's reply
    return chatbot_reply
