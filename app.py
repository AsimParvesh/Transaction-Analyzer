
import streamlit as st
import pandas as pd
import openai
import google.generativeai as genai
from utils.parser import extract_transactions_from_pdf

# Load API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="📄 UPI Analyzer", layout="centered")
st.title("📊 UPI Financial Analyzer (Offline Version)")

uploaded_file = st.file_uploader("📥 Upload your UPI PDF statement", type=["pdf"])

if uploaded_file:
    file_bytes = uploaded_file.read()
    df = extract_transactions_from_pdf(file_bytes)

    if df.empty:
        st.error("❌ Could not extract any transactions from the PDF.")
    else:
        st.success(f"✅ Extracted {len(df)} transactions")
        st.dataframe(df)

        # Generate insights using LLM
        prompt = f"""
You are a financial analyst assistant. A user has shared their UPI transaction summary. Analyze the following data and return insights in bullet points, followed by a short monthly budget recommendation:

{df.to_string(index=False)}

Focus on:
- Total spending
- Top spending categories (if guessable)
- Refunds and frequency
- Any patterns or excess spending
- Savings advice
"""
# Load Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

        st.subheader("📬 Generating Financial Insights with Gemini...")
        with st.spinner("Thinking..."):
            model = genai.GenerativeModel("gemini-pro")
            prompt_parts = [
                "You are a financial advisor AI. Analyze the following UPI transactions and return insights:",
                df.to_string(index=False),
                """
        Return:
        - Total spending
        - Refunds and frequency
        - Patterns in spending
        - Suggestions to improve savings
        - Budget planning tips
        Present everything in clean markdown.
        """
            ]
            try:
                response = model.generate_content(prompt_parts)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"❌ Gemini API error: {e}")
