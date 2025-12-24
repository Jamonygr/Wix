import 'dotenv/config';

const API_KEY = process.env.WIX_API_KEY;
const ACCOUNT_ID = process.env.WIX_ACCOUNT_ID;

async function testConnection() {
    console.log('🔄 Testing connection to Wix API...\n');
    
    try {
        // First, let's query the sites to get the site ID
        const sitesResponse = await fetch('https://www.wixapis.com/site-list/v2/sites/query', {
            method: 'POST',
            headers: {
                'Authorization': API_KEY,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: {}
            })
        });

        if (!sitesResponse.ok) {
            const errorText = await sitesResponse.text();
            console.log('❌ Sites API Error:', sitesResponse.status, errorText);
        } else {
            const sitesData = await sitesResponse.json();
            console.log('✅ Connected to Wix successfully!\n');
            console.log('📋 Your Sites:');
            
            if (sitesData.sites && sitesData.sites.length > 0) {
                sitesData.sites.forEach((site, index) => {
                    console.log(`\n  ${index + 1}. ${site.displayName || 'Unnamed Site'}`);
                    console.log(`     Site ID: ${site.id}`);
                    console.log(`     URL: ${site.siteUrl || 'N/A'}`);
                });
                
                // Save the first site ID for future use
                const siteId = sitesData.sites[0].id;
                console.log(`\n💡 Add this to your .env file:`);
                console.log(`   WIX_SITE_ID=${siteId}`);
            } else {
                console.log('  No sites found.');
            }
        }
        
    } catch (error) {
        console.error('❌ Connection failed:', error.message);
    }
}

testConnection();
