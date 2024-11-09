import os
import pandas as pd
import streamlit as st
import requests
from googletrans import Translator

# Load data from Excel file for offline mode
data = pd.read_excel("/content/pak.xlsx")

# Simulated offline response using the Excel data
def get_offline_response(query):
    # Search the Excel data for the best response
    for _, row in data.iterrows():
        if query.lower() in str(row['Description']).lower():
            return f"Offline mode: {row['Description']}"
    return "Offline mode: Information not available for your query."

# Groq API settings with corrected endpoint URL
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Initialize the Translator object for Google Translate
translator = Translator()

# Streamlit UI for the chatbot
st.title("Virtual Pakistan Travel Guide")
st.subheader("Your friendly virtual tour guide with 40 years of expertise in Pakistan's travel spots.")

# Greeting and initial introduction
st.write("Welcome! You can ask me about famous places, weather, events, or other travel-related topics in Pakistan.")

# Text input for the user query
user_input = st.text_input("Type your question here")

# Button to submit the query and handle response
if st.button("Submit Query"):
    if user_input:
        # Check internet connection and switch to offline mode if unavailable
        try:
            # Request payload for the Groq API
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
            payload = {
                "messages": [{"role": "user", "content": user_input}],
                "model": "llama3-8b-8192"
            }

            # Make the API call directly with requests
            response = requests.post(GROQ_API_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx

            # Parse the API response
            response_json = response.json()
            if 'choices' in response_json and len(response_json['choices']) > 0:
                response_text = response_json['choices'][0]['message']['content']
                st.write("Chatbot response (in English):")
                st.write(response_text)

                # Translate the response text into Urdu
                translated_text = translator.translate(response_text, src='en', dest='ur').text
                st.write("Chatbot response (in Urdu):")
                st.write(translated_text)
            else:
                st.error("Unexpected API response format. Please check the response structure.")

        except requests.exceptions.RequestException:
            # Fallback to offline mode response
            response_text = get_offline_response(user_input)
            st.write(response_text)

            # Translate the offline response into Urdu
            translated_text = translator.translate(response_text, src='en', dest='ur').text
            st.write("Offline response (in Urdu):")
            st.write(translated_text)

# Conclusion and feedback collection
st.write("Thank you for using the Pakistan Travel Assistant!")
feedback = st.text_input("Please provide your feedback here:")
if st.button("Submit Feedback"):
    st.write("Thank you for your feedback!")
  
