import streamlit as st
import os
import google.generativeai as genai

# --- CONFIG ---
st.set_page_config(page_title="DSU Campus GenAI Assistant", page_icon="🎓")
st.title("🎓 DSU Campus GenAI Assistant")
st.write("Ask anything about DSU - Syllabus, Exams, Fees, Placements")

# --- SIDEBAR ---
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
st.sidebar.info("Get free key from: aistudio.google.com")

# --- SAMPLE DSU KNOWLEDGE BASE (RAG Demo) ---
# In full version, this comes from PDFs via FAISS. For demo, we use chunks.
DSU_DOCS = """
DSU MCA Syllabus: Sem 1 - Python, DBMS, OS, Maths. Sem 2 - Java, CN, SE, Minor Project MSE-1.
DSU Exam: MSE-1 is 30 marks, MSE-2 is 30 marks, SEE is 40 marks. Attendance 85% required.
DSU Fees: MCA fees per year approx Rs. 1,50,000. Hostel fees separate.
DSU Placement: Average package 6 LPA, Highest 24 LPA. Companies: TCS, Infosys, Wipro, Accenture.
DSU Hostel: Girls hostel curfew 9 PM. Boys hostel curfew 10 PM. Mess timings 7:30 AM - 9 PM.
DSU Library: Open 8 AM - 8 PM, Monday to Saturday. 2 books per student for 14 days.
"""

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

question = st.chat_input("Ask about DSU... e.g. What is MCA Sem 2 syllabus?")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    if not api_key:
        answer = "⚠️ Please enter Gemini API Key in sidebar to get AI answer.\n\n**Demo Answer from DSU Docs:**\n" + DSU_DOCS[:500]
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            prompt = f"""You are DSU Campus Assistant. Answer ONLY from context below.
            If answer not in context, say 'Not found in DSU documents, please contact admin.'
            Always cite source: [DSU Document]

            Context: {DSU_DOCS}
            Question: {question}
            Answer in simple English, max 5 bullet points."""
            response = model.generate_content(prompt)
            answer = response.text + "\n\n**Source:** DSU Handbook / MCA Syllabus PDF"
        except Exception as e:
            answer = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)

# --- EXTRA FEATURES ---
st.divider()
st.subheader("✨ Extra Features")
col1, col2 = st.columns(2)
with col1:
    if st.button("Summarize Circular"):
        st.info("Upload a circular PDF in full version to summarize in 5 points.")
with col2:
    if st.button("Generate 5 MCQs"):
        st.info("Upload notes PDF to generate MCQs from that unit.")
