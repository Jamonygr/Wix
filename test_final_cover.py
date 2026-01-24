"""
Test the cover image format with a single blog
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('WIX_API_KEY')
SITE_ID = os.getenv('WIX_SITE_ID')
ACCOUNT_ID = os.getenv('WIX_ACCOUNT_ID')

# The Wix-hosted image URL
cover_image = "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png"

headers = {
    'Authorization': API_KEY,
    'wix-site-id': SITE_ID,
    'wix-account-id': ACCOUNT_ID,
    'Content-Type': 'application/json'
}

print("Testing correct cover image format...")
print("=" * 60)

# Extract media ID
media_id = cover_image.split('/media/')[-1]
print(f"Media ID: {media_id}")

# Build draft post with the correct format
draft_post = {
    "title": "TEST - Cover Image Final Test - DELETE ME",
    "richContent": {
        "nodes": [{
            "type": "PARAGRAPH",
            "nodes": [{
                "type": "TEXT",
                "textData": {"text": "Testing the correct cover image format matching existing posts."}
            }]
        }]
    },
    "memberId": ACCOUNT_ID,
    "media": {
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
}

data = {"draftPost": draft_post}

print("\nCreating draft...")
response = requests.post(
    'https://www.wixapis.com/blog/v3/draft-posts',
    headers=headers,
    json=data
)

if response.status_code in [200, 201]:
    result = response.json()
    draft_id = result.get('draftPost', {}).get('id')
    draft_media = result.get('draftPost', {}).get('media', {})
    
    print(f"✓ Draft created: {draft_id}")
    print(f"Draft media: {draft_media}")
    
    # Publish
    print("\nPublishing...")
    pub_url = f"https://www.wixapis.com/blog/v3/draft-posts/{draft_id}/publish"
    pub_response = requests.post(pub_url, headers=headers)
    
    if pub_response.status_code == 200:
        pub_result = pub_response.json()
        post = pub_result.get('post', {})
        post_media = post.get('media', {})
        
        print(f"✓ Published!")
        print(f"Post media: {post_media}")
        print(f"\nCheck the blog overview to see if cover image appears!")
    else:
        print(f"Publish failed: {pub_response.status_code}")
        print(pub_response.text[:300])
else:
    print(f"Failed: {response.status_code}")
    print(response.text[:500])
