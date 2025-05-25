
import streamlit as st
import pandas as pd
import openai
import google.generativeai as genai
from utils.parser import extract_transactions_from_pdf


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

        # ✅ Gemini insight generation AFTER df is defined
        import google.generativeai as genai
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

        st.subheader("📬 Generating Financial Insights with Gemini...")

        with st.spinner("Thinking..."):
            try:
                model = genai.GenerativeModel(model_name="gemini-pro")
                response = model.generate_content(
                    f"""
You are a smart financial advisor. Analyze the following UPI transactions and return:

- Total spending
- Any repeating expenses
- Refunds
- Wasteful spending patterns
- Personalized money-saving advice

Format as clean bullet points.

Transactions:
{df.to_string(index=False)}
"""
                )
                st.markdown(response.text)

            except Exception as e:
                st.error(f"❌ Gemini API error: {e}")
