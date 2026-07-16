"""
IW-02 GoogleMarkdown — Google Search → Markdown pour LLMs
Iron Warrior #2 — Format AI-ready, token-optimized.
Attaque : SearchCans ($12.67/10K reqs)
"""
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import sys
sys.path.insert(0, '/home/user/iron_warriors/shared')
from base import (
    create_app, fetch_html, SearchResult, SERPResponse,
    clean_text, html_to_markdown, get_timestamp, measure_latency
)
import time

app = create_app("IW-02 GoogleMarkdown", "Google search → Markdown pour LLMs — AI-ready, token-optimized")

class MarkdownResult(BaseModel):
    query: str
    engine: str
    markdown: str
    result_count: int
    timestamp: str
    latency_ms: int

@app.get("/search", response_model=MarkdownResult)
async def google_markdown(
    q: str = Query(..., description="Search query"),
    num: int = Query(10, ge=1, le=50, description="Number of results"),
    gl: str = Query("us"),
    hl: str = Query("en"),
    include_snippets: bool = Query(True, description="Include snippets in markdown"),
):
    start = time.time()
    url = f"https://www.google.com/search?q={quote_plus(q)}&num={num}&gl={gl}&hl={hl}"
    try:
        html = await fetch_html(url)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Google fetch failed: {e}")

    soup = BeautifulSoup(html, 'html.parser')
    results = []
    seen = set()

    for div in soup.find_all('div', class_='g'):
        h3 = div.find('h3')
        link = div.find('a', href=True)
        snippet_tag = div.find('div', class_='VwiC3b') or div.find('span', class_='aCOpRe')
        if h3 and link:
            href = link['href']
            if href.startswith('/url?q='):
                href = href.split('/url?q=')[1].split('&')[0]
            if href in seen or not href.startswith('http'):
                continue
            seen.add(href)
            results.append({
                "title": clean_text(h3.get_text()),
                "url": href,
                "snippet": clean_text(snippet_tag.get_text()) if snippet_tag and include_snippets else "",
                "position": len(results) + 1,
            })
            if len(results) >= num:
                break

    # Build markdown
    md_lines = [f"# Search: {q}\n"]
    md_lines.append(f"_{len(results)} results from Google_\n")
    for r in results:
        md_lines.append(f"## {r['position']}. [{r['title']}]({r['url']})")
        if r['snippet']:
            md_lines.append(f"\n> {r['snippet']}\n")
        md_lines.append("")

    # Related searches
    related = []
    for rs in soup.find_all('a', class_='fl'):
        related.append(clean_text(rs.get_text()))
    if not related:
        for rs in soup.find_all('p', class_='BBwThe'):
            related.append(clean_text(rs.get_text()))
    if related:
        md_lines.append("## Related Searches")
        for r in related[:10]:
            md_lines.append(f"- {r}")
        md_lines.append("")

    markdown = "\n".join(md_lines)

    return MarkdownResult(
        query=q, engine="google",
        markdown=markdown, result_count=len(results),
        timestamp=get_timestamp(), latency_ms=measure_latency(start),
    )

@app.get("/search/json", response_model=SERPResponse)
async def google_markdown_json(
    q: str = Query(...),
    num: int = Query(10, ge=1, le=50),
    gl: str = Query("us"),
    hl: str = Query("en"),
):
    """Same search but returns JSON instead of Markdown."""
    start = time.time()
    url = f"https://www.google.com/search?q={quote_plus(q)}&num={num}&gl={gl}&hl={hl}"
    try:
        html = await fetch_html(url)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Google fetch failed: {e}")

    soup = BeautifulSoup(html, 'html.parser')
    results = []
    seen = set()

    for div in soup.find_all('div', class_='g'):
        h3 = div.find('h3')
        link = div.find('a', href=True)
        snippet_tag = div.find('div', class_='VwiC3b') or div.find('span', class_='aCOpRe')
        if h3 and link:
            href = link['href']
            if href.startswith('/url?q='):
                href = href.split('/url?q=')[1].split('&')[0]
            if href in seen or not href.startswith('http'):
                continue
            seen.add(href)
            results.append(SearchResult(
                title=clean_text(h3.get_text()), url=href,
                snippet=clean_text(snippet_tag.get_text()) if snippet_tag else "",
                position=len(results) + 1,
            ))
            if len(results) >= num:
                break

    return SERPResponse(
        query=q, engine="google", results=results,
        timestamp=get_timestamp(), latency_ms=measure_latency(start),
    )
