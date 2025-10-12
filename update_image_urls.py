#!/usr/bin/env python3
"""
Helper script to replace MERMAID_IMAGE_N placeholders with actual Naver CDN URLs

After uploading images to Naver blog, use this script to update the HTML file.

Usage:
    python update_image_urls.py output_dir/output.html

    Then paste the Naver CDN URLs when prompted.
"""

import sys
import re
from pathlib import Path


def update_image_urls(html_file: Path):
    """Interactively replace image placeholders with Naver CDN URLs."""

    if not html_file.exists():
        print(f"Error: File not found: {html_file}")
        sys.exit(1)

    # Read HTML content
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all MERMAID_IMAGE_N placeholders
    placeholders = re.findall(r'MERMAID_IMAGE_\d+', content)

    if not placeholders:
        print("No MERMAID_IMAGE placeholders found in the HTML file.")
        return

    # Remove duplicates and sort
    placeholders = sorted(set(placeholders))

    print(f"\nFound {len(placeholders)} image placeholders to replace:\n")
    for placeholder in placeholders:
        print(f"  - {placeholder}")

    print("\n" + "="*60)
    print("INSTRUCTIONS:")
    print("="*60)
    print("1. Open Naver Blog post editor")
    print("2. Upload each PNG file from the images/ folder")
    print("3. After upload, right-click on the image → 'Copy image address'")
    print("4. Paste the URL here when prompted")
    print("\nNaver CDN URLs look like:")
    print("  https://postfiles.pstatic.net/...")
    print("  or")
    print("  https://blogpfthumb-phinf.pstatic.net/...")
    print("="*60 + "\n")

    # Collect URLs for each placeholder
    url_map = {}
    for placeholder in placeholders:
        while True:
            url = input(f"\nEnter Naver CDN URL for {placeholder}:\n> ").strip()

            if not url:
                print("  ⚠️  URL cannot be empty. Try again.")
                continue

            if not url.startswith('http'):
                print("  ⚠️  URL should start with http:// or https://. Try again.")
                continue

            if 'pstatic.net' not in url:
                confirm = input(f"  ⚠️  This doesn't look like a Naver CDN URL. Use anyway? (y/n): ").strip().lower()
                if confirm != 'y':
                    continue

            url_map[placeholder] = url
            print(f"  ✓ Saved URL for {placeholder}")
            break

    # Replace placeholders in content
    original_content = content
    for placeholder, url in url_map.items():
        content = content.replace(placeholder, url)

    if content == original_content:
        print("\n⚠️  No replacements were made. Check your URLs.")
        return

    # Save updated HTML
    backup_file = html_file.with_suffix('.html.backup')
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(original_content)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("\n" + "="*60)
    print("✓ SUCCESS!")
    print("="*60)
    print(f"Updated: {html_file}")
    print(f"Backup:  {backup_file}")
    print(f"Replaced {len(url_map)} image placeholders")
    print("\nNext steps:")
    print("1. Open the updated output.html")
    print("2. Copy the entire HTML content")
    print("3. Use DevTools (F12) to paste into Naver blog editor")
    print("="*60)


def main():
    if len(sys.argv) != 2:
        print("Usage: python update_image_urls.py <output_dir>/output.html")
        print("\nExample:")
        print("  python update_image_urls.py naver_output_20251012_153527/output.html")
        sys.exit(1)

    html_file = Path(sys.argv[1])
    update_image_urls(html_file)


if __name__ == '__main__':
    main()
