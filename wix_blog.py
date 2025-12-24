"""
Wix Blog Automation for BeyondCloudWithChriz.com
Automated blog posting tool using Python
"""

import os
import json
import requests
from datetime import datetime
import uuid

# Load credentials from .env file
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    config = {}
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    return config

CONFIG = load_env()
API_KEY = CONFIG.get('WIX_API_KEY', '')
SITE_ID = CONFIG.get('WIX_SITE_ID', '')
SITE_URL = CONFIG.get('WIX_SITE_URL', 'https://www.beyondcloudwithchriz.com')

HEADERS = {
    'Authorization': API_KEY,
    'Content-Type': 'application/json',
}


def test_connection():
    """Test connection to Wix API and retrieve site information."""
    print('\n🔄 Testing connection to Wix API...\n')
    
    try:
        response = requests.post(
            'https://www.wixapis.com/site-list/v2/sites/query',
            headers=HEADERS,
            json={'query': {}}
        )
        
        if response.status_code != 200:
            print(f'❌ Sites API Error: {response.status_code}')
            print(f'   Response: {response.text}')
            return None
        
        data = response.json()
        sites = data.get('sites', [])
        
        print('✅ Connected to Wix successfully!\n')
        print('📋 Your Sites:')
        
        if sites:
            for i, site in enumerate(sites, 1):
                print(f"\n  {i}. {site.get('displayName', 'Unnamed Site')}")
                print(f"     Site ID: {site.get('id')}")
                print(f"     URL: {site.get('siteUrl', 'N/A')}")
            
            site_id = sites[0].get('id')
            print(f'\n💡 Add this to your .env file:')
            print(f'   WIX_SITE_ID={site_id}')
            
            # Auto-update .env file
            update_env = input('\n📝 Update .env file automatically? (yes/no): ')
            if update_env.lower().startswith('y'):
                add_site_id_to_env(site_id)
                print('✅ .env file updated!')
            
            return site_id
        else:
            print('  No sites found.')
            return None
            
    except Exception as e:
        print(f'❌ Connection failed: {e}')
        return None


def add_site_id_to_env(site_id):
    """Add or update WIX_SITE_ID in .env file."""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    lines = []
    site_id_found = False
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            lines = f.readlines()
    
    with open(env_path, 'w') as f:
        for line in lines:
            if line.startswith('WIX_SITE_ID='):
                f.write(f'WIX_SITE_ID={site_id}\n')
                site_id_found = True
            else:
                f.write(line)
        
        if not site_id_found:
            f.write(f'WIX_SITE_ID={site_id}\n')


def generate_id():
    """Generate a unique ID for rich content nodes."""
    return str(uuid.uuid4())[:12]


def create_blog_post(title, content, excerpt=None, publish=True, tags=None, cover_image=None):
    """
    Create and optionally publish a blog post to Wix.
    
    Args:
        title (str): The title of the blog post
        content (str): The main content of the blog post
        excerpt (str, optional): Short description. Defaults to title.
        publish (bool, optional): Whether to publish immediately. Defaults to True.
        tags (list, optional): List of tag labels. Defaults to [].
        cover_image (str, optional): URL of the cover image.
    
    Returns:
        dict: Result with draft_id, post_id, slug, and published status
    """
    global SITE_ID, CONFIG
    
    # Reload config in case it was updated
    CONFIG = load_env()
    SITE_ID = CONFIG.get('WIX_SITE_ID', '')
    
    if not SITE_ID:
        print('❌ WIX_SITE_ID not found in .env file!')
        print('   Run test_connection() first to get your Site ID.')
        return None
    
    tags = tags or []
    excerpt = excerpt or title
    
    print(f'\n📝 Creating blog post: "{title}"...\n')
    
    # Build rich content structure
    # Split content by paragraphs for better formatting
    paragraphs = content.strip().split('\n\n')
    nodes = []
    
    for para in paragraphs:
        if para.strip():
            nodes.append({
                "type": "PARAGRAPH",
                "id": generate_id(),
                "nodes": [
                    {
                        "type": "TEXT",
                        "id": generate_id(),
                        "textData": {
                            "text": para.strip(),
                            "decorations": []
                        }
                    }
                ]
            })
    
    rich_content = {"nodes": nodes}
    
    # Build draft post object
    draft_post = {
        "title": title,
        "excerpt": excerpt,
        "richContent": rich_content,
        "featured": False,
        "commentingEnabled": True,
        "tagIds": []
    }
    
    # Add cover image if provided
    if cover_image:
        draft_post["media"] = {
            "wixMedia": {"image": cover_image},
            "displayed": True
        }
    
    headers = {
        **HEADERS,
        'wix-site-id': SITE_ID
    }
    
    try:
        # Step 1: Create draft post
        response = requests.post(
            'https://www.wixapis.com/blog/v3/draft-posts',
            headers=headers,
            json={"draftPost": draft_post}
        )
        
        if response.status_code != 200:
            print(f'❌ Failed to create draft: {response.status_code}')
            print(f'   Error: {response.text}')
            return None
        
        data = response.json()
        draft_post_id = data.get('draftPost', {}).get('id')
        print(f'✅ Draft created! ID: {draft_post_id}')
        
        # Step 2: Publish if requested
        if publish:
            print('📤 Publishing post...')
            
            publish_response = requests.post(
                f'https://www.wixapis.com/blog/v3/draft-posts/{draft_post_id}/publish',
                headers=headers
            )
            
            if publish_response.status_code != 200:
                print(f'❌ Failed to publish: {publish_response.status_code}')
                print(f'   Error: {publish_response.text}')
                print('   Note: Draft was created but not published.')
                return {"draft_id": draft_post_id, "published": False}
            
            publish_data = publish_response.json()
            post = publish_data.get('post', {})
            slug = post.get('slug', '')
            
            print('✅ Post published successfully!')
            print(f'\n🔗 View your post at: {SITE_URL}/blog/{slug}')
            
            return {
                "draft_id": draft_post_id,
                "post_id": post.get('id'),
                "slug": slug,
                "published": True
            }
        
        return {"draft_id": draft_post_id, "published": False}
        
    except Exception as e:
        print(f'❌ Error: {e}')
        return None


def list_blog_posts():
    """List all published blog posts."""
    global SITE_ID, CONFIG
    
    # Reload config
    CONFIG = load_env()
    SITE_ID = CONFIG.get('WIX_SITE_ID', '')
    
    if not SITE_ID:
        print('❌ WIX_SITE_ID not found in .env file!')
        return []
    
    print('\n📚 Fetching your blog posts...\n')
    
    headers = {
        **HEADERS,
        'wix-site-id': SITE_ID
    }
    
    try:
        response = requests.get(
            'https://www.wixapis.com/blog/v3/posts',
            headers=headers
        )
        
        if response.status_code != 200:
            print(f'❌ Failed to fetch posts: {response.status_code}')
            print(f'   Error: {response.text}')
            return []
        
        data = response.json()
        posts = data.get('posts', [])
        
        if not posts:
            print('📭 No blog posts found.')
        else:
            print(f'Found {len(posts)} posts:\n')
            for i, post in enumerate(posts, 1):
                pub_date = post.get('firstPublishedDate', 'Unknown')
                if pub_date != 'Unknown':
                    try:
                        pub_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00')).strftime('%Y-%m-%d')
                    except:
                        pass
                print(f'{i}. {post.get("title")}')
                print(f'   Published: {pub_date}')
                print(f'   URL: /blog/{post.get("slug")}\n')
        
        return posts
        
    except Exception as e:
        print(f'❌ Error: {e}')
        return []


def interactive_post():
    """Interactive mode to create a blog post."""
    print('\n🚀 Beyond Cloud with Chriz - Blog Poster')
    print('=' * 42)
    print()
    
    title = input('📌 Blog Title: ')
    
    print('\n📝 Enter your blog content (type "DONE" on a new line when finished):')
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'DONE':
            break
        lines.append(line)
    content = '\n'.join(lines)
    
    excerpt = input('\n📋 Short description/excerpt: ')
    
    publish_answer = input('\n🌐 Publish immediately? (yes/no): ')
    publish = publish_answer.lower().startswith('y')
    
    tags_input = input('\n🏷️  Tags (comma-separated): ')
    tags = [t.strip() for t in tags_input.split(',') if t.strip()]
    
    print('\n' + '-' * 40)
    print('Preview:')
    print(f'Title: {title}')
    print(f'Content: {content[:100]}...' if len(content) > 100 else f'Content: {content}')
    print(f'Excerpt: {excerpt}')
    print(f'Tags: {", ".join(tags)}')
    print(f'Publish: {"Yes" if publish else "No (Draft only)"}')
    print('-' * 40 + '\n')
    
    confirm = input('✅ Post this to your blog? (yes/no): ')
    
    if confirm.lower().startswith('y'):
        result = create_blog_post(
            title=title,
            content=content,
            excerpt=excerpt,
            publish=publish,
            tags=tags
        )
        return result
    else:
        print('\n❌ Post cancelled.')
        return None


def main():
    """Main menu for the blog automation tool."""
    print('\n' + '=' * 50)
    print('  🌐 Wix Blog Automation - BeyondCloudWithChriz')
    print('=' * 50)
    print('\nOptions:')
    print('  1. Test API Connection')
    print('  2. Create a Blog Post (Interactive)')
    print('  3. List All Blog Posts')
    print('  4. Quick Post (Sample)')
    print('  5. Exit')
    
    choice = input('\nSelect an option (1-5): ')
    
    if choice == '1':
        test_connection()
    elif choice == '2':
        interactive_post()
    elif choice == '3':
        list_blog_posts()
    elif choice == '4':
        # Quick sample post
        sample = {
            "title": "Welcome to Beyond Cloud with Chriz!",
            "content": """Hello and welcome to my blog!

This is my first automated post created using the Wix Blog API.

I'll be sharing insights about cloud computing, technology trends, and my journey in the tech world.

Stay tuned for more exciting content!

Best regards,
Chriz""",
            "excerpt": "Welcome to my blog! Discover insights about cloud computing and technology.",
            "publish": False,  # Draft only for safety
            "tags": ["welcome", "introduction", "cloud"]
        }
        
        print('\n📝 Sample Post Preview:')
        print(f'   Title: {sample["title"]}')
        print(f'   (This will be saved as a DRAFT)')
        
        confirm = input('\nCreate this sample post as a draft? (yes/no): ')
        if confirm.lower().startswith('y'):
            create_blog_post(**sample)
    elif choice == '5':
        print('\n👋 Goodbye!')
        return
    else:
        print('\n❌ Invalid option.')
    
    # Loop back to menu
    input('\nPress Enter to continue...')
    main()


if __name__ == '__main__':
    main()
