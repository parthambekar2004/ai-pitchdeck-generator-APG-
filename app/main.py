from fastapi import FastAPI
from app.schemas import FounderInput, TeaserResponse
from app.generator import generate_section
from app.wiki_logo import fetch_wiki_logo


app = FastAPI(
    title="AI Investment Teaser Generator",
    version="1.0.0"
)

@app.post("/generate-teaser", response_model=TeaserResponse)
def generate_teaser(data: FounderInput):

    market = generate_section(
        "Market",
        "Describe the market context in 3 bullets. Avoid numbers.",
        data.dict()
    )

    company = generate_section(
        "Company",
        "Explain what the company does and who it serves.",
        data.dict()
    )

    product = generate_section(
        "Product",
        "Describe the product and its core value proposition.",
        data.dict()
    )

    investment = generate_section(
        "Investment Opportunity",
        "Explain why this could be attractive to investors.",
        data.dict()
    )

    return {
        "market": market,
        "company": company,
        "product": product,
        "investment_opportunity": investment
    }

@app.get("/logo/wiki")
def get_wiki_logo(company: str):
    logo_url = fetch_wiki_logo(company)
    return {"logo": logo_url}
