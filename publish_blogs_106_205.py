"""
Publish numbered Azure blogs to Wix.

Discovers generated posts in the blogs folder, creates Wix draft posts, then
publishes them. Existing published titles are skipped.
"""

import argparse
import importlib.util
import os
import re
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
BLOGS_DIR = ROOT / "blogs"
POST_PATTERN = re.compile(r"^blog_(\d{3})_.*\.py$")

load_dotenv()
API_KEY = os.getenv("WIX_API_KEY")
SITE_ID = os.getenv("WIX_SITE_ID")
ACCOUNT_ID = os.getenv("WIX_ACCOUNT_ID")


def headers():
    return {
        "Authorization": API_KEY,
        "wix-site-id": SITE_ID,
        "wix-account-id": ACCOUNT_ID,
        "Content-Type": "application/json",
    }


def is_http_url(value):
    return isinstance(value, str) and value.startswith(("http://", "https://"))


def is_wixstatic_media_url(value):
    return is_http_url(value) and "wixstatic.com" in value and "/media/" in value


def cover_mime_type(url):
    normalized = url.lower().split("?", 1)[0]
    if normalized.endswith((".jpg", ".jpeg")):
        return "image/jpeg"
    if normalized.endswith(".webp"):
        return "image/webp"
    if normalized.endswith(".png") or "/png" in normalized:
        return "image/png"
    return None


def cover_display_name(title, url):
    extension = ".png"
    mime_type = cover_mime_type(url)
    if mime_type == "image/jpeg":
        extension = ".jpg"
    elif mime_type == "image/webp":
        extension = ".webp"

    safe_title = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_").lower()
    safe_title = safe_title[:64] or "azure_blog_cover"
    return f"{safe_title}{extension}"


def import_external_cover_image(cover_image, title):
    if not cover_image or not is_http_url(cover_image) or is_wixstatic_media_url(cover_image):
        return None

    payload = {
        "url": cover_image,
        "displayName": cover_display_name(title, cover_image),
        "parentFolderId": "media-root",
    }
    mime_type = cover_mime_type(cover_image)
    if mime_type:
        payload["mimeType"] = mime_type

    print("Importing external cover image to Wix Media Manager...")
    response = requests.post(
        "https://www.wixapis.com/site-media/v1/files/import",
        headers=headers(),
        json=payload,
        timeout=90,
    )

    if response.status_code not in [200, 201]:
        print(f"Warning: failed to import cover image ({response.status_code}).")
        print(response.text[:500])
        return None

    file_info = response.json().get("file", {})
    media_id = file_info.get("id") or file_info.get("_id")
    media_url = file_info.get("url") or file_info.get("fileUrl") or cover_image

    if not media_id:
        print("Warning: Wix image import succeeded but no media ID was returned.")
        return None

    return {"id": media_id, "url": media_url}


def discover_blog_files(start, end):
    files = []
    for path in BLOGS_DIR.glob("blog_*.py"):
        match = POST_PATTERN.match(path.name)
        if not match:
            continue
        number = int(match.group(1))
        if start <= number <= end:
            files.append((number, path))
    return [path for _, path in sorted(files)]


def load_blog_post(file_path):
    spec = importlib.util.spec_from_file_location("blog_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.BLOG_POST


def fetch_existing_titles():
    all_titles = set()
    offset = 0
    limit = 100
    url = "https://www.wixapis.com/blog/v3/posts"

    while True:
        response = requests.get(
            url,
            headers=headers(),
            params={"paging.limit": limit, "paging.offset": offset},
            timeout=45,
        )
        if response.status_code != 200:
            print(f"Warning: failed to fetch existing posts ({response.status_code}).")
            print(response.text[:500])
            return all_titles

        posts = response.json().get("posts", [])
        for post in posts:
            title = post.get("title", "").strip()
            if title:
                all_titles.add(title)

        if len(posts) < limit:
            break
        offset += len(posts)

    return all_titles


def paragraph_to_text_nodes(paragraph):
    text_nodes = []
    for index, part in enumerate(paragraph.split("**")):
        if not part:
            continue
        if index % 2 == 1:
            text_nodes.append({
                "type": "TEXT",
                "textData": {
                    "text": part,
                    "decorations": [{"type": "BOLD"}],
                },
            })
        else:
            text_nodes.append({
                "type": "TEXT",
                "textData": {"text": part},
            })
    return text_nodes


def rich_content_nodes(title, content, cover_image):
    nodes = []

    if cover_image and is_http_url(cover_image):
        nodes.append({
            "type": "IMAGE",
            "id": "cover-img",
            "nodes": [],
            "imageData": {
                "containerData": {
                    "width": {"size": "FULL_WIDTH"},
                    "alignment": "CENTER",
                },
                "image": {
                    "src": {"url": cover_image},
                    "width": 1200,
                    "height": 675,
                },
                "altText": title,
            },
        })

    for paragraph in content.split("\n\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if paragraph.startswith("## "):
            nodes.append({
                "type": "HEADING",
                "headingData": {"level": 2},
                "nodes": [{"type": "TEXT", "textData": {"text": paragraph[3:].strip()}}],
            })
            continue

        if paragraph.startswith("### "):
            nodes.append({
                "type": "HEADING",
                "headingData": {"level": 3},
                "nodes": [{"type": "TEXT", "textData": {"text": paragraph[4:].strip()}}],
            })
            continue

        text_nodes = paragraph_to_text_nodes(paragraph)
        if text_nodes:
            nodes.append({"type": "PARAGRAPH", "nodes": text_nodes})

    return nodes


def create_draft_post(blog_post):
    title = blog_post["title"]
    cover_image = blog_post.get("coverImage")
    imported_cover = import_external_cover_image(cover_image, title)
    rich_cover_image = imported_cover["url"] if imported_cover else cover_image
    draft_post = {
        "title": title,
        "richContent": {
            "nodes": rich_content_nodes(title, blog_post["content"], rich_cover_image),
        },
        "memberId": ACCOUNT_ID,
    }

    if blog_post.get("excerpt"):
        draft_post["excerpt"] = blog_post["excerpt"]

    if is_wixstatic_media_url(rich_cover_image):
        media_id = rich_cover_image.split("/media/", 1)[1]
        draft_post["media"] = {
            "wixMedia": {
                "image": {
                    "id": media_id,
                    "url": rich_cover_image,
                    "height": 1024,
                    "width": 1024,
                }
            },
            "displayed": True,
            "custom": False,
        }
    elif imported_cover:
        draft_post["media"] = {
            "wixMedia": {
                "image": {
                    "id": imported_cover["id"],
                    "url": imported_cover["url"],
                    "height": 675,
                    "width": 1200,
                }
            },
            "displayed": True,
            "custom": False,
        }

    response = requests.post(
        "https://www.wixapis.com/blog/v3/draft-posts",
        headers=headers(),
        json={"draftPost": draft_post},
        timeout=60,
    )
    if response.status_code in [200, 201]:
        return response.json()

    print(f"Error creating draft: {response.status_code}")
    print(response.text[:700])
    return None


def publish_draft(draft_post_id):
    response = requests.post(
        f"https://www.wixapis.com/blog/v3/draft-posts/{draft_post_id}/publish",
        headers=headers(),
        json={},
        timeout=60,
    )
    if response.status_code in [200, 201]:
        return response.json()

    print(f"Error publishing: {response.status_code}")
    print(response.text[:700])
    return None


def publish_blog(blog_post):
    print(f"Creating draft: {blog_post['title'][:70]}...")
    draft_response = create_draft_post(blog_post)
    if not draft_response:
        return False

    draft_id = draft_response.get("draftPost", {}).get("id")
    if not draft_id:
        print("Failed to get draft ID")
        return False

    print(f"Publishing draft {draft_id}...")
    publish_response = publish_draft(draft_id)
    if publish_response:
        post = publish_response.get("post", {})
        print(f"Published: {post.get('title', 'Unknown')}")
        return True

    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=106)
    parser.add_argument("--end", type=int, default=205)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--delay", type=float, default=1.25)
    args = parser.parse_args()

    if not all([API_KEY, SITE_ID, ACCOUNT_ID]):
        print("Error: Missing environment variables.")
        print(f"API_KEY: {'Set' if API_KEY else 'Missing'}")
        print(f"SITE_ID: {'Set' if SITE_ID else 'Missing'}")
        print(f"ACCOUNT_ID: {'Set' if ACCOUNT_ID else 'Missing'}")
        return 1

    blog_files = discover_blog_files(args.start, args.end)
    if args.limit:
        blog_files = blog_files[: args.limit]

    print("=" * 60)
    print(f"Publishing Azure Blogs {args.start}-{args.end}")
    print("=" * 60)
    print(f"Number of files selected: {len(blog_files)}")

    if not blog_files:
        print("No blog files found.")
        return 1

    if args.dry_run:
        for path in blog_files:
            print(path.relative_to(ROOT))
        return 0

    if not args.yes:
        confirm = input(f"Publish {len(blog_files)} blogs to Wix? Type yes: ")
        if confirm.lower() != "yes":
            print("Aborted.")
            return 0

    existing_titles = fetch_existing_titles()
    print(f"Existing published titles loaded: {len(existing_titles)}")

    success_count = 0
    fail_count = 0
    skip_count = 0

    for index, file_path in enumerate(blog_files, 1):
        print(f"\n[{index}/{len(blog_files)}] Processing {file_path.name}...")
        try:
            blog_post = load_blog_post(file_path)
            title = blog_post["title"].strip()
            if title in existing_titles:
                print(f"Skipping existing published post: {title}")
                skip_count += 1
                continue

            if publish_blog(blog_post):
                success_count += 1
                existing_titles.add(title)
            else:
                fail_count += 1

            if index < len(blog_files):
                print(f"Waiting {args.delay} seconds...")
                time.sleep(args.delay)
        except Exception as exc:
            print(f"Error: {exc}")
            fail_count += 1

    print("\n" + "=" * 60)
    print("PUBLISHING COMPLETE")
    print("=" * 60)
    print(f"Successful: {success_count}")
    print(f"Skipped: {skip_count}")
    print(f"Failed: {fail_count}")
    print(f"Total: {success_count + skip_count + fail_count}")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
