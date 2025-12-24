import 'dotenv/config';

const API_KEY = process.env.WIX_API_KEY;
const SITE_ID = process.env.WIX_SITE_ID;

/**
 * Create and publish a blog post to your Wix site
 * @param {Object} post - The blog post data
 * @param {string} post.title - The title of the blog post
 * @param {string} post.content - The HTML content of the blog post
 * @param {string} post.excerpt - Short description/excerpt
 * @param {boolean} post.publish - Whether to publish immediately (default: true)
 * @param {string[]} post.tags - Array of tag labels
 * @param {string} post.coverImage - URL of the cover image (optional)
 */
async function createBlogPost(post) {
    const { title, content, excerpt, publish = true, tags = [], coverImage } = post;
    
    if (!SITE_ID) {
        console.error('❌ WIX_SITE_ID not found in .env file!');
        console.log('   Run "npm test" first to get your Site ID.');
        return null;
    }

    console.log(`\n📝 Creating blog post: "${title}"...\n`);

    // Build the rich content structure for Wix
    const richContent = {
        nodes: [
            {
                type: "PARAGRAPH",
                id: generateId(),
                nodes: [
                    {
                        type: "TEXT",
                        id: generateId(),
                        textData: {
                            text: content,
                            decorations: []
                        }
                    }
                ]
            }
        ]
    };

    // Build the draft post object
    const draftPost = {
        title: title,
        excerpt: excerpt || title,
        richContent: richContent,
        featured: false,
        commentingEnabled: true,
        tagIds: []
    };

    // Add cover image if provided
    if (coverImage) {
        draftPost.media = {
            wixMedia: {
                image: coverImage
            },
            displayed: true
        };
    }

    try {
        // Step 1: Create a draft post
        const createResponse = await fetch(
            `https://www.wixapis.com/blog/v3/draft-posts`,
            {
                method: 'POST',
                headers: {
                    'Authorization': API_KEY,
                    'wix-site-id': SITE_ID,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ draftPost })
            }
        );

        if (!createResponse.ok) {
            const errorText = await createResponse.text();
            console.error('❌ Failed to create draft:', createResponse.status);
            console.error('   Error:', errorText);
            return null;
        }

        const createData = await createResponse.json();
        const draftPostId = createData.draftPost.id;
        console.log(`✅ Draft created! ID: ${draftPostId}`);

        // Step 2: Publish the post if requested
        if (publish) {
            console.log('📤 Publishing post...');
            
            const publishResponse = await fetch(
                `https://www.wixapis.com/blog/v3/draft-posts/${draftPostId}/publish`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': API_KEY,
                        'wix-site-id': SITE_ID,
                        'Content-Type': 'application/json',
                    }
                }
            );

            if (!publishResponse.ok) {
                const errorText = await publishResponse.text();
                console.error('❌ Failed to publish:', publishResponse.status);
                console.error('   Error:', errorText);
                console.log('   Note: Draft was created but not published.');
                return { draftId: draftPostId, published: false };
            }

            const publishData = await publishResponse.json();
            console.log('✅ Post published successfully!');
            console.log(`\n🔗 View your post at: https://www.beyondcloudwithchriz.com/blog/${publishData.post?.slug || ''}`);
            
            return { 
                draftId: draftPostId, 
                postId: publishData.post?.id,
                slug: publishData.post?.slug,
                published: true 
            };
        }

        return { draftId: draftPostId, published: false };

    } catch (error) {
        console.error('❌ Error:', error.message);
        return null;
    }
}

/**
 * List all published blog posts
 */
async function listBlogPosts() {
    if (!SITE_ID) {
        console.error('❌ WIX_SITE_ID not found in .env file!');
        return [];
    }

    console.log('\n📚 Fetching your blog posts...\n');

    try {
        const response = await fetch(
            `https://www.wixapis.com/blog/v3/posts`,
            {
                method: 'GET',
                headers: {
                    'Authorization': API_KEY,
                    'wix-site-id': SITE_ID,
                    'Content-Type': 'application/json',
                }
            }
        );

        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Failed to fetch posts:', response.status, errorText);
            return [];
        }

        const data = await response.json();
        const posts = data.posts || [];

        if (posts.length === 0) {
            console.log('📭 No blog posts found.');
        } else {
            console.log(`Found ${posts.length} posts:\n`);
            posts.forEach((post, index) => {
                console.log(`${index + 1}. ${post.title}`);
                console.log(`   Published: ${new Date(post.firstPublishedDate).toLocaleDateString()}`);
                console.log(`   URL: /blog/${post.slug}\n`);
            });
        }

        return posts;

    } catch (error) {
        console.error('❌ Error:', error.message);
        return [];
    }
}

// Helper function to generate random IDs for rich content
function generateId() {
    return Math.random().toString(36).substring(2, 15);
}

// ============================================
// EXAMPLE: Create a sample blog post
// ============================================

// Check if running directly
const isMainModule = import.meta.url === `file:///${process.argv[1].replace(/\\/g, '/')}`;

if (isMainModule) {
    // Example blog post - modify this!
    const samplePost = {
        title: "Welcome to Beyond Cloud with Chriz!",
        content: `Hello and welcome to my blog! 

This is my first automated post created using the Wix Blog API. 

I'll be sharing insights about cloud computing, technology trends, and my journey in the tech world.

Stay tuned for more exciting content!

Best regards,
Chriz`,
        excerpt: "Welcome to my blog! Discover insights about cloud computing and technology.",
        publish: true,  // Set to false to save as draft only
        tags: ["welcome", "introduction", "cloud"]
    };

    // Uncomment the line below to post:
    // await createBlogPost(samplePost);
    
    // Or list existing posts:
    await listBlogPosts();
}

export { createBlogPost, listBlogPosts };
