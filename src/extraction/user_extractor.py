"""
User Extractor module.
Handles fetching user profiles and search functionality from GitHub API.
"""
import time
import requests

SEARCH_URL = "https://api.github.com/search/users"
USER_URL   = "https://api.github.com/users/{}"
API_VERSION = "2022-11-28"

def get_headers(token: str) -> dict:
    return {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
        "Authorization": f"Bearer {token}",
    }

def search_users_by_location(token: str, location: str, max_users: int = 1000) -> list:
    """Return up to max_users login names from the search API (max 10 pages)."""
    headers = get_headers(token)
    logins  = []

    for page in range(1, 11):          # pages 1–10 → max 1000 results
        if len(logins) >= max_users:
            break

        print(f"Search page {page} – collected {len(logins)} so far …")
        r = requests.get(
            SEARCH_URL,
            headers=headers,
            params={"q": f"location:{location}", "per_page": 100, "page": page},
        )

        if r.status_code == 403:
            print("Rate limit hit during search, sleeping 60 s …")
            time.sleep(60)
            r = requests.get(SEARCH_URL, headers=headers,
                             params={"q": f"location:{location}", "per_page": 100, "page": page})

        if r.status_code != 200:
            print(f"Search error {r.status_code}: {r.text}")
            break

        items = r.json().get("items", [])
        if not items:
            break

        for item in items:
            logins.append(item["login"])
            if len(logins) >= max_users:
                break

    return logins[:max_users]

def fetch_user_profile(token: str, login: str) -> dict:
    """Fetch a user's full public profile via /users/{login}."""
    r = requests.get(USER_URL.format(login), headers=get_headers(token))

    if r.status_code == 403:
        print(f"Rate limit hit fetching @{login}, sleeping 60 s …")
        time.sleep(60)
        return fetch_user_profile(token, login)   # retry once

    if r.status_code != 200:
        print(f"Could not fetch @{login}: {r.status_code}")
        return None

    return r.json()
