"""
Add Cover Images to Published Blog Posts
Imports images from URLs and updates existing blog posts
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

# Blog files with their images
BLOG_FILES = [
    'blog_01_azure_superfactory.py',
    'blog_02_nvidia_rubin.py',
    'blog_03_a2a_protocol.py',
    'blog_04_oracle_azure_expansion.py',
    'blog_05_secure_future_initiative.py',
    'blog_06_claude_opus.py',
    'blog_07_container_apps_networking.py',
    'blog_08_virtual_desktop.py',
    'blog_09_log_analytics_fabric.py',
    'blog_10_uipath_integration.py',
    'blog_11_azure_resiliency.py',
    'blog_12_performance_plus_disk.py',
    'blog_13_github_universe.py',
    'blog_14_agent_hq.py',
    'blog_15_azure_pulse_january.py',
]

def load_blog_post(file_path):
    """Load BLOG_POST from a Python file"""
    spec = importlib.util.spec_from_file_location("blog_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.BLOG_POST

def import_image_to_wix(image_url):
    """Import an external image URL to Wix Media Manager"""
    url = 'https://www.wixapis.com/site-media/v1/files/import'
    
    headers = {
        'Authorization': API_KEY,
        'wix-site-id': SITE_ID,
        'wix-account-id': ACCOUNT_ID,
        'Content-Type': 'application/json'
    }
    
    data = {
        "url": image_url,
        "mimeType": "image/jpeg",
        "displayName": "Blog Cover Image"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        result = response.json()
        file_data = result.get('file', {})
        return file_data.get('id') or file_data.get('_id')
    else:
        print(f"Error importing image: {response.status_code}")
        print(response.text[:300])
        return None

def get_posts():
    """Get all published blog posts"""
    url = 'https://www.wixapis.com/blog/v3/posts'
    
    headers = {
        'Authorization': API_KEY,
        'wix-site-id': SITE_ID,
        'wix-account-id': ACCOUNT_ID,
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('posts', [])
    else:
        print(f"Error fetching posts: {response.status_code}")
        return []

def update_post_cover(post_id, wix_image_id):
    """Update a blog post's cover image using Wix media ID"""
    url = f'https://www.wixapis.com/blog/v3/posts/{post_id}'
    
    headers = {
        'Authorization': API_KEY,
        'wix-site-id': SITE_ID,
        'wix-account-id': ACCOUNT_ID,
        'Content-Type': 'application/json'
    }
    
    data = {
        "post": {
            "media": {
                "wixMedia": {
                    "image": wix_image_id
                },
                "displayed": True
            }
        }
    }
    
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        return True
    else:
        print(f"Error updating post: {response.status_code}")
        print(response.text[:300])
        return False

def main():
    """Main function to add cover images to posts"""
    print("=" * 60)
    print("Adding Cover Images to V3 Blog Posts")
    print("=" * 60)
    
    # Check environment variables
    if not all([API_KEY, SITE_ID, ACCOUNT_ID]):
        print("Error: Missing environment variables!")
        return
    
    # Get existing posts
    print("\nFetching existing posts...")
    posts = get_posts()
    print(f"Found {len(posts)} posts")
    
    # Create a mapping of titles to post IDs
    post_map = {}
    for post in posts:
        title = post.get('title', '')
        post_id = post.get('id')
        post_map[title] = post_id
        print(f"  - {title[:50]}... (ID: {post_id})")
    
    blogs_dir = os.path.join(os.path.dirname(__file__), 'blogs_v3')
    
    success_count = 0
    fail_count = 0
    
    for i, blog_file in enumerate(BLOG_FILES, 1):
        print(f"\n[{i}/{len(BLOG_FILES)}] Processing {blog_file}...")
        
        file_path = os.path.join(blogs_dir, blog_file)
        
        if not os.path.exists(file_path):
            print(f"  ✗ File not found")
            fail_count += 1
            continue
        
        try:
            blog_post = load_blog_post(file_path)
            title = blog_post['title']
            cover_url = blog_post.get('coverImage')
            
            if not cover_url:
                print(f"  ✗ No cover image URL")
                fail_count += 1
                continue
            
            # Find the post ID
            post_id = post_map.get(title)
            if not post_id:
                print(f"  ✗ Post not found in Wix: {title[:40]}...")
                fail_count += 1
                continue
            
            print(f"  Found post ID: {post_id}")
            print(f"  Importing image from: {cover_url[:50]}...")
            
            # Import image to Wix
            wix_image_id = import_image_to_wix(cover_url)
            
            if wix_image_id:
                print(f"  Image imported: {wix_image_id}")
                
                # Update post with cover image
                if update_post_cover(post_id, wix_image_id):
                    print(f"  ✓ Cover image added successfully!")
                    success_count += 1
                else:
                    fail_count += 1
            else:
                print(f"  ✗ Failed to import image")
                fail_count += 1
            
            # Wait between operations
            if i < len(BLOG_FILES):
                time.sleep(2)
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            fail_count += 1
    
    print("\n" + "=" * 60)
    print("COVER IMAGE UPDATE COMPLETE")
    print("=" * 60)
    print(f"✓ Successful: {success_count}")
    print(f"✗ Failed: {fail_count}")
    print(f"Total: {success_count + fail_count}")

if __name__ == '__main__':
    main()
