# Wix Blog Automation for BeyondCloudWithChriz.com

Automated blog posting tool for your Wix website.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Test Your Connection
```bash
npm test
```
This will show your Wix sites and give you your **Site ID**. Add it to your `.env` file.

### 3. Update .env with Site ID
After running the test, add the Site ID to your `.env` file:
```
WIX_SITE_ID=your-site-id-here
```

### 4. Post a Blog
```bash
npm run post
```

Or use the interactive mode:
```bash
node easyPost.js
```

## 📁 Files

| File | Description |
|------|-------------|
| `.env` | Your API credentials (KEEP SECRET!) |
| `postBlog.js` | Main blog posting functions |
| `easyPost.js` | Interactive blog poster |
| `testConnection.js` | Test your Wix API connection |
| `components/homepage_fancy_pack.html` | Wix-ready homepage CTA, terminal, start cards, latest posts, and newsletter section |
| `docs/homepage_fancy_pack.md` | Placement notes for the homepage fancy pack |

## 📝 Creating a Blog Post Programmatically

```javascript
import { createBlogPost } from './postBlog.js';

await createBlogPost({
    title: "My Amazing Blog Post",
    content: "This is the content of my blog post...",
    excerpt: "A short description for previews",
    publish: true,  // false = save as draft
    tags: ["tech", "cloud", "azure"]
});
```

## 🔐 Security

- **NEVER share your `.env` file**
- **NEVER commit `.env` to Git** (it's in .gitignore)
- Keep your API key secret

## 📚 Wix Blog API Reference

- [Wix Blog API Docs](https://dev.wix.com/docs/rest/api-reference/wix-blog/posts)
- [Rich Content Format](https://dev.wix.com/docs/rest/api-reference/wix-blog/rich-content)

## 🛠️ Troubleshooting

**"Site ID not found"** - Run `npm test` and add the Site ID to `.env`

**"401 Unauthorized"** - Your API key may have expired. Create a new one at [Wix API Keys](https://manage.wix.com/account/api-keys)

**"403 Forbidden"** - Make sure your API key has Blog permissions (read & write)

---

Made with ❤️ for BeyondCloudWithChriz.com
