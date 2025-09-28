#!/usr/bin/env python3
"""
Script to fetch company logos from Brandfetch API and update placements_data.json
"""

import json
import requests
import time
import sys
from typing import Dict, List, Optional

# Brandfetch API endpoint
BRANDFETCH_API_URL = "https://api.brandfetch.io/v2/search/{query}"

def fetch_company_logo(company_name: str) -> Optional[str]:
    """
    Fetch company logo from Brandfetch API
    
    Args:
        company_name: Name of the company to search for
        
    Returns:
        URL of the first logo found, or None if not found
    """
    try:
        # Clean company name for better search results
        clean_name = company_name.strip()
        
        # Make API request
        url = BRANDFETCH_API_URL.format(query=clean_name)
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if we have results
            if isinstance(data, list) and len(data) > 0:
                # Get the first result's icon
                first_result = data[0]
                if 'icon' in first_result:
                    return first_result['icon']
                    
        print(f"  ❌ No logo found for '{company_name}' (Status: {response.status_code})")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error fetching logo for '{company_name}': {e}")
        return None
    except Exception as e:
        print(f"  ❌ Unexpected error for '{company_name}': {e}")
        return None

def update_placements_data(input_file: str, output_file: str) -> None:
    """
    Update placements data with company logos
    
    Args:
        input_file: Path to input JSON file
        output_file: Path to output JSON file
    """
    try:
        # Load the data
        print(f"📖 Loading data from {input_file}...")
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if not isinstance(data, list):
            print("❌ Error: Expected JSON array")
            return
            
        print(f"📊 Found {len(data)} records to process")
        
        # Process each record
        updated_count = 0
        skipped_count = 0
        
        for i, record in enumerate(data, 1):
            if not isinstance(record, dict):
                print(f"⚠️  Skipping record {i}: Not a valid object")
                skipped_count += 1
                continue
                
            company_name = record.get('NewCompanyName', '').strip()
            
            if not company_name:
                print(f"⚠️  Skipping record {i}: No company name")
                skipped_count += 1
                continue
                
            print(f"\n🔍 Processing {i}/{len(data)}: {company_name}")
            
            # Check if logo already exists and is not a placeholder
            # current_logo = record.get('NewCompanyLogo', '')
            # if current_logo and not any(placeholder in current_logo.lower() for placeholder in ['placeholder', 'default', 'no-image']):
            #     print(f"  ✅ Logo already exists: {current_logo}")
            #     continue
            
            # Fetch new logo
            new_logo = fetch_company_logo(company_name)
            
            if new_logo:
                record['NewCompanyLogo'] = new_logo
                updated_count += 1
                print(f"  ✅ Updated logo: {new_logo}")
            else:
                print(f"  ⚠️  Could not fetch logo for {company_name}")
                skipped_count += 1
            
            # Add small delay to be respectful to the API
            time.sleep(0.5)
        
        # Save updated data
        print(f"\n💾 Saving updated data to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"\n✅ Processing complete!")
        print(f"   📈 Updated: {updated_count} records")
        print(f"   ⚠️  Skipped: {skipped_count} records")
        print(f"   📁 Output saved to: {output_file}")
        
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found")
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in '{input_file}': {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main function"""
    input_file = "placements_data.json"
    output_file = "placements_data_updated.json"
    
    print("🚀 Company Logo Fetcher")
    print("=" * 50)
    
    # Check if input file exists
    try:
        with open(input_file, 'r') as f:
            pass
    except FileNotFoundError:
        print(f"❌ Error: Input file '{input_file}' not found")
        print("Please make sure placements_data.json exists in the current directory")
        sys.exit(1)
    
    # Process the data
    update_placements_data(input_file, output_file)

if __name__ == "__main__":
    main()
