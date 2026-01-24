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

# Query posts - get more of them
url = "https://www.wixapis.com/blog/v3/posts"
params = {"paging.limit": 100}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    result = response.json()
    posts = result.get('posts', [])
    
    print(f"Found {len(posts)} posts\n")
    
    # Look for posts that have actual cover images
    for post in posts:
        title = post.get('title', 'No title')
        media = post.get('media', {})
        cover_media = post.get('coverMedia', {})
        
        # Skip test posts
        if 'TEST' in title or 'DELETE' in title:
            continue
        
        # Check if this post has any images
        has_image = bool(media.get('image') or cover_media.get('image') or media.get('wixMedia'))
        
        if has_image or len(media) > 2:  # More than just displayed and custom
            print(f"Title: {title[:60]}")
            print(f"  Full media object: {media}")
            print(f"  coverMedia: {cover_media}")
            print()
else:
    print(f"Failed: {response.status_code}")
    print(response.text[:500])

print("\n" + "=" * 60)
print("Looking for posts with 'displayed': True and actual images...")
