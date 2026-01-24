"""
Test cover image format for Wix Blog API - Round 2
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

# Different media ID formats
media_id_full = "32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png"
media_id_short = "32fce1_6c1cc8bc82db46b998b61dc5273d7d99"

headers = {
    'Authorization': API_KEY,
    'wix-site-id': SITE_ID,
    'wix-account-id': ACCOUNT_ID,
    'Content-Type': 'application/json'
}

# Test different cover media formats
formats_to_test = [
    # Format 1: media with image object containing id
    {
        "name": "media with image.id (full)",
        "media": {
            "image": {
                "id": media_id_full
            }
        }
    },
    # Format 2: media with image object containing id (short)
    {
        "name": "media with image.id (short)",
        "media": {
            "image": {
                "id": media_id_short
            }
        }
    },
    # Format 3: media with image object containing url
    {
        "name": "media with image.url",
        "media": {
            "image": {
                "url": WIX_IMAGE_URL
            }
        }
    },
    # Format 4: media with wixMedia containing id
    {
        "name": "media.wixMedia.id",
        "media": {
            "wixMedia": {
                "id": media_id_short
            }
        }
    },
    # Format 5: Just media.image as string (id)
    {
        "name": "media.image as string",
        "media": {
            "image": media_id_short
        }
    },
    # Format 6: media.wixMedia.image with full structure
    {
        "name": "media.wixMedia.image object",
        "media": {
            "wixMedia": {
                "image": {
                    "id": media_id_short,
                    "url": WIX_IMAGE_URL
                }
            }
        }
    },
    # Format 7: Try with wix: prefix
    {
        "name": "wix:image prefix",
        "media": {
            "image": f"wix:image://v1/{media_id_full}#originWidth=1200&originHeight=675"
        }
    }
]

print("Testing cover image formats for Wix Blog API - Round 2...")
print("=" * 60)

for i, format_test in enumerate(formats_to_test, 1):
    name = format_test.pop("name")
    print(f"\n{i}. Testing: {name}")
    
    # Build the draft post
    draft_post = {
        "title": f"TEST Cover R2-{i} - DELETE ME",
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
        
        # Check all media-related fields
        draft = result.get('draftPost', {})
        media_info = draft.get('media', {})
        
        print(f"   media: {media_info}")
        
        # Publish it to see if cover shows
        pub_url = f"https://www.wixapis.com/blog/v3/draft-posts/{draft_id}/publish"
        pub_response = requests.post(pub_url, headers=headers)
        if pub_response.status_code == 200:
            pub_result = pub_response.json()
            post = pub_result.get('post', {})
            print(f"   Published! Post media: {post.get('media', {})}")
        else:
            print(f"   Publish failed: {pub_response.status_code}")
    else:
        print(f"   ✗ Failed: {response.status_code}")
        error = response.text[:200]
        print(f"   Error: {error}")

print("\n" + "=" * 60)
print("Test complete!")
