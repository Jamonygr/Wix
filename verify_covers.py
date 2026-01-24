"""
Verify cover images on latest published blogs
"""
import os
import requests
from dotenv import load_dotenv
load_dotenv()

headers = {
    'Authorization': os.getenv('WIX_API_KEY'),
    'wix-site-id': os.getenv('WIX_SITE_ID'),
    'wix-account-id': os.getenv('WIX_ACCOUNT_ID'),
    'Content-Type': 'application/json'
}

# Get the latest posts
response = requests.get('https://www.wixapis.com/blog/v3/posts', headers=headers, params={'paging.limit': 20})
if response.status_code == 200:
    posts = response.json().get('posts', [])
    
    with_cover = 0
    without_cover = 0
    
    print("Latest 20 posts:")
    print("=" * 70)
    
    for post in posts:
        title = post.get('title', '')[:55]
        media = post.get('media', {})
        has_image = bool(media.get('wixMedia', {}).get('image'))
        
        status = "✓ HAS COVER" if has_image else "✗ NO COVER"
        
        if has_image:
            with_cover += 1
        else:
            without_cover += 1
        
        print(f"{status} | {title}")
    
    print("=" * 70)
    print(f"\nSummary: {with_cover} with cover, {without_cover} without cover")
