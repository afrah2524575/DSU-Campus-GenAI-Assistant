# DSU Campus GenAI Assistant

An LLM-powered RAG Chatbot for Dayananda Sagar University queries.
Built for RTD Open Elective - 30 Marks

**Author:** Barsharani Patra - SCA25MCA093
**Stack:** Python, Streamlit, Gemini 2.0 Flash, FAISS, RAG

## Features
- Ask Anything about DSU - Syllabus, Exams, Fees, Placements
- Source-Cited Answers from Official PDFs
- Upload Your PDF & Ask Questions
- Summarizer + MCQ Generator
- Hinglish Mode

## How to Run
pip install -r requirements.txt
streamlit run app.py

## Architecture
User Question -> Embedding -> FAISS Search -> Gemini LLM -> Answer + Source
