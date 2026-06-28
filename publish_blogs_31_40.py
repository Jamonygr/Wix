"""
Publish Blogs 31-40 to Wix
Publishes the 10 latest Azure blog posts from the blogs folder.
"""

import os
import time
import requests
import importlib.util
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('WIX_API_KEY')
SITE_ID = os.getenv('WIX_SITE_ID')
ACCOUNT_ID = os.getenv('WIX_ACCOUNT_ID')

BLOG_FILES = [
    'blog_31_log_analytics_retry_bin.py',
    'blog_32_storage_mover_private_s3.py',
    'blog_33_postgresql_elastic_clusters_iac.py',
    'blog_34_postgresql_grafana_dashboards.py',
    'blog_35_postgresql_cmk_premium_ssdv2.py',
    'blog_36_azure_sre_agent_ga.py',
    'blog_37_mssql_vscode_query_profiler.py',
    'blog_38_azure_policy_faster_enforcement.py',
    'blog_39_azure_firewall_draft_deploy.py',
    'blog_40_databricks_network_config.py',
]


def load_blog_post(file_path):
    """Load BLOG_POST from a Python file."""
    spec = importlib.util.spec_from_file_location("blog_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.BLOG_POST


def fetch_existing_titles():
    """Fetch currently published Wix blog titles."""
    url = 'https://www.wixapis.com/blog/v3/posts'

    headers = {
        'Authorization': API_KEY,
        'wix-site-id': SITE_ID,
        'wix-account-id': ACCOUNT_ID,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Warning: failed to fetch existing posts ({response.status_code}).")
        print(response.text[:300])
        return set()

    data = response.json()
    posts = data.get('posts', [])
    return {post.get('title', '').strip() for post in posts if post.get('title')}


def create_draft_post(title, content, excerpt=None, cover_image=None):
    """Create a draft blog post via Wix API."""
    url = 'https://www.wixapis.com/blog/v3/draft-posts'

    headers = {
        'Authorization': API_KEY,
        'wix-site-id': SITE_ID,
        'wix-account-id': ACCOUNT_ID,
        'Content-Type': 'application/json'
    }

    nodes = []

    if cover_image and 'wixstatic.com' in cover_image:
        nodes.append({
            "type": "IMAGE",
            "id": "cover-img",
            "nodes": [],
            "imageData": {
                "containerData": {
                    "width": {
                        "size": "FULL_WIDTH"
                    },
                    "alignment": "CENTER"
                },
                "image": {
                    "src": {
                        "url": cover_image
                    },
                    "width": 1200,
                    "height": 675
                },
                "altText": title
            }
        })

    paragraphs = content.split('\n\n')

    for para in paragraphs:
        if not para.strip():
            continue

        if para.startswith('## '):
            nodes.append({
                "type": "HEADING",
                "headingData": {"level": 2},
                "nodes": [{
                    "type": "TEXT",
                    "textData": {"text": para[3:].strip()}
                }]
            })
        elif para.startswith('### '):
            nodes.append({
                "type": "HEADING",
                "headingData": {"level": 3},
                "nodes": [{
                    "type": "TEXT",
                    "textData": {"text": para[4:].strip()}
                }]
            })
        elif para.startswith('**') and para.endswith('**'):
            nodes.append({
                "type": "PARAGRAPH",
                "nodes": [{
                    "type": "TEXT",
                    "textData": {
                        "text": para[2:-2],
                        "decorations": [{"type": "BOLD"}]
                    }
                }]
            })
        else:
            text_nodes = []
            parts = para.split('**')
            for i, part in enumerate(parts):
                if not part:
                    continue
                if i % 2 == 1:
                    text_nodes.append({
                        "type": "TEXT",
                        "textData": {
                            "text": part,
                            "decorations": [{"type": "BOLD"}]
                        }
                    })
                else:
                    text_nodes.append({
                        "type": "TEXT",
                        "textData": {"text": part}
                    })

            if text_nodes:
                nodes.append({
                    "type": "PARAGRAPH",
                    "nodes": text_nodes
                })

    draft_post = {
        "title": title,
        "richContent": {"nodes": nodes},
        "memberId": ACCOUNT_ID
    }

    if excerpt:
        draft_post["excerpt"] = excerpt

    if cover_image and 'wixstatic.com' in cover_image:
        media_id = cover_image.split('/media/')[-1] if '/media/' in cover_image else None
        if media_id:
            draft_post["media"] = {
                "wixMedia": {
                    "image": {
                        "id": media_id,
                        "url": cover_image,
                        "height": 1024,
                        "width": 1024
                    }
                },
                "displayed": True,
                "custom": False
            }

    response = requests.post(url, headers=headers, json={"draftPost": draft_post})

    if response.status_code in [200, 201]:
        return response.json()

    print(f"Error creating draft: {response.status_code}")
    print(response.text[:500])
    return None


def publish_draft(draft_post_id):
    """Publish a draft blog post."""
    url = f'https://www.wixapis.com/blog/v3/draft-posts/{draft_post_id}/publish'

    headers = {
        'Authorization': API_KEY,
        'wix-site-id': SITE_ID,
        'wix-account-id': ACCOUNT_ID,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json={})

    if response.status_code in [200, 201]:
        return response.json()

    print(f"Error publishing: {response.status_code}")
    print(response.text[:500])
    return None


def publish_blog(blog_post):
    """Create and publish a single blog post."""
    print(f"Creating draft: {blog_post['title'][:60]}...")

    draft_response = create_draft_post(
        title=blog_post['title'],
        content=blog_post['content'],
        excerpt=blog_post.get('excerpt'),
        cover_image=blog_post.get('coverImage')
    )

    if not draft_response:
        return False

    draft_id = draft_response.get('draftPost', {}).get('id')
    if not draft_id:
        print("Failed to get draft ID")
        return False

    print(f"Publishing draft {draft_id}...")
    publish_response = publish_draft(draft_id)

    if publish_response:
        post = publish_response.get('post', {})
        print(f"Published: {post.get('title', 'Unknown')}")
        return True

    return False


def main():
    """Publish blogs 31-40."""
    print("=" * 60)
    print("Publishing Azure Blogs 31-40")
    print("=" * 60)

    if not all([API_KEY, SITE_ID, ACCOUNT_ID]):
        print("Error: Missing environment variables!")
        print(f"API_KEY: {'Set' if API_KEY else 'Missing'}")
        print(f"SITE_ID: {'Set' if SITE_ID else 'Missing'}")
        print(f"ACCOUNT_ID: {'Set' if ACCOUNT_ID else 'Missing'}")
        return

    print(f"\nSite ID: {SITE_ID}")
    print(f"Number of blogs to publish: {len(BLOG_FILES)}")

    confirm = input("\nDo you want to publish blogs 31-40? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Aborted.")
        return

    blogs_dir = os.path.join(os.path.dirname(__file__), 'blogs')

    success_count = 0
    fail_count = 0
    skip_count = 0
    existing_titles = fetch_existing_titles()

    for i, blog_file in enumerate(BLOG_FILES, 1):
        print(f"\n[{i}/{len(BLOG_FILES)}] Processing {blog_file}...")
        file_path = os.path.join(blogs_dir, blog_file)

        if not os.path.exists(file_path):
            print(f"  ✗ File not found: {file_path}")
            fail_count += 1
            continue

        try:
            blog_post = load_blog_post(file_path)
            if blog_post['title'].strip() in existing_titles:
                print(f"  Skipping existing published post: {blog_post['title']}")
                skip_count += 1
                continue

            if publish_blog(blog_post):
                success_count += 1
                existing_titles.add(blog_post['title'].strip())
            else:
                fail_count += 1

            if i < len(BLOG_FILES):
                print("  Waiting 2 seconds...")
                time.sleep(2)

        except Exception as exc:
            print(f"  Error: {exc}")
            fail_count += 1

    print("\n" + "=" * 60)
    print("PUBLISHING COMPLETE")
    print("=" * 60)
    print(f"Successful: {success_count}")
    print(f"Skipped: {skip_count}")
    print(f"Failed: {fail_count}")
    print(f"Total: {success_count + fail_count}")


if __name__ == '__main__':
    main()
