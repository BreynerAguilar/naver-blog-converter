#!/usr/bin/env python3
"""
Markdown to Naver Blog Converter v2

Two-step workflow:
1. First run: Generate images
2. Upload images to Naver, get URLs
3. Second run: Generate HTML with real URLs

Usage:
    # Step 1: Generate images
    python md2naver_v2.py input.md

    # Step 2: After uploading, generate HTML with URLs
    python md2naver_v2.py input.md --image-urls url1 url2 url3
"""

import argparse
import sys
from pathlib import Path
from md2naver import NaverBlogConverter


class NaverBlogConverterV2(NaverBlogConverter):
    """Extended converter that accepts pre-uploaded image URLs."""

    def __init__(self, input_file: str, output_dir: str = None, image_urls: list = None):
        super().__init__(input_file, output_dir)
        self.image_urls = image_urls or []

    def extract_mermaid_blocks(self, content: str) -> str:
        """Override to use actual URLs if provided."""
        import re

        def replace_mermaid(match):
            self.mermaid_counter += 1
            mermaid_code = match.group(1)

            # Use actual URL if provided, otherwise placeholder
            if self.image_urls and self.mermaid_counter <= len(self.image_urls):
                url = self.image_urls[self.mermaid_counter - 1]
                placeholder_html = f'<img src="{url}" alt="Mermaid Diagram {self.mermaid_counter}" />'
            else:
                placeholder_html = f"![Mermaid Diagram {self.mermaid_counter}](MERMAID_IMAGE_{self.mermaid_counter})"

            self.mermaid_blocks.append({
                'number': self.mermaid_counter,
                'code': mermaid_code,
                'placeholder': f"MERMAID_IMAGE_{self.mermaid_counter}" if not self.image_urls else url
            })

            return placeholder_html

        pattern = r'```mermaid\s*\n(.*?)\n```'
        return re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)


def main():
    parser = argparse.ArgumentParser(
        description="Convert markdown to Naver blog HTML (v2 - with URL support)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Two-step workflow:

Step 1: Generate images
  python md2naver_v2.py article.md

Step 2: Upload to Naver, then regenerate with URLs
  python md2naver_v2.py article.md --image-urls URL1 URL2 URL3
        """
    )
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('-o', '--output', help='Output directory')
    parser.add_argument('--image-urls', nargs='+', help='Naver CDN URLs for mermaid images (in order)')

    args = parser.parse_args()

    try:
        if args.image_urls:
            print(f"Mode: Generating HTML with {len(args.image_urls)} provided image URLs")
            converter = NaverBlogConverterV2(args.input, args.output, args.image_urls)
        else:
            print("Mode: Generating images (Step 1)")
            print("After this, upload images to Naver and re-run with --image-urls")
            converter = NaverBlogConverter(args.input, args.output)

        converter.convert()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
