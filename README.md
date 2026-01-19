# AI Investment Teaser Generator

An AI-powered application that generates a one-page investment teaser using minimal founder input.

## Features
- AI-generated market, company, product & investment sections
- Public market stock snapshot (price + 30-day trend)
- Clean teaser UI
- One-click PDF export

## Tech Stack
- Streamlit (Frontend)
- FastAPI (Backend)
- Gemma 3 via Google Gemini API
- Altair (Charts)
- pandas
- yFinance (Market Data)
- ReportLab (PDF Generation)

# --- HTTP & parsing ---
- requests
- beautifulsoup4

## Setup Instructions

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
