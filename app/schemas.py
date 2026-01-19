from pydantic import BaseModel
from typing import List

class TeamMember(BaseModel):
    name: str
    role: str

class FounderInput(BaseModel):
    company_name: str
    industry: str
    product: str
    stage: str
    revenue_band: str
    funding_raised: str
    funding_ask: str
    location: str
    deal_type: str
    team: List[TeamMember]

class TeaserResponse(BaseModel):
    market: str
    company: str
    product: str
    investment_opportunity: str
