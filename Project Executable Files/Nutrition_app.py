import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import io
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variables
my_api_key = os.getenv('my_api_key')

# Set page configuration
st.set_page_config(page_title="Nutritionist AI 🍏")

# Configure Google Gemini API key
genai.configure(api_key=my_api_key)

# Function to get response from Nutritionist AI based on meal preferences
def get_meal_preference_response(meal_type, intake_type, cuisine, goal, duration):
    # Initialize the GenAI model
    model = genai.GenerativeModel('gemini-pro')

    # Define the content structure
    content = {
        "parts": [
            {"text": f"Generating {meal_type} meals for {duration} days with {intake_type} intake, focusing on {cuisine} cuisine for {goal}."}
        ]
    }

    # Generate content using the model
    response = model.generate_content(content)

    return response.text

# Function to get response from Nutritionist AI based on general query (text or image)
def get_general_query_response(input_text, uploaded_image, use_image):
    if use_image and uploaded_image:
        # Convert uploaded image to PIL image
        pil_image = Image.open(io.BytesIO(uploaded_image.read()))
        # Resize image if needed
        pil_image = pil_image.resize((224, 224))  # Adjust size as needed
        # Convert PIL image back to bytes
        img_bytes = io.BytesIO()
        pil_image.save(img_bytes, format='JPEG')
        img_bytes = img_bytes.getvalue()

        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([input_text, img_bytes])
    else:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([input_text])
    return response.text

# Initialize Streamlit app
st.title("Nutritionist AI 🍏")

# Sidebar for user options
option = st.sidebar.radio("Choose an Option:", ("Meal Preferences", "General Query"))

if option == "Meal Preferences":
    st.header("Meal Preferences")

    # Dropdown options for meal preferences
    meal_type = st.selectbox("Select Meal Type:", ("Breakfast", "Lunch", "Dinner", "Snacks"))
    intake_type = st.selectbox("Select Intake Type:", ("High-Protein", "Low-Carb", "Balanced"))
    cuisine = st.selectbox("Select Cuisine:", ("Indian", "French", "American", "Thai", "Korean", "Italian", "Japanese", "Chinese"))
    goal = st.selectbox("Select Goal:", ("Weight Loss", "Weight Gain"))
    duration = st.slider("Select Duration (days):", min_value=1, max_value=30, value=7)

    if st.button("Generate Meal Plan"):
        response = get_meal_preference_response(meal_type, intake_type, cuisine, goal, duration)
        st.subheader("Meal Preference Query Response")
        st.write(response)

else:
     st.header("General Query")

    # Text input for general query
    



    # Function to get response from Gemini Pro model (text-based)
     def get_gemini_pro_response(input_text):
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([input_text])
        return response.text

# Function to get response from Gemini Pro Vision model (image-based)
     def get_gemini_pro_vision_response(image):
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([image[0]])
        return response.text

     def input_image_setup(uploaded_file):
        # Check if a file has been uploaded
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
            raise FileNotFoundError("No file uploaded")

    # Initialize our streamlit app
     st.title("Gemini NutriAI 🍽️")

     input_text = st.text_input("Input Prompt: ", key="input")
     uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

     if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

     prompt_only = st.button("Get Prompt Response Only")
     with_image = st.button("Get Response with Image")

    # If 'Get Prompt Response Only' button is clicked
     if prompt_only:
        # Handle text-based query here
        response = get_gemini_pro_response(input_text)
        st.subheader("Text-based Query Response")
        st.write(response)

    # If 'Get Response with Image' button is clicked
     if with_image:
        if uploaded_file is not None:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_pro_vision_response(image_data)
            st.subheader("Image-based Query Response")
            st.write(response)
        else:
            st.error("Please upload an image to get a response with image.") 
