"""
Add neon CSS as a style block embedded in blog content
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

# Neon CSS styles (minified for embedding)
NEON_CSS = """
<style>
/* Neon Blog Effects */
[data-hook="post-title"], .post-title, h1 {
  color: #00f5ff !important;
  text-shadow: 0 0 5px #00f5ff, 0 0 10px #00f5ff, 0 0 20px #00f5ff, 0 0 40px #00a8cc !important;
  animation: neonPulse 2s ease-in-out infinite alternate;
}
@keyframes neonPulse {
  from { text-shadow: 0 0 5px #00f5ff, 0 0 10px #00f5ff, 0 0 20px #00f5ff; }
  to { text-shadow: 0 0 10px #00f5ff, 0 0 20px #00f5ff, 0 0 40px #00f5ff, 0 0 80px #00a8cc; }
}
[data-hook="post-list-item"], article {
  border: 2px solid #ff00ff !important;
  box-shadow: 0 0 15px rgba(255,0,255,0.4), 0 0 30px rgba(0,245,255,0.3) !important;
  border-radius: 8px !important;
  transition: all 0.3s ease !important;
}
[data-hook="post-list-item"]:hover, article:hover {
  box-shadow: 0 0 25px rgba(255,0,255,0.6), 0 0 50px rgba(0,245,255,0.5) !important;
  transform: translateY(-3px);
}
</style>
"""

print("Testing: Add neon effects via HTML node in blog content...")
print("=" * 60)

# Create a test post with embedded HTML/CSS
draft_post = {
    "title": "🌟 NEON TEST - Synthwave Style Demo",
    "richContent": {
        "nodes": [
            # HTML node with the CSS
            {
                "type": "HTML",
                "id": "neon-styles",
                "nodes": [],
                "htmlData": {
                    "containerData": {
                        "width": {"size": "FULL_WIDTH"},
                        "alignment": "CENTER"
                    },
                    "source": "HTML",
                    "html": NEON_CSS
                }
            },
            {
                "type": "PARAGRAPH",
                "nodes": [{
                    "type": "TEXT",
                    "textData": {"text": "This is a test post to see if neon CSS effects can be embedded in blog content."}
                }]
            }
        ]
    },
    "memberId": ACCOUNT_ID
}

response = requests.post(
    'https://www.wixapis.com/blog/v3/draft-posts',
    headers=headers,
    json={"draftPost": draft_post}
)

if response.status_code in [200, 201]:
    result = response.json()
    draft_id = result.get('draftPost', {}).get('id')
    print(f"✓ Draft created: {draft_id}")
    
    # Publish
    pub_response = requests.post(
        f'https://www.wixapis.com/blog/v3/draft-posts/{draft_id}/publish',
        headers=headers
    )
    
    if pub_response.status_code == 200:
        print("✓ Published!")
        print("\nCheck your blog to see if the neon effects are visible.")
    else:
        print(f"Publish failed: {pub_response.status_code}")
        print(pub_response.text[:300])
else:
    print(f"Failed: {response.status_code}")
    print(response.text[:500])
    
    # Try alternative: EMBED node
    print("\n\nTrying EMBED node instead...")
    
    draft_post2 = {
        "title": "🌟 NEON TEST v2 - Embed Node",
        "richContent": {
            "nodes": [
                {
                    "type": "EMBED",
                    "id": "neon-embed",
                    "nodes": [],
                    "embedData": {
                        "containerData": {
                            "width": {"size": "FULL_WIDTH"}
                        },
                        "html": NEON_CSS
                    }
                },
                {
                    "type": "PARAGRAPH",
                    "nodes": [{
                        "type": "TEXT",
                        "textData": {"text": "Testing neon effects with EMBED node."}
                    }]
                }
            ]
        },
        "memberId": ACCOUNT_ID
    }
    
    response2 = requests.post(
        'https://www.wixapis.com/blog/v3/draft-posts',
        headers=headers,
        json={"draftPost": draft_post2}
    )
    
    print(f"EMBED result: {response2.status_code}")
    print(response2.text[:300])
