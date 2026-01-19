import requests

WIKI_API = "https://en.wikipedia.org/w/api.php"

def fetch_wiki_logo(company_name: str):
    """
    Returns logo image URL from Wikipedia/Wikimedia if available
    """

    # 1️⃣ Search Wikipedia
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": company_name,
        "format": "json"
    }

    search_resp = requests.get(WIKI_API, params=search_params).json()
    search_results = search_resp.get("query", {}).get("search", [])

    if not search_results:
        return None

    page_title = search_results[0]["title"]

    # 2️⃣ Fetch page image
    image_params = {
        "action": "query",
        "titles": page_title,
        "prop": "pageimages",
        "pithumbsize": 400,
        "format": "json"
    }

    image_resp = requests.get(WIKI_API, params=image_params).json()
    pages = image_resp.get("query", {}).get("pages", {})

    for page in pages.values():
        thumbnail = page.get("thumbnail")
        if thumbnail:
            return thumbnail["source"]

    return None
