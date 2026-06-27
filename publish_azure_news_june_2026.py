"""
Publish the 15 June 2026 Azure news posts in blogs_v3.

The script checks existing Wix post titles first, so re-running it will skip
posts that already exist instead of creating doubles.
"""

import importlib.util
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WIX_API_KEY")
SITE_ID = os.getenv("WIX_SITE_ID")
ACCOUNT_ID = os.getenv("WIX_ACCOUNT_ID")

BLOG_FILES = [
    "blog_26_postgresql_vs_code_performance.py",
    "blog_27_storage_modernization_migration.py",
    "blog_28_build_2026_leader_takeaways.py",
    "blog_29_claude_fable_5_foundry.py",
    "blog_30_microsoft_discovery_ga.py",
    "blog_31_fabric_databases_agentic_apps.py",
    "blog_32_enterprise_rl_openenv_foundry.py",
    "blog_33_foundry_local_edge_ai.py",
    "blog_34_document_translation_build.py",
    "blog_35_foundry_managed_compute.py",
    "blog_36_agent_optimizer_foundry.py",
    "blog_37_agent_memory_foundry.py",
    "blog_38_toolboxes_routines_foundry.py",
    "blog_39_enterprise_agent_distribution.py",
    "blog_40_content_understanding_build.py",
]

COVER_MEDIA = {
    "wixMedia": {
        "image": {
            "id": "32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
            "url": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
            "height": 1024,
            "width": 1024,
        }
    },
    "displayed": True,
    "custom": False,
}


def headers():
    return {
        "Authorization": API_KEY,
        "wix-site-id": SITE_ID,
        "wix-account-id": ACCOUNT_ID,
        "Content-Type": "application/json",
    }


def load_blog_post(file_path):
    spec = importlib.util.spec_from_file_location("blog_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.BLOG_POST


def build_rich_content(content):
    nodes = []

    for para in content.split("\n\n"):
        para = para.strip()
        if not para:
            continue

        if para.startswith("## "):
            nodes.append({
                "type": "HEADING",
                "headingData": {"level": 2},
                "nodes": [{"type": "TEXT", "textData": {"text": para[3:].strip()}}],
            })
        elif para.startswith("### "):
            nodes.append({
                "type": "HEADING",
                "headingData": {"level": 3},
                "nodes": [{"type": "TEXT", "textData": {"text": para[4:].strip()}}],
            })
        elif para.startswith("---"):
            nodes.append({"type": "DIVIDER", "dividerData": {}})
        else:
            text_nodes = []
            parts = para.split("**")
            for i, part in enumerate(parts):
                if not part:
                    continue
                if i % 2 == 1:
                    text_nodes.append({
                        "type": "TEXT",
                        "textData": {
                            "text": part,
                            "decorations": [{"type": "BOLD"}],
                        },
                    })
                else:
                    text_nodes.append({"type": "TEXT", "textData": {"text": part}})

            nodes.append({"type": "PARAGRAPH", "nodes": text_nodes})

    return {"nodes": nodes}


def get_existing_titles():
    response = requests.get(
        "https://www.wixapis.com/blog/v3/posts",
        headers=headers(),
        params={"paging.limit": 100},
    )
    if response.status_code != 200:
        print(f"Could not fetch existing posts: {response.status_code}")
        print(response.text[:500])
        return set()

    return {
        post.get("title", "").strip().lower()
        for post in response.json().get("posts", [])
        if post.get("title")
    }


def create_draft_post(blog_post):
    draft_post = {
        "title": blog_post["title"],
        "richContent": build_rich_content(blog_post["content"]),
        "memberId": ACCOUNT_ID,
        "media": COVER_MEDIA,
    }

    if blog_post.get("excerpt"):
        draft_post["excerpt"] = blog_post["excerpt"]

    response = requests.post(
        "https://www.wixapis.com/blog/v3/draft-posts",
        headers=headers(),
        json={"draftPost": draft_post},
    )

    if response.status_code not in (200, 201):
        print(f"Error creating draft: {response.status_code}")
        print(response.text[:500])
        return None

    return response.json().get("draftPost", {}).get("id")


def publish_draft(draft_id):
    response = requests.post(
        f"https://www.wixapis.com/blog/v3/draft-posts/{draft_id}/publish",
        headers=headers(),
        json={},
    )

    if response.status_code not in (200, 201):
        print(f"Error publishing draft: {response.status_code}")
        print(response.text[:500])
        return False

    return True


def main():
    if not all([API_KEY, SITE_ID, ACCOUNT_ID]):
        print("Error: Missing WIX_API_KEY, WIX_SITE_ID, or WIX_ACCOUNT_ID.")
        return

    blogs_dir = os.path.join(os.path.dirname(__file__), "blogs_v3")
    existing_titles = get_existing_titles()

    published = 0
    skipped = 0
    failed = 0

    for index, blog_file in enumerate(BLOG_FILES, 1):
        file_path = os.path.join(blogs_dir, blog_file)
        blog_post = load_blog_post(file_path)
        title_key = blog_post["title"].strip().lower()

        print(f"[{index}/{len(BLOG_FILES)}] {blog_post['title']}")

        if title_key in existing_titles:
            print("  Skipping: title already exists in Wix.")
            skipped += 1
            continue

        draft_id = create_draft_post(blog_post)
        if not draft_id:
            failed += 1
            continue

        if publish_draft(draft_id):
            print("  Published.")
            existing_titles.add(title_key)
            published += 1
        else:
            failed += 1

        time.sleep(2)

    print("\nPublishing complete")
    print(f"Published: {published}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()

