"""
Upload image to Wix Media Manager and use it as cover image for all blogs
"""

import os
import time
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

# Import the image to get a proper media ID
import_url = "https://www.wixapis.com/site-media/v1/files/import"

import_data = {
    "url": WIX_IMAGE_URL,
    "displayName": "blog_cover_azure.png",
    "parentFolderId": "media-root"
}

response = requests.post(import_url, headers=headers, json=import_data)
print(f"Import response: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    file_info = result.get('file', {})
    media_id = file_info.get('id')
    print(f"Media ID: {media_id}")
    
    # Wait for processing
    print("\nWaiting for image processing...")
    time.sleep(2)
    
    # Now test with the proper media ID format
    print("\nStep 2: Create blog with proper media format...")
    
    # Try with just the ID (without .png extension)
    media_id_clean = media_id.replace('~mv2.png', '')
    
    # Test different formats with the imported media ID
    formats = [
        ("media.image as ID", {"media": {"image": media_id, "displayed": True}}),
        ("media.wixMedia.image", {"media": {"wixMedia": {"image": media_id}, "displayed": True}}),
        ("media.image clean ID", {"media": {"image": media_id_clean, "displayed": True}}),
    ]
    
    for name, media_config in formats:
        print(f"\nTesting: {name}")
        
        draft_post = {
            "title": f"TEST Cover {name[:10]} - DELETE",
            "richContent": {
                "nodes": [{
                    "type": "PARAGRAPH",
                    "nodes": [{
                        "type": "TEXT",
                        "textData": {"text": f"Testing: {name}"}
                    }]
                }]
            },
            "memberId": ACCOUNT_ID,
            **media_config
        }
        
        draft_response = requests.post(
            'https://www.wixapis.com/blog/v3/draft-posts',
            headers=headers,
            json={"draftPost": draft_post}
        )
        
        if draft_response.status_code == 200:
            draft_result = draft_response.json()
            draft_id = draft_result.get('draftPost', {}).get('id')
            media_info = draft_result.get('draftPost', {}).get('media', {})
            print(f"   ✓ Draft created: {draft_id}")
            print(f"   Draft media: {media_info}")
            
            # Publish it
            pub_url = f"https://www.wixapis.com/blog/v3/draft-posts/{draft_id}/publish"
            pub_response = requests.post(pub_url, headers=headers)
            
            if pub_response.status_code == 200:
                pub_result = pub_response.json()
                post_media = pub_result.get('post', {}).get('media', {})
                post_url = pub_result.get('post', {}).get('url', '')
                print(f"   ✓ Published!")
                print(f"   Post media: {post_media}")
                print(f"   URL: {post_url}")
            else:
                print(f"   Publish failed: {pub_response.status_code}")
        else:
            print(f"   ✗ Failed: {draft_response.status_code}")
            print(f"   {draft_response.text[:200]}")
else:
    print(f"Import failed: {response.text}")

print("\n" + "=" * 60)
print("Check the blog at https://www.beyondcloudwithchriz.com/blog to see if covers appear!")
