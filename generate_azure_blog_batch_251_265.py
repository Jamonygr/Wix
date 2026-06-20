"""
Generate Azure blog posts 251-265.

Uses the Azure Updates feed, skips local and live Wix duplicates, and assigns
the same shared Wix cover image used by the previous blog posts.
"""

import os
import sys

import requests
from dotenv import load_dotenv

sys.dont_write_bytecode = True

from generate_azure_blog_batch_106_205 import (  # noqa: E402
    AZURE_UPDATES_API,
    ROOT,
    ascii_clean,
    existing_local_context,
    news_post,
    news_title,
    normalize,
    parse_date,
    slugify,
    title_core,
    write_post,
)


START = 251
COUNT = 15
FETCH_PAGE_SIZE = 100
FETCH_LIMIT = 2000
COMMON_COVER_IMAGE = "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png"


def wix_headers():
    load_dotenv(dotenv_path=ROOT / ".env")
    api_key = os.getenv("WIX_API_KEY")
    site_id = os.getenv("WIX_SITE_ID")
    account_id = os.getenv("WIX_ACCOUNT_ID")

    if not all([api_key, site_id, account_id]):
        raise RuntimeError("Missing Wix environment variables for live duplicate check.")

    return {
        "Authorization": api_key,
        "wix-site-id": site_id,
        "wix-account-id": account_id,
        "Content-Type": "application/json",
    }


def fetch_live_title_context():
    titles = []
    offset = 0
    limit = 100

    while True:
        response = requests.get(
            "https://www.wixapis.com/blog/v3/posts",
            headers=wix_headers(),
            params={"paging.limit": limit, "paging.offset": offset},
            timeout=45,
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to fetch live Wix posts ({response.status_code}): "
                f"{response.text[:300]}"
            )

        posts = response.json().get("posts", [])
        for post in posts:
            title = ascii_clean(post.get("title", "")).strip()
            if title:
                titles.append(title)

        if len(posts) < limit:
            break

        offset += len(posts)

    return set(titles), " ".join(normalize(title) for title in titles)


def fetch_candidate_news_items():
    items = []
    skip = 0

    while skip < FETCH_LIMIT:
        response = requests.get(
            AZURE_UPDATES_API,
            params={
                "$count": "true",
                "includeFacets": "true",
                "top": str(FETCH_PAGE_SIZE),
                "skip": str(skip),
                "orderby": "modified desc",
            },
            timeout=45,
        )
        response.raise_for_status()
        page = response.json().get("value", [])

        if not page:
            break

        items.extend(page)
        skip += len(page)

        if len(page) < FETCH_PAGE_SIZE:
            break

    return items


def select_news_items(count):
    used_ids, local_text = existing_local_context()
    live_titles, live_text = fetch_live_title_context()
    combined_text = f"{local_text} {live_text}"
    selected = []
    skipped = []

    for item in fetch_candidate_news_items():
        item_id = str(item.get("id", "")).strip()
        official_title = ascii_clean(item.get("title", ""))
        generated_title = news_title(item)
        official_core = title_core(official_title)
        generated_core = title_core(generated_title)

        if not item_id or item_id in used_ids:
            skipped.append((item_id, "source id", official_title))
            continue

        if not official_title or official_title.lower().startswith("test"):
            skipped.append((item_id, "empty/test", official_title))
            continue

        if generated_title in live_titles:
            skipped.append((item_id, "live title", official_title))
            continue

        if official_core and len(official_core) > 8 and official_core in combined_text:
            skipped.append((item_id, "existing core phrase", official_title))
            continue

        if generated_core and len(generated_core) > 8 and generated_core in live_text:
            skipped.append((item_id, "live generated core phrase", official_title))
            continue

        selected.append(item)
        if len(selected) == count:
            break

    if len(selected) < count:
        raise RuntimeError(f"Only found {len(selected)} usable Azure news items.")

    return selected, skipped, len(live_titles)


def main():
    selected, skipped, live_count = select_news_items(COUNT)
    written = []

    for offset, item in enumerate(selected):
        number = START + offset
        post = news_post(item)
        post["coverImage"] = COMMON_COVER_IMAGE

        slug = slugify(post["title"])
        written.append(write_post(number, slug, post))

    print(f"Generated {len(written)} blog files.")
    print(f"News posts: {START}-{START + COUNT - 1}")
    print(f"Live Wix titles checked: {live_count}")
    print(f"Skipped existing/local/live Azure update candidates: {len(skipped)}")
    for path, item in zip(written, selected):
        print(
            f"  {path.name}: {item.get('id')} | {parse_date(item.get('modified'))} | "
            f"{news_title(item)}"
        )


if __name__ == "__main__":
    main()
