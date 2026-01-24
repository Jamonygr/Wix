"""
Test: Query existing published posts to see how their cover images are structured
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('WIX_API_KEY')
SITE_ID = os.getenv('WIX_SITE_ID')
ACCOUNT_ID = os.getenv('WIX_ACCOUNT_ID')

headers = {
    'Authorization': API_KEY,
    'wix-site-id': SITE_ID,
    'wix-account-id': ACCOUNT_ID,
    'Content-Type': 'application/json'
}

print("Querying existing blog posts to see cover image structure...")
print("=" * 60)

# Query posts
url = "https://www.wixapis.com/blog/v3/posts"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    result = response.json()
    posts = result.get('posts', [])
    
    print(f"Found {len(posts)} posts\n")
    
    for post in posts[:5]:  # Check first 5 posts
        title = post.get('title', 'No title')
        media = post.get('media', {})
        cover_media = post.get('coverMedia', {})
        hero_image = post.get('heroImage', {})
        
        print(f"Title: {title[:50]}...")
        print(f"  media: {media}")
        print(f"  coverMedia: {cover_media}")
        print(f"  heroImage: {hero_image}")
        
        # Check rich content for images
        rich_content = post.get('richContent', {})
        nodes = rich_content.get('nodes', [])
        for node in nodes:
            if node.get('type') == 'IMAGE':
                print(f"  IMAGE in content: {node.get('imageData', {}).get('image', {})}")
        
        print()
else:
    print(f"Failed: {response.status_code}")
    print(response.text[:500])
