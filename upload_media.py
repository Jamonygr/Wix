"""
Upload image to Wix Media Manager and use it as cover image
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('WIX_API_KEY')
SITE_ID = os.getenv('WIX_SITE_ID')
ACCOUNT_ID = os.getenv('WIX_ACCOUNT_ID')

# The Wix-hosted image URL to import
WIX_IMAGE_URL = "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png"

headers = {
    'Authorization': API_KEY,
    'wix-site-id': SITE_ID,
    'wix-account-id': ACCOUNT_ID,
    'Content-Type': 'application/json'
}

print("Step 1: Import image to Wix Media Manager...")
print("=" * 60)

# Try to import the image to get a proper media ID
import_url = "https://www.wixapis.com/site-media/v1/files/import"

import_data = {
    "url": WIX_IMAGE_URL,
    "displayName": "blog_cover_azure.png",
    "parentFolderId": "media-root"
}

response = requests.post(import_url, headers=headers, json=import_data)
print(f"Import response: {response.status_code}")
print(response.text[:500])

if response.status_code == 200:
    result = response.json()
    file_info = result.get('file', {})
    media_id = file_info.get('id')
    print(f"\nMedia ID: {media_id}")
    
    # Now try to use this media ID for a blog post
    print("\nStep 2: Create blog with this media ID...")
    
    draft_post = {
        "title": "TEST - Media ID Cover - DELETE ME",
        "richContent": {
            "nodes": [{
                "type": "PARAGRAPH",
                "nodes": [{
                    "type": "TEXT",
                    "textData": {"text": "Testing with uploaded media ID"}
                }]
            }]
        },
        "memberId": ACCOUNT_ID,
        "media": {
            "image": media_id,
            "displayed": True
        }
    }
    
    draft_response = requests.post(
        'https://www.wixapis.com/blog/v3/draft-posts',
        headers=headers,
        json={"draftPost": draft_post}
    )
    
    print(f"Draft response: {draft_response.status_code}")
    print(draft_response.text[:500])
else:
    # Try alternative: Generate upload URL
    print("\nTrying generate upload URL instead...")
    
    gen_url = "https://www.wixapis.com/site-media/v1/files/generate-upload-url"
    
    gen_data = {
        "mimeType": "image/png",
        "fileName": "blog_cover.png"
    }
    
    gen_response = requests.post(gen_url, headers=headers, json=gen_data)
    print(f"Generate URL response: {gen_response.status_code}")
    print(gen_response.text[:500])
