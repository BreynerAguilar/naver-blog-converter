#!/usr/bin/env python3
"""
Create a self-contained HTML file with embedded images (base64 or file paths)
for direct paste into Naver blog editor.

Usage:
    python create_pasteable_html.py naver_output_TIMESTAMP
"""

import sys
import base64
from pathlib import Path


def image_to_base64(image_path: Path) -> str:
    """Convert image file to base64 data URI."""
    with open(image_path, 'rb') as f:
        image_data = f.read()
    b64_data = base64.b64encode(image_data).decode('utf-8')
    return f"data:image/png;base64,{b64_data}"


def create_pasteable_html(output_dir: Path):
    """Create HTML with embedded images for direct paste."""

    html_file = output_dir / "output.html"
    images_dir = output_dir / "images"

    if not html_file.exists():
        print(f"Error: {html_file} not found")
        sys.exit(1)

    if not images_dir.exists():
        print(f"Error: {images_dir} not found")
        sys.exit(1)

    # Read original HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all image files
    image_files = sorted(images_dir.glob("mermaid_*.png"))

    if not image_files:
        print(f"Error: No mermaid_*.png files found in {images_dir}")
        sys.exit(1)

    print(f"\nFound {len(image_files)} images to embed")
    print("Converting images to base64...")

    # Replace each MERMAID_IMAGE_N with base64 data URI
    for i, image_file in enumerate(image_files, 1):
        placeholder = f"MERMAID_IMAGE_{i}"
        print(f"  Processing {image_file.name} ({image_file.stat().st_size // 1024} KB)...")

        base64_uri = image_to_base64(image_file)
        content = content.replace(placeholder, base64_uri)

    # Save pasteable version
    pasteable_file = output_dir / "output_pasteable.html"
    with open(pasteable_file, 'w', encoding='utf-8') as f:
        f.write(content)

    file_size = pasteable_file.stat().st_size
    print(f"\n{'='*60}")
    print("✓ Created pasteable HTML with embedded images")
    print(f"{'='*60}")
    print(f"File: {pasteable_file}")
    print(f"Size: {file_size // 1024} KB")
    print(f"\nNext steps:")
    print("1. Open the file in a web browser to verify images show")
    print("2. Select all content (Cmd+A)")
    print("3. Copy (Cmd+C)")
    print("4. Paste into Naver blog editor")
    print("\nNote: Naver may strip base64 images. If it doesn't work,")
    print("      you'll need to upload images manually and use CDN URLs.")
    print(f"{'='*60}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python create_pasteable_html.py <output_directory>")
        print("\nExample:")
        print("  python create_pasteable_html.py naver_output_20251012_153527")
        sys.exit(1)

    output_dir = Path(sys.argv[1])

    if not output_dir.exists():
        print(f"Error: Directory not found: {output_dir}")
        sys.exit(1)

    create_pasteable_html(output_dir)


if __name__ == '__main__':
    main()
