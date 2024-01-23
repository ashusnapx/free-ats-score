import streamlit as st
import os
import google.generativeai as genai
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Gemini AI
genai.configure(api_key=os.getenv('GOOGLE_GEMINI_KEY'))

input_prompt = '''
As an adept ATS (Application Tracking System) professional specializing in the tech, software, data science, and big data engineering domains, your task is to meticulously evaluate a given resume within the context of a fiercely competitive job market. Your expertise is sought to analyze the resume against a provided job description, assign a percentage match based on key criteria, identify missing keywords with unparalleled accuracy, and deliver top-tier guidance for resume enhancement.

Please structure your response in a single string format with meticulous formatting in best possible structure, incorporating the following elements. JD Match in percentage, an aaray of missing keywords, and profile summary should be short, crisp, with all important information and numbers and professional, also add a section which tells what are information in your resume is useless, redundant and unprofessional.

Resume:
{text}

Job Description:
{jd}
'''

# Function to get Gemini response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Function to extract text from PDF
def text_in_uploaded_pdf(uploaded_file):
    read = pdf.PdfReader(uploaded_file)
    text = ''
    for page in range(len(read.pages)):
        page_text = read.pages[page].extract_text()
        text += f"Page {page + 1}:\n{page_text}\n\n"
    return text

# Main Streamlit app
def main():
    # Set app title and page icon
    st.set_page_config(page_title='Free ATS Score Checker', page_icon=':shark', layout="wide")

    # Set app title and description
    st.title('Free ATS Score Checker 📊')
    st.markdown(
        "Evaluate your resume against a job description to get an ATS score. "
        "Improve your chances of getting shortlisted in the competitive job market."
    )

    # Job description input
    jd = st.text_area('Paste the job description', help='Copy and paste the job description from the job posting.')

    # Resume upload
    uploaded_file = st.file_uploader('Upload your resume (PDF)', type='pdf', accept_multiple_files=False)

    # Check ATS Score button
    submit = st.button('Check ATS Score')

    # Display loading spinner while processing
    if submit:
            if uploaded_file is not None and len(jd) > 50:

                # Process the uploaded PDF
                text = text_in_uploaded_pdf(uploaded_file)

                # Get Gemini response
                response = get_gemini_response(input_prompt.format(text=text, jd=jd))

                # Display result
                st.success('Your ATS score has been calculated successfully! 🚀')
                st.subheader('ATS Score Results')
                st.markdown(response)
                st.subheader('_Thanks for using the tool made by_ :blue[@ashusnapx] :sunglasses:')
            else:
                # Display error messages
                if len(jd) < 50:
                    st.error('Please enter a detailed job description. 🧐')
                elif uploaded_file is None:
                    st.error('Please upload your resume (PDF). 🥲')

if __name__ == "__main__":
    main()
