"""
Update Blog Posts Script
Updates existing blog posts with new narrative content and cover images
"""

import os
import sys
import time
import requests
import importlib.util
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('WIX_API_KEY')
SITE_ID = os.getenv('WIX_SITE_ID')
ACCOUNT_ID = os.getenv('WIX_ACCOUNT_ID')

# Blog files to process
BLOG_FILES = [
    'blog_01_gpt52.py',
    'blog_02_ignite2025.py',
    'blog_03_claude_foundry.py',
    'blog_04_horizondb.py',
    'blog_05_copilot_agents.py',
    'blog_06_fabric_iq.py',
    'blog_07_ultra_disk.py',
    'blog_08_sql_server_2025.py',
    'blog_09_azure_boost.py',
    'blog_10_mistral_large_3.py',
    'blog_11_documentdb.py',
    'blog_12_sovereign_cloud.py',
    'blog_13_foundry_iq.py',
    'blog_14_cobalt_200.py',
    'blog_15_github_defender.py',
    'blog_16_azure_networking.py',
    'blog_17_redhat_partnership.py',
    'blog_18_azure_storage.py',
    'blog_19_gartner_leader.py',
    'blog_20_azure_pulse_december.py',
]

def load_blog_post(file_path):
    """Load BLOG_POST from a Python file"""
    spec = importlib.util.spec_from_file_location("blog_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.BLOG_POST

def get_posts():
    """Get all published blog posts"""
    url = 'https://www.wixapis.com/blog/v3/posts?paging.limit=50&sort=PUBLISHED_DATE_DESCENDING'
    headers = {
        'Authorization': API_KEY,
        'wix-site-id': SITE_ID,
        'wix-account-id': ACCOUNT_ID,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('posts', [])
    return []

def find_post_by_title(posts, title):
    """Find a post ID by matching title"""
    for post in posts:
        if post.get('title', '').lower() == title.lower():
            return post.get('id')
    return None

def build_rich_content(content):
    """Convert markdown-style content to Wix rich content format"""
    nodes = []
    paragraphs = content.split('\n\n')
    
    for para in paragraphs:
        if not para.strip():
            continue
            
        if para.startswith('## '):
            nodes.append({
                "type": "HEADING",
                "headingData": {"level": 2},
                "nodes": [{"type": "TEXT", "textData": {"text": para[3:].strip()}}]
            })
        elif para.startswith('### '):
            nodes.append({
                "type": "HEADING",
                "headingData": {"level": 3},
                "nodes": [{"type": "TEXT", "textData": {"text": para[4:].strip()}}]
            })
        elif para.startswith('---'):
            nodes.append({
                "type": "DIVIDER",
                "dividerData": {}
            })
        else:
            text_nodes = []
            parts = para.split('**')
            for i, part in enumerate(parts):
                if part:
                    if i % 2 == 1:
                        text_nodes.append({
                            "type": "TEXT",
                            "textData": {"text": part, "decorations": [{"type": "BOLD"}]}
                        })
                    else:
                        # Handle italic
                        italic_parts = part.split('*')
                        for j, ipart in enumerate(italic_parts):
                            if ipart:
                                if j % 2 == 1:
                                    text_nodes.append({
                                        "type": "TEXT",
                                        "textData": {"text": ipart, "decorations": [{"type": "ITALIC"}]}
                                    })
                                else:
                                    text_nodes.append({
                                        "type": "TEXT",
                                        "textData": {"text": ipart}
                                    })
            
            if text_nodes:
                nodes.append({"type": "PARAGRAPH", "nodes": text_nodes})
    
    return {"nodes": nodes}

def update_post(post_id, blog_post):
    """Update an existing blog post"""
    url = f'https://www.wixapis.com/blog/v3/posts/{post_id}'
    
    headers = {
        'Authorization': API_KEY,
        'wix-site-id': SITE_ID,
        'wix-account-id': ACCOUNT_ID,
        'Content-Type': 'application/json'
    }
    
    rich_content = build_rich_content(blog_post['content'])
    
    # Use existing Wix Media image (80s retro style)
    wix_media_image = {
        "wixMedia": {
            "image": {
                "id": "32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
                "url": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
                "height": 1024,
                "width": 1024
            }
        },
        "displayed": True,
        "custom": False
    }
    
    update_data = {
        "post": {
            "richContent": rich_content,
            "media": wix_media_image
        }
    }
    
    if blog_post.get('excerpt'):
        update_data["post"]["excerpt"] = blog_post['excerpt']
    
    response = requests.patch(url, headers=headers, json=update_data)
    
    if response.status_code in [200, 201]:
        return True
    else:
        print(f"  Error updating: {response.status_code}")
        print(f"  {response.text[:300]}")
        return False

def delete_and_recreate(blog_post):
    """Delete old post and create new one"""
    # Create as draft first
    url = 'https://www.wixapis.com/blog/v3/draft-posts'
    
    headers = {
        'Authorization': API_KEY,
        'wix-site-id': SITE_ID,
        'wix-account-id': ACCOUNT_ID,
        'Content-Type': 'application/json'
    }
    
    rich_content = build_rich_content(blog_post['content'])
    
    # Use existing Wix Media image (80s retro style)
    wix_media_image = {
        "wixMedia": {
            "image": {
                "id": "32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
                "url": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
                "height": 1024,
                "width": 1024
            }
        },
        "displayed": True,
        "custom": False
    }
    
    draft_post = {
        "title": blog_post['title'],
        "richContent": rich_content,
        "memberId": ACCOUNT_ID,
        "media": wix_media_image
    }
    
    if blog_post.get('excerpt'):
        draft_post["excerpt"] = blog_post['excerpt']
    
    data = {"draftPost": draft_post}
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        draft_id = response.json().get('draftPost', {}).get('id')
        if draft_id:
            # Publish the draft
            pub_url = f'https://www.wixapis.com/blog/v3/draft-posts/{draft_id}/publish'
            pub_response = requests.post(pub_url, headers=headers, json={})
            if pub_response.status_code in [200, 201]:
                return True
    
    print(f"  Error creating: {response.status_code}")
    print(f"  {response.text[:300]}")
    return False

def main():
    """Main function"""
    print("=" * 60)
    print("Updating Blog Posts with Narrative Style and Images")
    print("=" * 60)
    
    if not all([API_KEY, SITE_ID, ACCOUNT_ID]):
        print("Error: Missing environment variables!")
        return
    
    # Get existing posts
    print("\nFetching existing posts...")
    existing_posts = get_posts()
    print(f"Found {len(existing_posts)} existing posts")
    
    blogs_dir = os.path.join(os.path.dirname(__file__), 'blogs_v2')
    
    success_count = 0
    fail_count = 0
    
    for i, blog_file in enumerate(BLOG_FILES, 1):
        print(f"\n[{i}/20] Processing {blog_file}...")
        
        file_path = os.path.join(blogs_dir, blog_file)
        
        if not os.path.exists(file_path):
            print(f"  File not found: {file_path}")
            fail_count += 1
            continue
        
        try:
            blog_post = load_blog_post(file_path)
            title = blog_post['title']
            
            # Find existing post
            post_id = find_post_by_title(existing_posts, title)
            
            if post_id:
                print(f"  Found existing post, updating...")
                if update_post(post_id, blog_post):
                    print(f"  ✓ Updated: {title[:50]}...")
                    success_count += 1
                else:
                    fail_count += 1
            else:
                print(f"  Creating new post with image...")
                if delete_and_recreate(blog_post):
                    print(f"  ✓ Created: {title[:50]}...")
                    success_count += 1
                else:
                    fail_count += 1
            
            time.sleep(1.5)
            
        except Exception as e:
            print(f"  Error: {str(e)}")
            fail_count += 1
    
    print("\n" + "=" * 60)
    print("UPDATE COMPLETE")
    print("=" * 60)
    print(f"✓ Successful: {success_count}")
    print(f"✗ Failed: {fail_count}")

if __name__ == '__main__':
    main()
