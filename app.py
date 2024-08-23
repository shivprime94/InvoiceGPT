
from dotenv import load_dotenv

load_dotenv()  
import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini Pro Vision model and get respones

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input,image[0],prompt])
    return response.text
    

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        return [image]
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app
st.set_page_config(page_title="InvoiceGPT", page_icon=":moneybag:", layout="centered", initial_sidebar_state="expanded")

st.header("InvoiceGPT")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
else:
    image=Image.open("./invoices/invoice-1.png")
    uploaded_file = open("./invoices/invoice-1.png", "rb")
    st.image(image, caption="Demo Invoice.", use_column_width=True)


submit=st.button("Tell me about the image")

input_prompt = """You are an expert in understanding invoices.You will receive input images as invoices & you will have to answer questions based on the input image
"""

## If ask button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is:")
    st.write(response)
