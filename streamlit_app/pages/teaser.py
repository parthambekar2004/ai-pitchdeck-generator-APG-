# ================= PYTHON PATH FIX (CRITICAL) =================
import sys
from pathlib import Path

# Add project root (ai_teaser_generator) to PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

# ================= IMPORTS =================
import streamlit as st
import altair as alt
import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

from app.pdf_generator import generate_teaser_pdf

# ================= SCRAPER FUNCTION =================
def fetch_brand_logo(brand_name):
    """
    Searches brandlogos.net for the brand and returns the first logo URL.
    NOTE: Works locally, but not production / interview safe.
    """
    search_url = f"https://brandlogos.net/?s={quote(brand_name)}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        img_tag = soup.find("img", attrs={"class": "attachment-post-thumbnail"})
        if img_tag:
            return img_tag.get("src")
    except Exception:
        return None

    return None

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Investment Teaser",
    layout="wide"
)

# ================= GUARD =================
if "teaser_data" not in st.session_state:
    st.warning("No teaser found. Please generate one first.")
    st.stop()

data = st.session_state["teaser_data"]
company = st.session_state.get("company_name", "Reliance Industries")

# ================= HEADER =================
col1, col2 = st.columns([4, 1])

with col1:
    st.title(f"Investment Teaser: {company}")
    st.caption("Confidential – for discussion purposes only")

with col2:
    logo_url = fetch_brand_logo(company)
    if logo_url:
        st.image(logo_url, width=150)
    else:
        st.caption("Logo unavailable")

st.divider()

# ================= MAIN CONTENT =================
left, right = st.columns([2, 1])

with left:
    st.subheader("Market")
    st.write(data["market"])
    st.caption("Source: AI-inferred")

    st.subheader("Company")
    st.write(data["company"])
    st.caption("Source: Founder-provided")

    st.subheader("Product")
    st.write(data["product"])

    st.subheader("Investment Opportunity")
    st.write(data["investment_opportunity"])

# ================= STOCK SNAPSHOT =================
with right:
    st.subheader("Market Snapshot")

    st.write("**Company Type:** Public")
    st.write("**Exchange:** NSE / BSE")
    st.write("**Ticker:** RELIANCE.NS")

    try:
        stock = yf.Ticker("RELIANCE.NS")

        # ----- TODAY PRICE -----
        today = stock.history(period="2d")

        if not today.empty:
            latest = today.iloc[-1]
            price = latest["Close"]

            if len(today) > 1:
                prev = today.iloc[-2]["Close"]
                pct = ((price - prev) / prev) * 100
            else:
                pct = 0

            st.metric(
                label="Stock Price (Today)",
                value=f"₹{price:,.2f}",
                delta=f"{pct:.2f}%"
            )
        else:
            st.info("Today's price not available")

        # ----- 30 DAY CHART (ALT AIR) -----
        hist_30d = stock.history(period="1mo").reset_index()

        if not hist_30d.empty:
            st.caption("Price Trend (Last 30 Days)")

            chart = (
                alt.Chart(hist_30d)
                .mark_line(color="#4da3ff", strokeWidth=2)
                .encode(
                    x=alt.X("Date:T", title=None),
                    y=alt.Y(
                        "Close:Q",
                        title="Price (₹)",
                        scale=alt.Scale(zero=False)
                    ),
                    tooltip=[
                        alt.Tooltip("Date:T", title="Date"),
                        alt.Tooltip("Close:Q", title="Price (₹)", format=",.2f")
                    ]
                )
                .properties(height=250)
            )

            st.altair_chart(chart, use_container_width=True)

    except Exception:
        st.info("Stock data unavailable")

# ================= PDF DOWNLOAD =================
st.divider()

pdf_buffer = generate_teaser_pdf(company, data)

st.download_button(
    label="📄 Download Teaser as PDF",
    data=pdf_buffer,
    file_name=f"{company.replace(' ', '_')}_Investment_Teaser.pdf",
    mime="application/pdf"
)

# ================= FOOTER =================
st.divider()

if st.button("← Back to Form"):
    st.switch_page("../ui.py")
