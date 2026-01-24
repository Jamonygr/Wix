"""
Test cover image format for Wix Blog API
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('WIX_API_KEY')
SITE_ID = os.getenv('WIX_SITE_ID')
ACCOUNT_ID = os.getenv('WIX_ACCOUNT_ID')

# The Wix-hosted image URL
WIX_IMAGE_URL = "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png"

# Extract the media ID from the URL
# Format: https://static.wixstatic.com/media/{media_id}~mv2.{ext}
media_id = "32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png"

headers = {
    'Authorization': API_KEY,
    'wix-site-id': SITE_ID,
    'wix-account-id': ACCOUNT_ID,
    'Content-Type': 'application/json'
}

# Test different cover media formats
formats_to_test = [
    # Format 1: Using wixMedia.image with full URL
    {
        "name": "wixMedia with full URL",
        "media": {
            "wixMedia": {"image": WIX_IMAGE_URL},
            "displayed": True
        }
    },
    # Format 2: Using just the media ID
    {
        "name": "wixMedia with media ID",
        "media": {
            "wixMedia": {"image": media_id},
            "displayed": True
        }
    },
    # Format 3: Using image URL directly
    {
        "name": "wixMedia with image structure",
        "media": {
            "wixMedia": {
                "image": {
                    "url": WIX_IMAGE_URL,
                    "width": 1200,
                    "height": 675
                }
            },
            "displayed": True
        }
    },
    # Format 4: coverMedia field (alternative name)
    {
        "name": "coverMedia field",
        "coverMedia": {
            "image": WIX_IMAGE_URL
        }
    },
    # Format 5: heroImage field
    {
        "name": "heroImage field",
        "heroImage": {
            "url": WIX_IMAGE_URL
        }
    }
]

print("Testing cover image formats for Wix Blog API...")
print("=" * 60)

for i, format_test in enumerate(formats_to_test, 1):
    name = format_test.pop("name")
    print(f"\n{i}. Testing: {name}")
    
    # Build the draft post
    draft_post = {
        "title": f"TEST Cover Image Format {i} - DELETE ME",
        "richContent": {
            "nodes": [{
                "type": "PARAGRAPH",
                "nodes": [{
                    "type": "TEXT",
                    "textData": {"text": f"Testing cover image format: {name}"}
                }]
            }]
        },
        "memberId": ACCOUNT_ID,
        **format_test
    }
    
    data = {"draftPost": draft_post}
    
    response = requests.post(
        'https://www.wixapis.com/blog/v3/draft-posts',
        headers=headers,
        json=data
    )
    
    if response.status_code in [200, 201]:
        result = response.json()
        draft_id = result.get('draftPost', {}).get('id')
        print(f"   ✓ Draft created: {draft_id}")
        
        # Check if media was set
        media_info = result.get('draftPost', {}).get('media')
        cover_media = result.get('draftPost', {}).get('coverMedia')
        hero_image = result.get('draftPost', {}).get('heroImage')
        
        print(f"   media field: {media_info}")
        print(f"   coverMedia field: {cover_media}")
        print(f"   heroImage field: {hero_image}")
    else:
        print(f"   ✗ Failed: {response.status_code}")
        print(f"   Error: {response.text[:300]}")

print("\n" + "=" * 60)
print("Test complete. Check the drafts in Wix to see which format shows the cover image.")
print("Remember to delete the test drafts!")
