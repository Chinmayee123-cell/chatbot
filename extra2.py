import streamlit as st
from groq import Groq

# Step 1: Initialize the API client
API_KEY = "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"  # Replace with your actual API key
client = Groq(api_key=API_KEY)

# Step 2: Define the function to fetch chat responses
def get_chat_response(client, messages, stream=False):
    try:
        # Request chat completion from the API
        completion = client.chat.completions.create(
            model="llama3-70b-8192",  # Replace with the correct model name
            messages=messages,
            temperature=0.7,         # Adjust creativity level
            max_tokens=256,          # Set token limit
            top_p=0.9,               # Sampling diversity
            stream=stream,           # Enable or disable streaming
            stop=None                # Specify stop conditions if needed
        )
        
        if stream:
            # Collect streaming chunks
            response = ""
            for chunk in completion:
                response += chunk.choices[0].delta.content or ""
            return response
        else:
            # For non-streaming, access content properly
            response_content = completion.choices[0].message.content
            return response_content
    
    except Exception as e:
        return f"Error occurred: {e}"

# Step 3: Build the Streamlit Interface
st.title("     Chatbot      ")

# Input for user prompt with unique key
user_prompt = st.text_area("Enter your prompt:", placeholder="Type your question here...", key="unique_prompt_1")

# Submit button
if st.button("Send"):
    if user_prompt.strip():
        with st.spinner("Generating response..."):
            # Step 4: Send the user input to the chatbot
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_prompt}
            ]
            response = get_chat_response(client, messages)
        
        # Display the chatbot's response
        st.write("### Chatbot Response:")
        st.write(response)
    else:
        st.warning("Please enter a prompt before sending.")

# Optional Footer
st.markdown("---")
st.caption("Built with Streamlit and Groq API")

