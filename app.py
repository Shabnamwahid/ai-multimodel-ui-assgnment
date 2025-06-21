
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Models list
model_options = {
 
    "GPT-3.5 Turbo": "openai/gpt-3.5-turbo",
    "Claude 3 Haiku": "anthropic/claude-3-haiku",
    "LLaMA 3": "meta-llama/llama-3-70b-instruct",
    "Mistral 7B": "mistralai/mistral-7b-instruct",
   "Mixtral 8x7B": "mistralai/mixtral-8x7b-instruct" ,
}

# Streamlit app
st.set_page_config(page_title="Simple AI Chat", layout="centered")
st.title(" 🤖Multi-Model AI Chatbot")

# Model selection
selected_model = st.selectbox("Choose a Model:", list(model_options.keys()))

# Ask question
question = st.text_input("Ask your question:")

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please type a question first.")
    else:
        model_id = model_options[selected_model]
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model_id,
                    "messages": [{"role": "user", "content": question}]
                }
            )
            data = response.json()
            if "choices" in data:
                answer = data["choices"][0]["message"]["content"]
            else:
                answer = "⚠️ No answer received."
        except Exception as e:
            answer = f"❌ Error: {str(e)}"

        st.markdown("### 💡 Answer:")
        st.write(answer)
