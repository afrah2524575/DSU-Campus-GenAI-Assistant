# LLM - Gemini call
import google.generativeai as genai
def ask_gemini(api_key, prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    return model.generate_content(prompt).text
