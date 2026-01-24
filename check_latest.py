"""
Check latest posts for cover image
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
response = requests.get('https://www.wixapis.com/blog/v3/posts', headers=headers, params={'paging.limit': 5})
if response.status_code == 200:
    posts = response.json().get('posts', [])
    for post in posts:
        title = post.get('title', '')[:50]
        media = post.get('media', {})
        print(f"Title: {title}...")
        print(f"  Media: {media}")
        print()
