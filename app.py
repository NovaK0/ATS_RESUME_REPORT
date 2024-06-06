from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App

st.set_page_config(page_title="ATS Resume Expert", page_icon="📄", layout="wide")

st.title("📄 ATS Resume Expert")
st.subheader("Optimize Your Resume for Job Applications")

st.markdown("""
    Welcome to the ATS Resume Expert! This tool helps you align your resume with job descriptions, providing detailed evaluations and actionable advice.
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("Instructions")
    st.markdown("""
        1. Enter the job description in the text area below.
        2. Upload your resume (Preferably a single page PDF).
        3. Choose one of the options to analyze your resume.
    """, unsafe_allow_html=True)

input_text = st.text_area("Job Description", key="input", height=150)

uploaded_file = st.file_uploader("Upload your resume (Preferably a single page PDF)", type=['pdf'])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")

col1, col2 = st.columns(2)

with col1:
    submit1 = st.button("📝 Tell Me About the Resume")

with col2:
    submit2 = st.button("📊 Percentage Match with JD")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
Be honest in the response if the resume is not aligning with the job description, point it out.
Please also do make sure that it is a resume only, not any other document.
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of the role mentioned in the job description and ATS functionality.
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches the job description.
First, the output should come as a percentage, then keywords missing, and last final thoughts.
Please also do make sure that it is a resume only, not any other document.
"""

if submit1 and uploaded_file is not None:
    with st.spinner("Processing..."):
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is:")
        st.write(response)
elif submit2 and uploaded_file is not None:
    with st.spinner("Processing..."):
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt2)
        st.subheader("The Response is:")
        st.write(response)
elif (submit1 or submit2) and uploaded_file is None:
    st.warning("Please upload your resume.")
