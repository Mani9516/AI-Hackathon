import streamlit as st
import os
import requests
import json

# Set the API key (in environment variables or hardcoded here)
os.environ["GEMINI_API_KEY"] = "AIzaSyAAje9hxCF6TxXb7_y-cZ2P7TQunb2Nc-8"
GEMINI_API_URL = "https://api.gemini.example.com/v1/chat"  # Ensure this is the correct API endpoint

# Load knowledge base from JSON file
def load_knowledge_base(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

knowledge_base = load_knowledge_base('knowledge_base.json')

# Search the knowledge base for pre-defined answers
def search_knowledge_base(query):
    for issue, solution in knowledge_base.items():
        if issue in query.lower():
            return solution
    return None

# Call the Gemini API for a response when the knowledge base does not have the answer
def generate_response_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.7
    }
    
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("text", "").strip()
    else:
        return f"Error: Could not fetch response from Gemini API. Status Code: {response.status_code}"

# Main function to process user queries
def chatbot(query):
    # Try to search the knowledge base first
    knowledge_base_response = search_knowledge_base(query)
    if knowledge_base_response:
        return f"**Answer from Knowledge Base** : {knowledge_base_response}"
    else:
        # Fall back to Gemini API if no knowledge base match is found
        gemini_response = generate_response_gemini(query)
        return f"**AI-Powered Response (Gemini)**: {gemini_response}"

# Streamlit UI
st.title("Gemini AI Chatbot")
st.write("Chatbot for How-To's, Troubleshooting, and Content Creation using the Gemini API.")

# Take user input via text input
user_input = st.text_input("Enter your prompt:")

# If the user provides an input, generate a response
if user_input:
    response = chatbot(user_input)
    st.write(response)
