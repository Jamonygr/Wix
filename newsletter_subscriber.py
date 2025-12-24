"""
Newsletter Subscriber API for BeyondCloudWithChriz.com
Adds subscribers to your Wix Contacts list via API
"""

import os
import json
import requests
from datetime import datetime

# Load credentials
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
ACCOUNT_ID = CONFIG.get('WIX_ACCOUNT_ID', '')

HEADERS = {
    'Authorization': API_KEY,
    'wix-site-id': SITE_ID,
    'wix-account-id': ACCOUNT_ID,
    'Content-Type': 'application/json',
}


def add_subscriber(email, name=None):
    """
    Add a new subscriber to your Wix Contacts list.
    
    Args:
        email: Subscriber's email address
        name: Optional subscriber name
    
    Returns:
        dict with success status and contact info
    """
    print(f'\n📧 Adding subscriber: {email}')
    
    url = 'https://www.wixapis.com/contacts/v4/contacts'
    
    contact_data = {
        'info': {
            'emails': {
                'items': [
                    {
                        'email': email,
                        'primary': True,
                        'tag': 'MAIN'
                    }
                ]
            }
        }
    }
    
    # Add name if provided
    if name:
        parts = name.split(' ', 1)
        contact_data['info']['name'] = {
            'first': parts[0],
            'last': parts[1] if len(parts) > 1 else ''
        }
    
    try:
        response = requests.post(url, headers=HEADERS, json=contact_data)
        
        if response.status_code in [200, 201]:
            data = response.json()
            contact_id = data.get('contact', {}).get('id', 'unknown')
            print(f'✅ Subscriber added successfully!')
            print(f'   Contact ID: {contact_id}')
            return {
                'success': True,
                'contact_id': contact_id,
                'email': email
            }
        else:
            print(f'❌ Error: {response.status_code}')
            print(f'   Response: {response.text}')
            
            # Check if contact already exists
            if 'ALREADY_EXISTS' in response.text or 'duplicate' in response.text.lower():
                print('ℹ️  This email is already subscribed!')
                return {
                    'success': True,
                    'already_exists': True,
                    'email': email
                }
            
            return {
                'success': False,
                'error': response.text
            }
            
    except Exception as e:
        print(f'❌ Exception: {e}')
        return {
            'success': False,
            'error': str(e)
        }


def list_subscribers():
    """List all contacts (subscribers)."""
    print('\n📋 Fetching subscribers...')
    
    url = 'https://www.wixapis.com/contacts/v4/contacts/query'
    
    query_data = {
        'query': {}
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=query_data)
        
        if response.status_code == 200:
            data = response.json()
            contacts = data.get('contacts', [])
            
            print(f'\n✅ Found {len(contacts)} subscribers:\n')
            for i, contact in enumerate(contacts, 1):
                emails = contact.get('info', {}).get('emails', {}).get('items', [])
                email = emails[0].get('email') if emails else 'No email'
                name = contact.get('info', {}).get('name', {})
                full_name = f"{name.get('first', '')} {name.get('last', '')}".strip() or 'Anonymous'
                print(f'  {i}. {email} ({full_name})')
            
            return contacts
        else:
            print(f'❌ Error: {response.status_code}')
            print(f'   Response: {response.text}')
            return []
            
    except Exception as e:
        print(f'❌ Exception: {e}')
        return []


def create_newsletter_label():
    """Create the newsletter-subscriber label if it doesn't exist."""
    print('\n🏷️  Creating newsletter label...')
    
    url = 'https://www.wixapis.com/contacts/v4/labels'
    
    label_data = {
        'label': {
            'key': 'custom.newsletter-subscriber',
            'displayName': 'Newsletter Subscriber',
            'labelType': 'USER_DEFINED'
        }
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=label_data)
        
        if response.status_code in [200, 201]:
            print('✅ Label created successfully!')
            return True
        elif 'ALREADY_EXISTS' in response.text:
            print('ℹ️  Label already exists')
            return True
        else:
            print(f'⚠️  Label creation: {response.status_code}')
            print(f'   (This is OK if the label already exists)')
            return True
            
    except Exception as e:
        print(f'❌ Exception: {e}')
        return False


# ============================================================
# CLI Interface
# ============================================================

if __name__ == "__main__":
    import sys
    
    print("\n" + "="*50)
    print("  📧 Newsletter Subscriber Manager")
    print("  BeyondCloudWithChriz.com")
    print("="*50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'add' and len(sys.argv) > 2:
            email = sys.argv[2]
            name = sys.argv[3] if len(sys.argv) > 3 else None
            add_subscriber(email, name)
            
        elif command == 'list':
            list_subscribers()
            
        elif command == 'setup':
            create_newsletter_label()
            
        else:
            print("\nUsage:")
            print("  python newsletter_subscriber.py add <email> [name]")
            print("  python newsletter_subscriber.py list")
            print("  python newsletter_subscriber.py setup")
    else:
        # Interactive mode
        print("\n1. Add subscriber")
        print("2. List subscribers")
        print("3. Setup (create label)")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            email = input("Email: ").strip()
            name = input("Name (optional): ").strip()
            if email:
                add_subscriber(email, name if name else None)
        elif choice == '2':
            list_subscribers()
        elif choice == '3':
            create_newsletter_label()
