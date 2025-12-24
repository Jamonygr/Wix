import 'dotenv/config';
import { createBlogPost } from './postBlog.js';
import * as readline from 'readline';

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function question(prompt) {
    return new Promise((resolve) => {
        rl.question(prompt, (answer) => {
            resolve(answer);
        });
    });
}

async function interactivePost() {
    console.log('\n🚀 Beyond Cloud with Chriz - Blog Poster\n');
    console.log('=========================================\n');

    try {
        const title = await question('📌 Blog Title: ');
        
        console.log('\n📝 Enter your blog content (press Enter twice when done):\n');
        
        let content = '';
        let emptyLineCount = 0;
        
        const contentLines = [];
        
        // Simple content input
        const contentInput = await question('');
        content = contentInput;
        
        const excerpt = await question('\n📋 Short description/excerpt: ');
        
        const publishAnswer = await question('\n🌐 Publish immediately? (yes/no): ');
        const publish = publishAnswer.toLowerCase().startsWith('y');

        const tagsInput = await question('\n🏷️  Tags (comma-separated): ');
        const tags = tagsInput.split(',').map(t => t.trim()).filter(t => t);

        console.log('\n-----------------------------------');
        console.log('Preview:');
        console.log(`Title: ${title}`);
        console.log(`Content: ${content.substring(0, 100)}...`);
        console.log(`Excerpt: ${excerpt}`);
        console.log(`Tags: ${tags.join(', ')}`);
        console.log(`Publish: ${publish ? 'Yes' : 'No (Draft only)'}`);
        console.log('-----------------------------------\n');

        const confirm = await question('✅ Post this to your blog? (yes/no): ');
        
        if (confirm.toLowerCase().startsWith('y')) {
            await createBlogPost({
                title,
                content,
                excerpt,
                publish,
                tags
            });
        } else {
            console.log('\n❌ Post cancelled.');
        }

    } catch (error) {
        console.error('Error:', error.message);
    } finally {
        rl.close();
    }
}

interactivePost();
