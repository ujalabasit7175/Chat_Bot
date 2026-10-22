
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

endpoint = os.getenv("AZURE_ENDPOINT", "").strip().rstrip("/")
api_key = os.getenv("AZURE_API_KEY", "").strip()
deployment = os.getenv("AZURE_DEPLOYMENT", "").strip()

st.set_page_config(page_title="My Azure Chatbot", page_icon="🤖")
st.title("🤖 My Azure Chatbot")
st.caption("Powered by Microsoft Azure AI Foundry")

if not endpoint or not api_key or not deployment:
    st.error("Check your endpoint, API key, and deployment name in .env")
    st.stop()

client = OpenAI(
    base_url=endpoint + "/",
    api_key=api_key
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful, friendly assistant."
        }
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = client.responses.create(
                    model=deployment,
                    input=st.session_state.messages
                )

                answer = response.output_text
                st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(f"Azure request failed: {e}")

            # Remove the failed message so you can retry.
            st.session_state.messages.pop()

            st.info(
                "Check your Azure endpoint, API key, "
                "deployment name, and model access."
            )
