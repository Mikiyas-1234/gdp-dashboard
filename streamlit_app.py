# Import necessary libraries
import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv  # Use dotenv to load environment variables
import google.generativeai as genai

# Load all the environment variables from the .env file
load_dotenv()

# Configure the generative AI client with the provided API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY is missing. Please check your .env file or environment variables.")
else:
    genai.configure(api_key)

def get_gemini_response(input_text, image, prompt):
    """Generates a response from the Gemini model based on the input and image."""
    try:
        # Use generative model for processing input and image
        response = genai.generate_text(prompt=prompt, input=image)
        return response.text  # Get the text response
    except Exception as e:
        st.error(f"An error occurred while generating the response: {str(e)}")  # Error handling
        return None

def input_image_details(uploaded_file):
    """Returns image details from the uploaded file."""
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File not found")  # Raise an error if no file is uploaded

# Initialize our Streamlit app
st.set_page_config(page_title="MultiLanguage Text Extractor")

st.header("MultiLanguage Text Extractor")
input_text = st.text_input("Input prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image of the extracted text...", type=["jpg", "jpeg", "png"], key="image")
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the extracted text")

# Define a prompt for the generative AI model
input_prompt = """
You are an expert in understanding text in images. We will upload an image of the text, and you will tell us about the text in the image.
The text can be in any language.
"""

# If the submit button is clicked
if submit:
    try:
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(input_text, image_data, input_prompt)

        st.subheader("The Response is:")
        if response:
            st.write(response)
        else:
            st.error("No response was generated. Please try again.")
    except FileNotFoundError as e:
        st.error(str(e))  # Display error messages on the Streamlit app
