from PIL import Image
import google.generativeai as genai
import streamlit as st
import time
import random
import os
from mongodb_utils import MongoDatabase
from utils import SAFETY_SETTTINGS
import os
import dotenv

dotenv.load_dotenv()


st.set_page_config(
    page_title="Flow Contract Enhancer",
    page_icon="🔥",
    menu_items={
        "About": "### Flow Contract Enhancer\nMade for optimizing and enhancing Flow blockchain contracts with AI.",
    },
    layout="wide",
)

# Sidebar
st.sidebar.image(
    "flow_logo.png", width=200
)  # Replace 'path_to_flow_logo.png' with actual path to Flow's logo.
st.sidebar.markdown("# 🌊 Flow Contract Enhancer 🚀")
st.sidebar.markdown("## About")
st.sidebar.markdown(
    "This tool uses AI to suggest optimizations and enhancements for your Flow blockchain smart contracts. Simply paste your contract code below!"
)


# # Load avatars
user_avatar = "user.png"  # Replace with the correct path
assistant_avatar = "flow_logo.png"

# Load and split your API keys
api_keys = os.getenv("API_KEYS").split("...")


st.title("Improve your Flow Smart Contract with AI! 🚀")
st.caption(
    "A chatbot that helps you optimize and enhance your Flow blockchain smart contracts. Simply paste your contract code below! 🌊"
)

# Randomly select an API key for this session
if "app_key" not in st.session_state:
    st.session_state.app_key = random.choice(api_keys)

if "history" not in st.session_state:
    st.session_state.history = []

try:
    genai.configure(api_key=st.session_state.app_key)
except AttributeError as e:
    st.warning("Please reload the page to try a different API key.")

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=st.session_state.history)

with st.sidebar:
    if st.button("Clear Chat Window", use_container_width=True, type="primary"):
        st.session_state.history = []
        st.rerun()

for message in chat.history:
    role = "assistant" if message.role == "model" else message.role
    avatar = assistant_avatar if role == "assistant" else user_avatar
    with st.chat_message(role, avatar=avatar):
        st.markdown(message.parts[0].text)

# from mongodb_utils import MongoDatabase

# db = MongoDatabase(os.getenv("MONGO_URI"), os.getenv("MONGO_DB_NAME"))

# def insert_and_display_document():
#     sample_data = {
#         "name": {user},
#         "message": {messages},
#     }
#     inserted_id = db.insert_document("messages", sample_data)
#     st.success(f"Inserted document with ID: {inserted_id}")

#     document = db.find_document("messages", {"_id": inserted_id})
#     st.write(document)

# if st.button("Insert History"):
#     insert_and_display_document()

if "app_key" in st.session_state:
    if prompt := st.chat_input(""):
        prompt = prompt.replace("\n", "  \n")
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            try:
                full_response = ""
                prompt = (
                    "You are a Flow blockchain smart contract expert. You will help users with their Flow smart contract's code. Provide suggestions to optimize and make it more secure, and do any improvements in general. Explain your reasoning and finally provide the finished code. || Here is what the user said:"
                    + prompt
                )
                for chunk in chat.send_message(
                    prompt, stream=True, safety_settings=SAFETY_SETTTINGS
                ):
                    word_count = 0
                    random_int = random.randint(5, 10)
                    for word in chunk.text:
                        full_response += word
                        word_count += 1
                        if word_count == random_int:
                            time.sleep(0.05)
                            message_placeholder.markdown(full_response + "_")
                            word_count = 0
                            random_int = random.randint(5, 10)
                message_placeholder.markdown(full_response)
            except genai.types.generation_types.BlockedPromptException as e:
                st.exception(e)
            except Exception as e:
                st.exception(e)
            st.session_state.history = chat.history
