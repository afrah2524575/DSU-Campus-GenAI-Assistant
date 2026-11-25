import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

st.set_page_config(page_title="DSU Campus GenAI Assistant", page_icon="🎓")
st.title("🎓 DSU Campus GenAI Assistant")
st.write("Ask anything about DSU | Upload Circular PDF to Summarize")

# --- SIDEBAR ---
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
st.sidebar.info("Get free key from: aistudio.google.com")

# --- FEATURE 1: UPLOAD CIRCULAR PDF & SUMMARIZE IN 5 POINTS ---
st.subheader("📄 Upload Circular PDF to Summarize in 5 Points")
uploaded_file = st.file_uploader("Upload DSU Circular / Notice PDF", type=["pdf"])

if uploaded_file is not None:
    st.write(f"✅ File uploaded: {uploaded_file.name}")
    if not api_key:
        st.warning("⚠️ Please enter Gemini API Key in sidebar first.")
    else:
        if st.button("Summarize This Circular"):
            with st.spinner("Reading PDF and summarizing..."):
                try:
                    reader = PdfReader(uploaded_file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""
                    
                    st.write(f"✅ PDF Read: {len(reader.pages)} pages")

                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    prompt = f"""Summarize this DSU circular in EXACTLY 5 bullet points.
                    Make it simple for students. Include: What is it about, Last Date, Who is eligible, What to do, Where to submit.
                    At end, add Source: Uploaded Circular PDF.

                    Circular Text:
                    {text[:8000]}
                    """
                    response = model.generate_content(prompt)
                    st.success("Summary Ready:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

st.divider()

# --- FEATURE 2: NORMAL Q&A ---
st.subheader("💬 Ask DSU Question")
DSU_DOCS = """
DSU MCA Syllabus: Sem 1 - Python, DBMS, OS, Maths. Sem 2 - Java, CN, SE, Minor Project.
DSU Exam: MSE-1 30 marks, MSE-2 30 marks, SEE 40 marks. Attendance 85% required.
DSU Fees: MCA fees approx Rs. 1,50,000 per year.
DSU Placement: Average 6 LPA, Highest 24 LPA. Companies: TCS, Infosys, Wipro.
DSU Hostel: Girls curfew 9 PM, Boys 10 PM. Library 8 AM - 8 PM.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

question = st.chat_input("Ask about DSU...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)
    if not api_key:
        answer = "Please enter API Key in sidebar."
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"You are DSU Assistant. Answer from context: {DSU_DOCS}. Question: {question}. Give 5 bullet points and cite Source: DSU Document"
        answer = model.generate_content(prompt).text
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
