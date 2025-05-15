import os
import httpx
from bs4 import BeautifulSoup

BRIGHT_MCP_HOST = os.getenv("MCP_HOST", "http://localhost")
BRIGHT_MCP_PORT = os.getenv("MCP_PORT", "8191")
BRIGHT_MCP_TOKEN = os.getenv("BRIGHT_DATA_API_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {BRIGHT_MCP_TOKEN}"
}

def parse_amazon(html: str):
    soup = BeautifulSoup(html, "lxml")
    results = []
    items = soup.select("div.s-main-slot div[data-component-type='s-search-result']")
    for item in items[:5]:  # Limit for speed
        title = item.select_one("h2 span")
        price_whole = item.select_one(".a-price-whole")
        price_fraction = item.select_one(".a-price-fraction")
        rating = item.select_one(".a-icon-alt")
        results.append({
            "title": title.text.strip() if title else "N/A",
            "price": f"${price_whole.text.strip()}.{price_fraction.text.strip()}" if price_whole and price_fraction else "N/A",
            "rating": rating.text.strip() if rating else "N/A"
        })
    return results

async def extract_product_data(urls: list[str]):
    all_results = []
    async with httpx.AsyncClient(timeout=30.0) as client:
        for url in urls:
            try:
                response = await client.post(
                    f"{BRIGHT_MCP_HOST}:{BRIGHT_MCP_PORT}/browser",
                    headers=HEADERS,
                    json={"url": url, "render": True}
                )
                if response.status_code == 200:
                    html = response.json().get("content", "")
                    if "amazon" in url:
                        parsed = parse_amazon(html)
                    else:
                        parsed = [{"title": "Unsupported site", "price": "N/A", "rating": "N/A"}]
                    all_results.extend(parsed)
            except Exception as e:
                print(f"Error scraping {url}: {str(e)}")
    return all_results
