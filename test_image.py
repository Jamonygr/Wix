"""
Test different image formats for Wix Blog API
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('WIX_API_KEY')
SITE_ID = os.getenv('WIX_SITE_ID')
ACCOUNT_ID = os.getenv('WIX_ACCOUNT_ID')

def create_test_post_with_image():
    """Test creating a post with an embedded image"""
    url = 'https://www.wixapis.com/blog/v3/draft-posts'
    
    headers = {
        'Authorization': API_KEY,
        'wix-site-id': SITE_ID,
        'wix-account-id': ACCOUNT_ID,
        'Content-Type': 'application/json'
    }
    
    image_url = "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200"
    
    # Try using EMBED with oembed format
    nodes = [
        {
            "type": "EMBED",
            "id": "embed-img",
            "nodes": [],
            "embedData": {
                "containerData": {
                    "width": {
                        "size": "FULL_WIDTH"
                    },
                    "alignment": "CENTER"
                },
                "oembed": {
                    "type": "photo",
                    "url": image_url,
                    "width": 1200,
                    "height": 675,
                    "thumbnail_url": image_url,
                    "thumbnail_width": 1200,
                    "thumbnail_height": 675
                },
                "src": image_url
            }
        },
        {
            "type": "PARAGRAPH",
            "id": "p1",
            "nodes": [
                {
                    "type": "TEXT",
                    "id": "t1",
                    "textData": {
                        "text": "This is a test post to check if images display correctly."
                    }
                }
            ]
        }
    ]
    
    rich_content = {
        "nodes": nodes
    }
    
    draft_post = {
        "title": "TEST - Image Display Test (Delete Me)",
        "richContent": rich_content,
        "memberId": ACCOUNT_ID,
        "excerpt": "Testing image display"
    }
    
    data = {"draftPost": draft_post}
    
    print("Creating test post with image...")
    print(f"Image URL: {image_url}")
    
    response = requests.post(url, headers=headers, json=data)
    
    print(f"Response status: {response.status_code}")
    print(f"Response: {response.text[:1000]}")
    
    if response.status_code in [200, 201]:
        result = response.json()
        draft_id = result.get('draftPost', {}).get('id')
        print(f"\nDraft created: {draft_id}")
        
        # Publish it
        pub_url = f'https://www.wixapis.com/blog/v3/draft-posts/{draft_id}/publish'
        pub_response = requests.post(pub_url, headers=headers, json={})
        print(f"Publish status: {pub_response.status_code}")
        
        if pub_response.status_code in [200, 201]:
            pub_result = pub_response.json()
            post = pub_result.get('post', {})
            slug = post.get('slug', '')
            print(f"Published! Check: https://www.beyondcloudwithchriz.com/blog/{slug}")
    
    return response

if __name__ == '__main__':
    create_test_post_with_image()
