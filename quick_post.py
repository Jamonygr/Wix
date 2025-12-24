"""
Quick Blog Poster for BeyondCloudWithChriz.com
Simply run: python quick_post.py
"""

from wix_blog import create_blog_post

# ============================================================
# ✏️ EDIT YOUR BLOG POST BELOW
# ============================================================

BLOG_POST = {
    "title": "Your Blog Title Here",
    
    "content": """
Your blog content goes here.

You can have multiple paragraphs - just leave a blank line between them.

Add your main content, tips, tutorials, or whatever you want to share!

Feel free to be creative - this is YOUR blog!
""",
    
    "excerpt": "A short description that appears in previews and search results",
    
    "publish": False,  # Set to True to publish immediately, False for draft
    
    "tags": ["azure", "cloud", "technology"]  # Add your tags
}

# ============================================================
# 🚀 RUN THE POST
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  📝 Quick Blog Poster - BeyondCloudWithChriz")
    print("="*50)
    
    print(f"\n📌 Title: {BLOG_POST['title']}")
    print(f"📋 Excerpt: {BLOG_POST['excerpt']}")
    print(f"🏷️  Tags: {', '.join(BLOG_POST['tags'])}")
    print(f"🌐 Publish: {'Yes (Live immediately)' if BLOG_POST['publish'] else 'No (Draft only)'}")
    
    confirm = input("\n✅ Post this blog? (yes/no): ")
    
    if confirm.lower().startswith('y'):
        result = create_blog_post(**BLOG_POST)
        if result and result.get('published'):
            print("\n🎉 SUCCESS! Your blog post is LIVE!")
        elif result:
            print("\n📝 Draft saved! You can publish it from your Wix dashboard.")
    else:
        print("\n❌ Cancelled.")
