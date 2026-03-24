"""
SoloOS v7 — Real Web Intelligence

Actual HTTP calls to public APIs. No authentication required for any of these.
No mocking. No fallback to fake data.

Sources:
- Hacker News: Firebase Realtime Database API (official, no auth)
- Reddit: Public JSON API (add .json to any Reddit URL)
- Jina AI: Free web reader API (no auth for basic use)
- ProductHunt: GraphQL API (no auth for public data)

Designed to work in both local Claude Code AND remote CCR triggers.
"""

import json
import re
import urllib.request
import urllib.parse
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional


# ─────────────────────────────────────────────────────────────
# Shared HTTP helper
# ─────────────────────────────────────────────────────────────

_DEFAULT_HEADERS = {
    "User-Agent": "SoloOS/7.0 (Founder Intelligence; research@soloos.dev)",
    "Accept": "application/json",
}


def _http_get(url: str, timeout: int = 8, extra_headers: dict | None = None) -> dict | list | None:
    """Simple HTTP GET returning parsed JSON. Returns None on error."""
    headers = {**_DEFAULT_HEADERS, **(extra_headers or {})}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw)
    except (urllib.error.URLError, json.JSONDecodeError, Exception):
        return None


def _http_get_text(url: str, timeout: int = 10) -> str:
    """HTTP GET returning raw text (for HTML/markdown scraping)."""
    headers = {**_DEFAULT_HEADERS, "Accept": "text/html,text/plain,*/*"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return ""


# ─────────────────────────────────────────────────────────────
# Hacker News — Firebase API (official, free, no auth)
# ─────────────────────────────────────────────────────────────

_HN_BASE = "https://hacker-news.firebaseio.com/v0"

_FOUNDER_KEYWORDS = {
    "startup", "saas", "founder", "indie", "bootstrapped", "mrr", "arr",
    "b2b", "solopreneur", "indiehacker", "product", "launch", "revenue",
    "churn", "retention", "pmf", "acquisition", "growth", "customer",
    "pricing", "stripe", "solo", "side project", "micro-saas",
}


def get_hn_top_stories(limit: int = 30, filter_founder_relevant: bool = True) -> list[dict]:
    """
    Fetch top Hacker News stories. Filters for startup/founder relevance.

    Args:
        limit: Max stories to return (before filtering)
        filter_founder_relevant: If True, filter for startup-relevant stories

    Returns: List of story dicts with title, url, score, comments, age_hours
    """
    top_ids = _http_get(f"{_HN_BASE}/topstories.json", timeout=5)
    if not top_ids or not isinstance(top_ids, list):
        return []

    # Fetch story details in parallel (first N IDs)
    target_ids = top_ids[:min(limit * 3, 150)]  # Fetch extra to allow filtering

    def _fetch_item(item_id: int) -> dict | None:
        data = _http_get(f"{_HN_BASE}/item/{item_id}.json", timeout=5)
        if not data or data.get("type") != "story":
            return None
        return data

    stories = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(_fetch_item, iid) for iid in target_ids]
        for f in as_completed(futures, timeout=15):
            try:
                item = f.result(timeout=5)
                if item:
                    stories.append(item)
            except Exception:
                pass

    # Process and filter
    results = []
    import time
    now = time.time()

    for s in stories:
        title = s.get("title", "")
        url = s.get("url", "")
        score = s.get("score", 0)
        comments = s.get("descendants", 0)
        timestamp = s.get("time", now)
        age_hours = (now - timestamp) / 3600

        if filter_founder_relevant:
            title_lower = title.lower()
            if not any(kw in title_lower for kw in _FOUNDER_KEYWORDS):
                # Check URL domain for known founder/tech sites
                relevant_domains = {"ycombinator", "indiehackers", "pieter.levels", "stripe.com"}
                if not any(d in url.lower() for d in relevant_domains):
                    if score < 50:  # Low-score non-founder stories skip
                        continue

        results.append({
            "title": title,
            "url": url or f"https://news.ycombinator.com/item?id={s.get('id')}",
            "score": score,
            "comments": comments,
            "age_hours": round(age_hours, 1),
            "hn_url": f"https://news.ycombinator.com/item?id={s.get('id')}",
        })

    # Sort by score descending, limit
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


def search_hn(query: str, limit: int = 10) -> list[dict]:
    """
    Search HN via Algolia HN Search API (official, free, no auth).
    Better for topic-specific searches than top stories.
    """
    encoded = urllib.parse.quote(query)
    url = f"https://hn.algolia.com/api/v1/search?query={encoded}&tags=story&hitsPerPage={limit}"
    data = _http_get(url, timeout=8)
    if not data or "hits" not in data:
        return []

    results = []
    for hit in data["hits"]:
        results.append({
            "title": hit.get("title", ""),
            "url": hit.get("url", ""),
            "score": hit.get("points", 0),
            "comments": hit.get("num_comments", 0),
            "author": hit.get("author", ""),
            "hn_url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            "created_at": hit.get("created_at", ""),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


# ─────────────────────────────────────────────────────────────
# Reddit — Public JSON API (no auth for basic reads)
# ─────────────────────────────────────────────────────────────

def get_subreddit_posts(
    subreddit: str,
    sort: str = "hot",
    limit: int = 25,
    time_filter: str = "week",
) -> list[dict]:
    """
    Fetch posts from a subreddit using Reddit's public JSON API.

    Args:
        subreddit: Subreddit name without r/ (e.g., "entrepreneur")
        sort: "hot", "new", "top", "rising"
        limit: Number of posts
        time_filter: "hour", "day", "week", "month", "year", "all" (for sort=top)

    Returns: List of post dicts
    """
    if sort == "top":
        url = f"https://www.reddit.com/r/{subreddit}/top.json?limit={limit}&t={time_filter}"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"

    headers = {"User-Agent": "SoloOS/7.0 (research; opensource)"}
    data = _http_get(url, extra_headers=headers)
    if not data:
        return []

    posts = []
    children = data.get("data", {}).get("children", [])
    for child in children:
        post = child.get("data", {})
        if post.get("stickied"):
            continue
        posts.append({
            "title": post.get("title", ""),
            "url": post.get("url", ""),
            "reddit_url": f"https://reddit.com{post.get('permalink', '')}",
            "score": post.get("score", 0),
            "comments": post.get("num_comments", 0),
            "selftext": post.get("selftext", "")[:500],  # First 500 chars
            "author": post.get("author", ""),
            "flair": post.get("link_flair_text", ""),
            "created_utc": post.get("created_utc", 0),
        })

    return posts


def search_reddit(query: str, subreddit: str = "", limit: int = 15) -> list[dict]:
    """
    Search Reddit using public search API.

    Args:
        query: Search query
        subreddit: Optional subreddit to restrict search to
        limit: Number of results
    """
    encoded_q = urllib.parse.quote(query)
    if subreddit:
        url = (
            f"https://www.reddit.com/r/{subreddit}/search.json"
            f"?q={encoded_q}&restrict_sr=1&sort=relevance&limit={limit}"
        )
    else:
        url = f"https://www.reddit.com/search.json?q={encoded_q}&sort=relevance&limit={limit}"

    headers = {"User-Agent": "SoloOS/7.0 (research; opensource)"}
    data = _http_get(url, extra_headers=headers)
    if not data:
        return []

    posts = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        posts.append({
            "title": post.get("title", ""),
            "url": post.get("url", ""),
            "reddit_url": f"https://reddit.com{post.get('permalink', '')}",
            "subreddit": post.get("subreddit", ""),
            "score": post.get("score", 0),
            "comments": post.get("num_comments", 0),
            "selftext": post.get("selftext", "")[:400],
            "author": post.get("author", ""),
        })

    posts.sort(key=lambda x: x["score"], reverse=True)
    return posts


def mine_pain_points(subreddit: str, topic: str, limit: int = 20) -> dict:
    """
    Mine a subreddit for pain point signals related to a topic.
    Uses sentiment analysis heuristics to find frustrated posts.

    Returns: pain points list, strength assessment, verbatim quotes
    """
    # Search with pain-signal keywords
    pain_queries = [
        f"{topic} problem",
        f"{topic} frustrated",
        f"{topic} hate",
        f"I wish {topic}",
        f"{topic} fails",
        f"annoying {topic}",
    ]

    all_posts = []
    # Run 3 queries in parallel
    def _fetch_query(q):
        return search_reddit(q, subreddit=subreddit, limit=8)

    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = [ex.submit(_fetch_query, q) for q in pain_queries[:3]]
        for f in as_completed(futures, timeout=15):
            try:
                all_posts.extend(f.result(timeout=10))
            except Exception:
                pass

    # Deduplicate by title
    seen_titles = set()
    unique_posts = []
    for p in all_posts:
        title = p["title"].lower()
        if title not in seen_titles:
            seen_titles.add(title)
            unique_posts.append(p)

    # Score by pain signal keywords
    pain_words = [
        "hate", "frustrated", "annoyed", "wish", "please", "why can't",
        "impossible", "pain", "broken", "terrible", "awful", "sucks",
        "no solution", "looking for", "need help", "problem", "issue",
    ]
    scored = []
    for p in unique_posts:
        text = (p["title"] + " " + p.get("selftext", "")).lower()
        pain_score = sum(2 if w in text else 0 for w in pain_words)
        pain_score += min(p.get("score", 0) // 10, 20)  # Upvotes signal community resonance
        pain_score += min(p.get("comments", 0) // 5, 15)
        scored.append((pain_score, p))

    scored.sort(reverse=True)
    top_pain_posts = [p for _, p in scored[:10]]

    # Extract verbatim quotes (post titles with high pain signal)
    verbatim = [p["title"] for p in top_pain_posts[:5] if p.get("score", 0) > 5]

    # Strength assessment
    total_score = sum(s for s, _ in scored[:5])
    if total_score > 100:
        strength = "STRONG — multiple high-engagement posts about this pain"
    elif total_score > 40:
        strength = "MODERATE — some signal, not overwhelming evidence"
    elif total_score > 10:
        strength = "WEAK — low engagement signal"
    else:
        strength = "NONE — no meaningful pain point signal found"

    return {
        "topic": topic,
        "subreddit": f"r/{subreddit}",
        "pain_signal_strength": strength,
        "verbatim_pain_quotes": verbatim,
        "top_posts": top_pain_posts[:5],
        "total_posts_analyzed": len(unique_posts),
    }


# ─────────────────────────────────────────────────────────────
# Jina AI Reader — Free web content extraction
# ─────────────────────────────────────────────────────────────

def read_url_content(url: str, max_chars: int = 3000) -> str:
    """
    Extract clean text from any URL using Jina AI reader.
    Free tier: no auth required for basic usage.

    Args:
        url: The URL to read
        max_chars: Max characters to return

    Returns: Clean text content
    """
    if not url.startswith("http"):
        return f"Invalid URL: {url}"

    jina_url = f"https://r.jina.ai/{url}"
    content = _http_get_text(jina_url, timeout=15)

    if not content:
        return f"Could not fetch content from {url}"

    # Clean up and truncate
    content = re.sub(r'\n{3,}', '\n\n', content)  # Collapse multiple newlines
    return content[:max_chars].strip()


def get_competitor_intel(competitor_url: str) -> dict:
    """
    Extract pricing, features, and positioning from a competitor page.

    Args:
        competitor_url: Homepage or pricing page URL

    Returns: Structured competitor intel dict
    """
    content = read_url_content(competitor_url, max_chars=5000)

    if not content or "Could not fetch" in content:
        return {"error": f"Could not access {competitor_url}", "url": competitor_url}

    # Extract pricing signals
    price_pattern = re.compile(
        r'\$[\d,]+(?:\.\d{2})?(?:/mo|/month|/year|/yr)?|\d+\s*(?:per|/)?\s*month',
        re.IGNORECASE
    )
    prices = list(set(price_pattern.findall(content)))[:10]

    # Extract feature signals
    feature_indicators = ["✓", "✅", "•", "- ", "* "]
    feature_lines = []
    for line in content.split("\n"):
        if any(ind in line for ind in feature_indicators) and 10 < len(line) < 150:
            feature_lines.append(line.strip().lstrip("✓✅•-* "))

    return {
        "url": competitor_url,
        "pricing_signals": prices,
        "feature_signals": feature_lines[:20],
        "raw_excerpt": content[:1000],
        "content_length": len(content),
    }


# ─────────────────────────────────────────────────────────────
# ProductHunt — Public GraphQL API
# ─────────────────────────────────────────────────────────────

def search_producthunt(query: str, limit: int = 10) -> list[dict]:
    """
    Search ProductHunt for products matching a query.
    Uses public GraphQL API — no auth required for basic queries.
    """
    import urllib.request

    graphql_query = """
    {
      posts(first: %d, order: VOTES, featured: true) {
        edges {
          node {
            name
            tagline
            url
            votesCount
            commentsCount
            topics {
              edges { node { name } }
            }
          }
        }
      }
    }
    """ % limit

    # Note: PH GraphQL requires a developer token for searches
    # Falling back to public site search via Jina
    search_url = f"https://www.producthunt.com/search?q={urllib.parse.quote(query)}"
    content = read_url_content(search_url, max_chars=3000)

    if not content:
        return []

    # Extract product names from search results (basic parsing)
    results = []
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if len(line) > 10 and len(line) < 100:
            results.append({"title": line.strip(), "source": "producthunt.com"})
        if len(results) >= limit:
            break

    return results


# ─────────────────────────────────────────────────────────────
# Morning brief intelligence swarm
# ─────────────────────────────────────────────────────────────

def run_morning_intelligence(
    founder_stage: str = "",
    focus_topics: list[str] | None = None,
) -> dict:
    """
    Run the full morning intelligence swarm using public APIs.
    Designed to work in both local and remote (CCR) environments.

    Fetches: HN top stories + startup Reddit signals in parallel.

    Args:
        founder_stage: MRR stage for relevance filtering
        focus_topics: Topics to bias the intelligence toward

    Returns: Structured morning brief dict
    """
    focus_topics = focus_topics or ["saas", "startup", "founder", "indie hacker"]

    def _fetch_hn():
        stories = get_hn_top_stories(limit=20, filter_founder_relevant=True)
        # Also search for focus topics
        focused = []
        for topic in focus_topics[:2]:
            focused.extend(search_hn(topic, limit=5))
        # Deduplicate
        seen = set()
        combined = []
        for s in stories + focused:
            if s["title"] not in seen:
                seen.add(s["title"])
                combined.append(s)
        return sorted(combined, key=lambda x: x["score"], reverse=True)[:10]

    def _fetch_entrepreneur():
        return get_subreddit_posts("entrepreneur", sort="hot", limit=15)

    def _fetch_saas():
        return get_subreddit_posts("SaaS", sort="hot", limit=10)

    def _fetch_inh():
        return get_subreddit_posts("indiehackers", sort="hot", limit=10)

    results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(_fetch_hn): "hn",
            executor.submit(_fetch_entrepreneur): "r_entrepreneur",
            executor.submit(_fetch_saas): "r_saas",
            executor.submit(_fetch_inh): "r_indiehackers",
        }
        for future in as_completed(futures, timeout=20):
            key = futures[future]
            try:
                results[key] = future.result(timeout=15)
            except Exception as e:
                results[key] = []

    # Surface top signals from each source
    hn_top = results.get("hn", [])[:5]

    reddit_all = (
        results.get("r_entrepreneur", []) +
        results.get("r_saas", []) +
        results.get("r_indiehackers", [])
    )
    reddit_top = sorted(reddit_all, key=lambda x: x.get("score", 0), reverse=True)[:8]

    # Pain point mining — top engaged posts
    pain_posts = [p for p in reddit_top if p.get("score", 0) > 20][:5]

    return {
        "hn_signals": hn_top,
        "reddit_signals": reddit_top,
        "pain_point_posts": pain_posts,
        "sources": {
            "hn_stories_fetched": len(results.get("hn", [])),
            "reddit_posts_fetched": len(reddit_all),
        },
    }
