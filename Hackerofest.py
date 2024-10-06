import streamlit as st
import os
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set the API key (in environment variables or hardcoded here)
os.environ["GEMINI_API_KEY"] = "AIzaSyAAje9hxCF6TxXb7_y-cZ2P7TQunb2Nc-8"
GEMINI_API_URL = "https://api.gemini.example.com/v1/chat"  # Ensure this is the correct API endpoint

# Updated knowledge base with new scenarios
knowledge_base = {
    "inventory discrepancy": "This issue is caused when inventory levels in Hotwax are not updated in Shopify. Ensure that the synchronization flow for inventory is active.",
    "order mismatch": "Order mismatches occur when order data is not fully transmitted. Check the synchronization status for orders and retry the failed jobs.",
    "product information error": "Ensure that product synchronization between Hotwax and Shopify is active and running to avoid product information discrepancies.",
    "products not available in hotwax commerce": (
        "1. Verification on Shopify: Go to Shopify and verify if the products are available. If not, create the missing products.\n"
        "2. Run Product Import Job: In the Job Manager app, execute the Product Import job to ensure the products are imported into HotWax Commerce."
    ),
    "product available in shopify and not available in oms": (
        "1. Check Shopify Jobs Section: Navigate to the HotWax Commerce platform and access the EXIM section.\n"
        "2. Review MDM Jobs: Look for the Create Update Shopify Products job and inspect logs for any failed errors.\n"
        "3. Identify Error Messages: Examine the JSON file for specific error details and address them accordingly.\n"
        "4. Import Orders: Manually import orders if needed. For technical errors, contact HotWax support."
    ),
    "creating a product and its variants in multiple steps": (
        "This issue occurs when a product and its variants are not created simultaneously in Shopify. To avoid this:\n"
        "1. Create All Product Variants at Once: Ensure that all product variants are created in Shopify at the same time.\n"
        "2. Disable Product Sync Job Temporarily: Disable the sync job while creating products and re-enable it after."
    ),
    "how to sync products that are not synced in hotwax commerce": (
        "1. Access the EXIM Menu in HotWax Commerce.\n"
        "2. Choose Shopify Config and Enter Product IDs: Select the appropriate config and enter the Shopify Product IDs.\n"
        "3. Run the Sync: Click the Run button to start synchronization."
    ),
    "cloning product in shopify": (
        "This issue arises when a product is created in Shopify by cloning an existing product. To synchronize metafields:\n"
        "1. Access the Job Manager App and find the Import Metafields Job.\n"
        "2. Run the Job: Click Run Now to import the metafields from Shopify."
    )
}

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
    response = chatbot(user_input)  # Use chatbot() instead of generate_response()
    st.write(response)
