# IW-02 GoogleMarkdown

> Google Search → Markdown for LLMs
> Part of the **PERTURABO Iron Warriors** fleet — SERP/Search API siege.

## 🎯 What It Does

Format AI-ready, token-optimized

## 📡 API Endpoints

### `/search + /search/json`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `q` | string | ✅ | — | Search query |
| `num` | int | ❌ | 10 | Number of results |
| `gl` | string | ❌ | "us" | Country code |
| `hl` | string | ❌ | "en" | Language code |
| `include_snippets` | bool | ❌ | true | Include snippets |

### Response Format

```
Markdown AI-ready + JSON fallback
```

## 💰 Why This Exists

**Target beaten:** SearchCans ($12.67/10K)

This Iron Warrior is self-hosted — no RapidAPI 25% commission, no marketplace tax.
Deploy it on your own infrastructure and pay $0 per request.

## 🚀 Quick Start

```bash
# Install dependencies
pip install fastapi uvicorn httpx beautifulsoup4 pydantic

# Run the Iron Warrior
cd IW-02_GoogleMarkdown
uvicorn main:app --host 0.0.0.0 --port 8000

# Test it
curl "http://localhost:8000/search + /search/json?q=test"
```

## 🏗️ Architecture

```
IW-02_GoogleMarkdown/
├── main.py          # FastAPI app with endpoint(s)
├── shared/
│   └── base.py      # Shared module (HTTP client, parsing, models)
├── requirements.txt # Python dependencies
└── README.md        # This file
```

Built with:
- **FastAPI** — async web framework with auto-generated docs (`/docs`)
- **httpx** — async HTTP client
- **BeautifulSoup4** — HTML parsing
- **Pydantic v2** — type-safe response models

## 📊 Cost Comparison

| Provider | Cost per 10K requests | This Iron Warrior |
|---|---|---|
| RapidAPI (with 25% commission) | SearchCans ($12.67/10K) | **$0** (self-hosted) |

## 🔗 Part of PERTURABO

This Iron Warrior is one of 20 specialized SERP wrappers forged during the
PERTURABO API siege. Each wrapper targets a specific search vertical.

**Fleet status:** 20/20 operational
**Total fleet code:** 2,007 lines
**Shared module:** `base.py` (127 lines)
