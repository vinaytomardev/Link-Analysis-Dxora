import httpx
from bs4 import BeautifulSoup
from app.config import settings

USER_AGENT = "AILinkAnalysisBot/1.0 (+educational project)"

async def extract_website(url: str) -> dict:
    headers = {"User-Agent": USER_AGENT}
    timeout = httpx.Timeout(settings.request_timeout_seconds)
    async with httpx.AsyncClient(
        timeout=timeout, follow_redirects=True, headers=headers
    ) as client:
        response = await client.get(url)
        response.raise_for_status()

    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type.lower():
        raise ValueError("The supplied URL did not return an HTML page.")

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "nav", "footer"]):
        tag.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = description_tag.get("content", "").strip() if description_tag else ""
    headings = [h.get_text(" ", strip=True) for h in soup.find_all(["h1", "h2", "h3"])]
    text = " ".join(soup.stripped_strings)
    text = " ".join(text.split())[:settings.max_page_chars]

    if len(text) < 100:
        raise ValueError("Not enough readable content was found on the website.")

    return {
        "final_url": str(response.url),
        "title": title,
        "meta_description": description,
        "headings": headings[:40],
        "content": text,
    }
