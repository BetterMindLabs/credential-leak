import streamlit as st
import google.generativeai as genai

# === Configure Gemini ===
api_key = st.secrets["api_keys"]["google_api_key"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# === Streamlit UI ===
st.set_page_config(page_title="🔐 Credential Leak Checker")
st.title("🔐 Credential Leak Checker")
st.write("Paste a suspicious credential or key below. The system will analyze it for potential exposure risk.")

# Input box
leaked_input = st.text_area(
    "Paste token / API key / email:password combo / suspicious string",
    height=200,
    placeholder="e.g. AWS_SECRET=AKIAIOSFODNN7EXAMPLE"
)

if st.button("Analyze Leak"):
    if not leaked_input.strip():
        st.warning("Please paste a suspicious credential or string.")
    else:
        with st.spinner("Analyzing with Gemini..."):
            prompt = f"""
You are a cybersecurity LLM trained to assess potential credential leaks or exposure risks.

Given the following input string, identify:
- Verdict: Leak / Not a Leak / Unclear
- Credential Type: API Key / Email+Password / Token / Other
- Severity: Low / Medium / High
- Reason: Short factual explanation (1-2 lines max)

Input:
\"\"\"{leaked_input}\"\"\"

Respond in this format:
Verdict: <...>  
Credential Type: <...>  
Severity: <...>  
Reason: <...>
"""

            response = model.generate_content(prompt)
            result = response.text.strip()

       
        st.text(result)
