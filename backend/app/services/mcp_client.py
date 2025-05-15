import os
import httpx

BRIGHT_MCP_HOST = os.getenv("MCP_HOST", "http://localhost")
BRIGHT_MCP_PORT = os.getenv("MCP_PORT", "8191")
BRIGHT_MCP_TOKEN = os.getenv("BRIGHT_DATA_API_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {BRIGHT_MCP_TOKEN}"
}

async def discover_products(query: str):
    # Optional: use search engine scraping
    return {
        "urls": [
            f"https://www.amazon.com/s?k={query.replace(' ', '+')}",
            f"https://www.ebay.com/sch/i.html?_nkw={query.replace(' ', '+')}"
        ]
    }

async def extract_product_data(urls: list[str]):
    results = []
    async with httpx.AsyncClient() as client:
        for url in urls:
            response = await client.post(
                f"{BRIGHT_MCP_HOST}:{BRIGHT_MCP_PORT}/browser",
                headers=HEADERS,
                json={"url": url, "render": True}
            )
            if response.status_code == 200:
                content = response.json().get("content", "")
                # Optional: parse using BeautifulSoup or XPath
                results.append({"url": url, "html": content})
    return results
