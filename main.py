import requests
import json
import time
import os
import logging
from bs4 import BeautifulSoup

# -------------- Configuration --------------
API_URL = "https://leetcode.com/graphql"
OUTPUT_FILE = "leetcode_questions.json"
DESIRED_COUNT = 75    # Adjust to fetch ~75 to 100 questions
PAGE_SIZE = 50        # Number of questions per request

# Insert your logged-in session cookie and CSRF token here
HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
    "User-Agent": "Mozilla/5.0",
    "Cookie": "LEETCODE_SESSION=<YOUR_SESSION>; csrftoken=<YOUR_CSRF_TOKEN>",
    "x-csrftoken": "<YOUR_CSRF_TOKEN>"
}

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# -------------- Queries --------------
QUERY_LIST = """
query problemsetQuestionListV2($limit: Int, $skip: Int) {
  problemsetQuestionListV2(limit: $limit, skip: $skip) {
    questions {
      titleSlug
      title
      difficulty
      __typename
    }
  }
}
"""

QUERY_DETAIL = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    content
    topicTags { name }
    questionId
    difficulty
    title
    __typename
  }
}
"""

# -------------- Helpers --------------
def html_to_text(html):
    return BeautifulSoup(html or "", "html.parser").get_text(separator="\n").strip()

# ------------- Fetch Slugs -------------
def fetch_slugs(limit=DESIRED_COUNT):
    slugs = []
    skip = 0

    while len(slugs) < limit:
        vars = {"limit": PAGE_SIZE, "skip": skip}
        resp = requests.post(API_URL, json={"query": QUERY_LIST, "variables": vars}, headers=HEADERS)
        logging.info(f"Fetching slugs batch (skip={skip})... status {resp.status_code}")

        try:
            data = resp.json()
            logging.debug("Response JSON:\n" + json.dumps(data, indent=2))
        except Exception as e:
            logging.error("Invalid JSON response:", e)
            break

        block = data.get("data", {}).get("problemsetQuestionListV2", {}).get("questions")
        if not block:
            logging.warning("Empty slug batch. Stopping.")
            break

        for q in block:
            slugs.append(q["titleSlug"])
            if len(slugs) >= limit:
                break

        skip += PAGE_SIZE
        time.sleep(0.8)

    return slugs

# ------------- Fetch Details -------------
def fetch_detail(slug):
    resp = requests.post(API_URL, json={"query": QUERY_DETAIL, "variables": {"titleSlug": slug}}, headers=HEADERS)
    if resp.status_code != 200:
        logging.error(f"Failed to fetch detail for {slug} ({resp.status_code})")
        return None

    data = resp.json().get("data", {}).get("question")
    if not data:
        logging.warning(f"No detail data for {slug}")
        return None

    return {
        "id": slug,
        "title": data.get("title"),
        "difficulty": data.get("difficulty"),
        "description": html_to_text(data.get("content")),
        "tags": [tag["name"] for tag in data.get("topicTags", [])],
        "url": f"https://leetcode.com/problems/{slug}/"
    }

# -------------- Main Logic --------------
def main():
    logging.info("Starting LeetCode scraper...")

    questions = []
    slugs = fetch_slugs()

    logging.info(f"Fetched {len(slugs)} slugs, now retrieving details...")
    for idx, slug in enumerate(slugs, 1):
        logging.info(f"[{idx}/{len(slugs)}] {slug}")
        q = fetch_detail(slug)
        if q:
            questions.append(q)
        time.sleep(0.5)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    logging.info(f"Saved {len(questions)} questions to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
