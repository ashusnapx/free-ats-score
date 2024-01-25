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
As an ATS specialist, I meticulously evaluate resumes in tech, software, and data science for a fierce job market. Provide a percentage match, identify keywords, and offer top-tier guidance.

1. **Contact Information:**
   - Full name
   - Phone number (with country code)
   - Email address
   - LinkedIn profile
   - Location (City, State, ZIP code)

2. **Resume Format:**
   - Compatible formats (.docx, .pdf)
   - Proper naming convention

3. **Keywords and Phrases:**
   - Relevant to job description
   - Industry-specific terms
   - Synonyms and variations

4. **Formatting:**
   - Consistent and professional
   - Proper fonts, spacing, headers
   - Bulleted lists for clarity

5. **Work Experience:**
   - Job titles
   - Company names
   - Employment dates
   - Achievements, quantified

6. **Education:**
   - Degree earned
   - Institution name
   - Graduation date
   - Relevant coursework or honors

7. **Skills:**
   - Keywords from job description
   - Specific skills mentioned
   - Soft and hard skills

8. **Quantifiable Achievements:**
   - Measurable accomplishments
   - Metrics and data support

9. **Online Presence:**
   - LinkedIn and relevant profiles
   - Consistency with resume

10. **Customization:**
    - Tailored to job requirements
    - Avoid generic content
    - Address company's needs

11. **Gaps in Employment:**
    - Explain significant gaps
    - Provide context for career breaks

12. **Consistency:**
    - Consistent tense and formatting
    - Uniform language and style

13. **Length:**
    - Appropriate for experience level
    - Concise without omitting key details

14. **Language and Grammar:**
    - Correct grammar and spelling
    - Avoid jargon not understood by ATS
    - Use impactful action verbs

15. **File Naming:**
    - Professional and identifiable (e.g., FirstName_LastName_Resume.pdf)
    - Avoid special characters

16. **Applicant's Contact:**
    - Track interactions or applications
    - Mention referrals or connections

Check and mark all 16 points. Ignore irrelevant info. Consider industry-grade ATS like Oracle Taleo.

Make a table in which it will have 3 columns, first column will show keywords in job description, 2nd column will show keywords in your resume, and third column will show keywords missing. Make another table considering of all 16 points mentioned above, add tick and cross as required.

*Resume:*
{text}

*Job Description:*
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