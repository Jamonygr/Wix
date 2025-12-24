const { chromium } = require('playwright');

(async () => {
    console.log('🚀 Starting Wix Editor automation...');
    console.log('');
    
    const browser = await chromium.launch({ 
        headless: false,
        slowMo: 300
    });
    
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    
    const page = await context.newPage();
    
    try {
        // Go directly to Wix editor
        console.log('📂 Opening Wix site manager...');
        await page.goto('https://manage.wix.com/dashboard');
        
        // Wait for login/dashboard to load
        console.log('⏳ Waiting for Wix to load (30 seconds)...');
        await page.waitForTimeout(30000);
        
        // Try to click on the site
        console.log('🔍 Looking for your site...');
        try {
            await page.click('text="beyondcloudwithchriz"', { timeout: 5000 });
            console.log('✅ Found site, clicking...');
            await page.waitForTimeout(3000);
        } catch (e) {
            console.log('ℹ️  Could not auto-click site');
        }
        
        // Try to click Edit Site
        console.log('🔍 Looking for Edit Site button...');
        try {
            await page.click('text="Edit Site"', { timeout: 5000 });
            console.log('✅ Clicked Edit Site');
            await page.waitForTimeout(10000);
        } catch (e) {
            console.log('ℹ️  Could not find Edit Site button');
        }
        
        // Now in editor - try to click Add
        console.log('🔍 Looking for Add button in editor...');
        try {
            // Try different selectors for Add button
            const addSelectors = [
                '[data-hook="add-panel-opener"]',
                'button:has-text("Add")',
                '[aria-label="Add"]',
                '.add-panel-btn'
            ];
            
            for (const selector of addSelectors) {
                try {
                    await page.click(selector, { timeout: 3000 });
                    console.log('✅ Clicked Add button');
                    await page.waitForTimeout(2000);
                    break;
                } catch (e) {
                    continue;
                }
            }
        } catch (e) {
            console.log('ℹ️  Could not find Add button');
        }
        
        // Try to find Embed Code
        console.log('🔍 Looking for Embed Code...');
        try {
            await page.click('text="Embed Code"', { timeout: 5000 });
            console.log('✅ Clicked Embed Code');
            await page.waitForTimeout(1500);
            
            await page.click('text="Embed HTML"', { timeout: 5000 });
            console.log('✅ Clicked Embed HTML');
            await page.waitForTimeout(2000);
        } catch (e) {
            console.log('ℹ️  Could not find Embed options');
        }
        
        // Copy subscribe code to clipboard
        const subscribeCode = `<div style="text-align:center;padding:30px"><h3 style="color:#00ffff;text-shadow:0 0 10px rgba(0,255,255,0.8)">🎮 Join the Grid</h3><p style="color:#aaa;margin:15px 0">Get Azure updates in your inbox</p><input id="e" placeholder="Your email" style="padding:15px;border:2px solid #ff00ff;border-radius:5px;background:#0d0620;color:#fff;width:250px"><button onclick="alert('Subscribed: '+document.getElementById('e').value)" style="padding:15px 30px;margin-left:10px;background:linear-gradient(135deg,#ff00ff,#00ffff);border:none;border-radius:5px;color:#fff;font-weight:bold;cursor:pointer">Subscribe</button></div>`;
        
        await page.evaluate((code) => {
            navigator.clipboard.writeText(code);
        }, subscribeCode);
        
        console.log('');
        console.log('📋 Subscribe code copied to clipboard!');
        console.log('');
        console.log('👉 If the Embed HTML dialog is open, press Ctrl+V to paste');
        console.log('👉 Position the element below the music player');
        console.log('👉 Click Publish when done');
        console.log('');
        console.log('🔄 Browser will stay open. Close it manually when finished.');
        
        // Keep browser open for 10 minutes
        await page.waitForTimeout(600000);
        
    } catch (error) {
        console.error('❌ Error:', error.message);
        // Keep browser open anyway
        await page.waitForTimeout(600000);
    }
})();
