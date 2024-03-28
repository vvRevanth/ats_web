import streamlit as st
import openai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import pandas as pd

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Smart ATS",
    page_icon="👨‍💼",
    layout="centered",
)

# Define your OpenAI API Key
API_KEY = os.getenv("AIzaSyD2oLQHkz9sYQvKZN6VaZ7ZI2t2N79wefQ")  # Make sure you have this key set in your environment variables

# Function to configure OpenAI API with the provided API key
def configure_openai_api(api_key):
    openai.api_key = api_key

# Function to get response from OpenAI's GPT-3 model
def get_gpt3_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the appropriate engine for your task
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Load job postings data
@st.cache
def load_job_postings():
    job_postings = pd.read_csv('job.csv')
    return job_postings

# Streamlit app
st.title("Resume Matcher ATS")

# Configure OpenAI API
configure_openai_api(API_KEY)

# Load job postings
job_postings = load_job_postings()

if 'title' not in job_postings.columns:
    st.error("Job postings data does not contain the 'title' column.")
    st.stop()

# Filter job titles
search_query = ""
filtered_job_titles = job_postings['title'][job_postings['title'].str.contains(search_query, case=False)].tolist()

selected_job_titles = st.multiselect("Select Job Titles", filtered_job_titles)
if not selected_job_titles:
    st.info("Please select at least one job title.")
    st.stop()

# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analyst
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide the 
best assistance for improving the resumes. Assign the percentage Matching based 
on JD and the missing keywords with high accuracy.
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
"""

## Streamlit app
st.title("Resume Matcher ATS")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gpt3_response(input_prompt.format(text=text, jd=selected_job_titles))
        st.subheader("Response:")
        parsed_response = json.loads(response)
        for key, value in parsed_response.items():
            st.write(f"{key}:** {value}")
