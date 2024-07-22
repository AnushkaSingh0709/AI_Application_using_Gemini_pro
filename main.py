import os
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import (load_gemini_pro_model,gemini_1_5_flash_response,embedding_model_response,gemini_pro_response)
from PIL import Image

working_directory = os.path.dirname(os.path.abspath(__file__))

# Setting up the page configuration
st.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout="centered"
)

with st.sidebar:
    selected = option_menu("Gemini AI", ["Chatbot", "Image Captioning", "Embed Text", "Ask Me Anything"],
                           menu_icon='robot', icons=['chat', 'image', 'textarea-t', 'patch-question'],
                           default_index=0)


def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role


if selected == "Chatbot":
    model = load_gemini_pro_model()

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Streamlit title for the Chatbot page
    st.title("🤖 Chatbot")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask Gemini-Pro....")

    if user_prompt:
        # Display user's input
        with st.chat_message("user"):
            st.markdown(user_prompt)
        # Get and display Gemini response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


if selected == "Image Captioning":
    st.title("📷 Snap Narrate")
    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if st.button("Generate Caption"):
        image = Image.open(uploaded_image)
        col1, col2 = st.columns(2)
        with col1:
            resized_image = image.resize((800, 500))
            st.image(resized_image)

        default_prompt = "Write a short caption for this picture"

        # Getting the response from gemini-1.5-flash model
        caption = gemini_1_5_flash_response(default_prompt, image)

        with col2:
            st.info(caption)


if selected=="Embed Text":
    st.title("🔡Embed Text")

    #input text box
    input_text=st.text_area(label="",placeholder="Enter the text to get the embeddings")

    if st.button("Get Embeddings"):
        response=embedding_model_response(input_text)
        st.markdown(response)

if selected=="Ask Me Anything":
    st.title("Ask me a Question❔")

    #textbox to enter prompt
    user_prompt=st.text_area(label="",placeholder="Ask Gemini-Pro...")

    if st.button("Get an Answer"):
        response=gemini_pro_response(user_prompt)
        st.markdown(response)