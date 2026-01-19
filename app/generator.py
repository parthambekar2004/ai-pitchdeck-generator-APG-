import json
from app.gemma_client import call_gemma
from app.prompts import SYSTEM_PROMPT

def generate_section(section_name, instructions, founder_data):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""
Section: {section_name}

Company Context:
{json.dumps(founder_data, indent=2)}

Instructions:
{instructions}

Output bullet points only.
"""
        }
    ]

    return call_gemma(messages)
