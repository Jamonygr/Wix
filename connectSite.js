import 'dotenv/config';
import fs from 'fs';
import path from 'path';
import readline from 'readline';

const API_KEY = process.env.WIX_API_KEY;
const SITE_URL = process.env.WIX_SITE_URL || 'https://www.beyondcloudwithchriz.com';

function normalizeDomain(value) {
    if (!value) {
        return '';
    }

    let normalized = value.trim().toLowerCase();
    normalized = normalized.replace(/^https?:\/\//, '');
    normalized = normalized.replace(/^www\./, '');
    return normalized.split('/')[0];
}

function upsertEnv(lines, key, value) {
    let found = false;
    const updated = lines.map((line) => {
        if (line.startsWith(`${key}=`)) {
            found = true;
            return `${key}=${value}`;
        }
        return line;
    });

    if (!found) {
        updated.push(`${key}=${value}`);
    }

    return updated;
}

async function main() {
    if (!API_KEY) {
        console.error('WIX_API_KEY is missing in .env.');
        console.error('Add WIX_API_KEY=your-api-key and rerun.');
        process.exit(1);
    }

    const response = await fetch('https://www.wixapis.com/site-list/v2/sites/query', {
        method: 'POST',
        headers: {
            Authorization: API_KEY,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: {} }),
    });

    if (!response.ok) {
        const errorText = await response.text();
        console.error('Sites API error:', response.status, errorText);
        process.exit(1);
    }

    const data = await response.json();
    const sites = data.sites || [];

    if (sites.length === 0) {
        console.error('No sites found for this API key.');
        process.exit(1);
    }

    console.log('Available sites:');
    sites.forEach((site, index) => {
        console.log(`${index + 1}. ${site.displayName || 'Unnamed Site'}`);
        console.log(`   Site ID: ${site.id}`);
        console.log(`   URL: ${site.siteUrl || 'N/A'}`);
    });

    const targetDomain = normalizeDomain(SITE_URL);
    let selectedSite = sites.find((site) => normalizeDomain(site.siteUrl) === targetDomain);

    if (!selectedSite && sites.length === 1) {
        selectedSite = sites[0];
    }

    let rl;
    const ask = (question) => {
        if (!rl) {
            rl = readline.createInterface({
                input: process.stdin,
                output: process.stdout,
            });
        }
        return new Promise((resolve) => rl.question(question, resolve));
    };

    try {
        if (!selectedSite) {
            while (!selectedSite) {
                const answer = await ask('Select site number to use: ');
                const index = Number.parseInt(answer, 10);
                if (Number.isInteger(index) && index >= 1 && index <= sites.length) {
                    selectedSite = sites[index - 1];
                    break;
                }
                console.log(`Invalid selection. Enter a number between 1 and ${sites.length}.`);
            }
        }

        console.log(`Selected site: ${selectedSite.displayName || selectedSite.id}`);
        const confirm = await ask('Update .env with WIX_SITE_ID and WIX_SITE_URL? (y/n): ');

        if (!confirm.trim().toLowerCase().startsWith('y')) {
            console.log('Skipped .env update.');
            console.log(`WIX_SITE_ID=${selectedSite.id}`);
            console.log(`WIX_SITE_URL=${selectedSite.siteUrl || SITE_URL}`);
            return;
        }

        const envPath = path.join(process.cwd(), '.env');
        const existing = fs.existsSync(envPath) ? fs.readFileSync(envPath, 'utf8').split(/\r?\n/) : [];
        const updatedId = upsertEnv(existing, 'WIX_SITE_ID', selectedSite.id);
        const finalUrl = selectedSite.siteUrl || SITE_URL;
        const updated = upsertEnv(updatedId, 'WIX_SITE_URL', finalUrl);
        const cleaned = updated.filter((line, idx) => !(idx === updated.length - 1 && line.trim() === ''));

        fs.writeFileSync(envPath, `${cleaned.join('\n')}\n`, 'utf8');

        console.log('Updated .env with site settings.');
    } finally {
        if (rl) {
            rl.close();
        }
    }
}

main().catch((error) => {
    console.error('Error:', error.message);
    process.exit(1);
});
