# resume_analyzer.py
import streamlit as st
import PyPDF2
import google.generativeai as genai

# 🚨 Replace with your actual API key
genai.configure(api_key="AIzaSyBp9npZeUo2QnR-wWdISXUqLIzSSWajp5I")

def extract_text_from_pdf(f):
    reader = PyPDF2.PdfReader(f)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def call_gemini(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
    return model.generate_content(prompt).text

def build_prompt(resume, job_desc):
    return f"""
Act as an experienced HR professional.
From this resume:
{resume}
And this job description:
{job_desc}

1. List key skills.
2. Summarize work experience in 2–3 sentences.
3. Rate alignment on a scale of 0–100.
4. Highlight any skills missing relative to the job description.
Respond in JSON format like:
{{
  "skills": [...],
  "summary": "...",
  "alignment_score": 85,
  "missing_skills": [...]
}}
"""

st.title("📄 Resume Analyzer with Gemini")
resume_file = st.file_uploader("Upload your resume (PDF or .txt)", type=["pdf", "txt"])
job_desc = st.text_area("Paste the job description here")

if st.button("Analyze"):
    if not resume_file or not job_desc.strip():
        st.error("Please upload a resume and enter a job description.")
    else:
        with st.spinner("Extracting text..."):
            resume_content = (
                extract_text_from_pdf(resume_file)
                if resume_file.type == "application/pdf"
                else resume_file.read().decode("utf-8")
            )
        prompt = build_prompt(resume_content, job_desc)
        with st.spinner("Contacting Gemini..."):
            result = call_gemini(prompt)
        st.subheader("✅ Analysis Result")
        st.code(result, language="json")
