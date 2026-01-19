import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/generate-teaser"

st.set_page_config(page_title="AI Investment Teaser")

st.title("AI-Powered Investment Teaser Generator")

# ---------- FORM ----------
company_name = st.text_input("Company Name")
industry = st.text_input("Industry")
product = st.text_area("Product Description")
stage = st.selectbox("Stage", ["Idea", "Early-stage", "Growth"])
revenue_band = st.selectbox("Revenue", ["Pre-revenue", "<$1M", "$1–5M", "$5M+"])
funding_raised = st.text_input("Funding Raised")
funding_ask = st.text_input("Funding Ask")
location = st.text_input("Location")
deal_type = st.selectbox("Deal Type", ["Investment", "Majority Sale", "Full Sale"])

founder_name = st.text_input("Founder Name")
founder_role = st.text_input("Founder Role")

if st.button("Generate Teaser"):
    payload = {
        "company_name": company_name,
        "industry": industry,
        "product": product,
        "stage": stage,
        "revenue_band": revenue_band,
        "funding_raised": funding_raised,
        "funding_ask": funding_ask,
        "location": location,
        "deal_type": deal_type,
        "team": [{"name": founder_name, "role": founder_role}]
    }

    with st.spinner("Generating teaser..."):
        response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        st.session_state["teaser_data"] = response.json()
        st.session_state["company_name"] = company_name
        st.switch_page("pages/teaser.py")
