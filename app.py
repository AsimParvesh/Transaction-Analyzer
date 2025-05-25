
import streamlit as st
import pandas as pd
import openai
from openai import OpenAI
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

        st.subheader("📬 Generating Financial Insights...")
        with st.spinner("Thinking..."):
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial advisor AI."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            insight = response.choices[0].message.content
            st.markdown(insight)
