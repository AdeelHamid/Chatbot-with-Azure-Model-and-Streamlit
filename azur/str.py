import streamlit as st
import requests
import json

# Replace with your actual Azure endpoint URI and API key
AZURE_ENDPOINT_URI = ""
AZURE_API_KEY = ""

# Set up the Streamlit page
st.title("Azure AI Chatbot")
st.write("Ask me anything! I am powered by a model deployed on Azure.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare data for the API request
    # The structure must match the format expected by the model's API
    # This is a common format for chat models, but may vary
    data = {
        "messages": [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
    }

    # Set up request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AZURE_API_KEY}",
        # Some models require an azureml-model-deployment header
        "azureml-model-deployment": "YOUR_DEPLOYMENT_NAME"
    }

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Make the API call to the Azure endpoint
                response = requests.post(AZURE_ENDPOINT_URI, json=data, headers=headers)
                response.raise_for_status()  # Raise an exception for bad status codes

                # Extract the assistant's response
                response_content = response.json()["choices"][0]["message"]["content"]
                st.markdown(response_content)
                
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
                response_content = "An error occurred. Please check the endpoint and API key."

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})