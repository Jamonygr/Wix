"""
Batch Blog Publisher
Publishes all 20 blog posts to Wix
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

# Blog files in order
BLOG_FILES = [
    'blog_01_gpt52.py',
    'blog_02_ignite2025.py',
    'blog_03_claude_foundry.py',
    'blog_04_horizondb.py',
    'blog_05_azure_copilot_agents.py',
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

def create_draft_post(title, content, excerpt=None, tags=None):
    """Create a draft blog post via Wix API"""
    url = 'https://www.wixapis.com/blog/v3/draft-posts'
    
    headers = {
        'Authorization': API_KEY,
        'wix-site-id': SITE_ID,
        'wix-account-id': ACCOUNT_ID,
        'Content-Type': 'application/json'
    }
    
    # Build rich content from plain text
    nodes = []
    paragraphs = content.split('\n\n')
    
    for para in paragraphs:
        if not para.strip():
            continue
            
        if para.startswith('## '):
            # H2 heading
            nodes.append({
                "type": "HEADING",
                "headingData": {"level": 2},
                "nodes": [{
                    "type": "TEXT",
                    "textData": {"text": para[3:].strip()}
                }]
            })
        elif para.startswith('### '):
            # H3 heading
            nodes.append({
                "type": "HEADING",
                "headingData": {"level": 3},
                "nodes": [{
                    "type": "TEXT",
                    "textData": {"text": para[4:].strip()}
                }]
            })
        elif para.startswith('**') and para.endswith('**'):
            # Bold paragraph
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
            # Regular paragraph - handle inline bold
            text_nodes = []
            parts = para.split('**')
            for i, part in enumerate(parts):
                if part:
                    if i % 2 == 1:  # Bold text
                        text_nodes.append({
                            "type": "TEXT",
                            "textData": {
                                "text": part,
                                "decorations": [{"type": "BOLD"}]
                            }
                        })
                    else:  # Regular text
                        text_nodes.append({
                            "type": "TEXT",
                            "textData": {"text": part}
                        })
            
            if text_nodes:
                nodes.append({
                    "type": "PARAGRAPH",
                    "nodes": text_nodes
                })
    
    rich_content = {
        "nodes": nodes
    }
    
    draft_post = {
        "title": title,
        "richContent": rich_content,
        "memberId": ACCOUNT_ID
    }
    
    if excerpt:
        draft_post["excerpt"] = excerpt
    
    data = {"draftPost": draft_post}
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"Error creating draft: {response.status_code}")
        print(response.text[:500])
        return None

def publish_draft(draft_post_id):
    """Publish a draft blog post"""
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
    else:
        print(f"Error publishing: {response.status_code}")
        print(response.text[:500])
        return None

def publish_blog(blog_post):
    """Create and publish a blog post"""
    print(f"Creating draft: {blog_post['title'][:50]}...")
    
    draft_response = create_draft_post(
        title=blog_post['title'],
        content=blog_post['content'],
        excerpt=blog_post.get('excerpt'),
        tags=blog_post.get('tags')
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
        print(f"✓ Published: {post.get('title', 'Unknown')}")
        return True
    else:
        return False

def main():
    """Main function to publish all blogs"""
    print("=" * 60)
    print("Batch Blog Publisher for BeyondCloudwithChriz")
    print("=" * 60)
    
    # Check environment variables
    if not all([API_KEY, SITE_ID, ACCOUNT_ID]):
        print("Error: Missing environment variables!")
        print(f"API_KEY: {'Set' if API_KEY else 'Missing'}")
        print(f"SITE_ID: {'Set' if SITE_ID else 'Missing'}")
        print(f"ACCOUNT_ID: {'Set' if ACCOUNT_ID else 'Missing'}")
        return
    
    print(f"\nSite ID: {SITE_ID}")
    print(f"Number of blogs to publish: {len(BLOG_FILES)}")
    
    # Confirm before proceeding
    confirm = input("\nDo you want to publish all 20 blogs? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Aborted.")
        return
    
    blogs_dir = os.path.join(os.path.dirname(__file__), 'blogs')
    
    success_count = 0
    fail_count = 0
    
    for i, blog_file in enumerate(BLOG_FILES, 1):
        print(f"\n[{i}/{len(BLOG_FILES)}] Processing {blog_file}...")
        
        file_path = os.path.join(blogs_dir, blog_file)
        
        if not os.path.exists(file_path):
            print(f"  ✗ File not found: {file_path}")
            fail_count += 1
            continue
        
        try:
            blog_post = load_blog_post(file_path)
            
            if publish_blog(blog_post):
                success_count += 1
            else:
                fail_count += 1
            
            # Wait between posts to avoid rate limiting
            if i < len(BLOG_FILES):
                print("  Waiting 2 seconds...")
                time.sleep(2)
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            fail_count += 1
    
    print("\n" + "=" * 60)
    print("PUBLISHING COMPLETE")
    print("=" * 60)
    print(f"✓ Successful: {success_count}")
    print(f"✗ Failed: {fail_count}")
    print(f"Total: {success_count + fail_count}")

if __name__ == '__main__':
    main()
