#!/usr/bin/env python3
"""
Markdown to Naver Blog Converter

Transforms markdown files into Naver blog-compatible HTML with:
- Mermaid diagram conversion to images
- Table HTML conversion
- Frontmatter stripping
- WikiLink conversion
- Code block preservation

Usage:
    python md2naver.py input.md
    python md2naver.py input.md -o output_dir
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

try:
    import markdown
    from markdown.extensions import tables, fenced_code, codehilite
except ImportError:
    print("ERROR: Required package 'markdown' not found.")
    print("Install with: pip install markdown")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Required package 'beautifulsoup4' not found.")
    print("Install with: pip install beautifulsoup4")
    sys.exit(1)


class NaverBlogConverter:
    def __init__(self, input_file: str, output_dir: str = None, use_gcs: bool = False,
                 gcs_project: str = None, gcs_bucket: str = None):
        self.input_file = Path(input_file)
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        # Setup output directory
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            # Use filename (without .md) as base for output directory
            base_name = self.input_file.stem  # Gets filename without extension
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_dir = Path(f"naver_{base_name}_{timestamp}")

        self.output_dir.mkdir(exist_ok=True)
        self.images_dir = self.output_dir / "images"
        self.images_dir.mkdir(exist_ok=True)

        self.mermaid_counter = 0
        self.mermaid_blocks = []
        self.code_blocks = []

        # GCS configuration
        self.use_gcs = use_gcs

        # Load from config if not provided
        if use_gcs:
            from config import GCS_PROJECT_ID, GCS_BUCKET_NAME
            self.gcs_project = gcs_project or GCS_PROJECT_ID
            self.gcs_bucket = gcs_bucket or GCS_BUCKET_NAME

            if not self.gcs_project or not self.gcs_bucket:
                raise ValueError(
                    "GCS project and bucket must be specified via:\n"
                    "  1. Command-line args: --gcs-project and --gcs-bucket\n"
                    "  2. Environment variables: GCS_PROJECT_ID and GCS_BUCKET_NAME\n"
                    "  3. .env file with the above variables"
                )
        else:
            self.gcs_project = gcs_project
            self.gcs_bucket = gcs_bucket

        self.gcs_uploader = None
        self.gcs_image_urls = {}

    def read_file(self) -> str:
        """Read the input markdown file."""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            return f.read()

    def strip_frontmatter(self, content: str) -> str:
        """Remove YAML frontmatter from markdown."""
        # Match frontmatter: starts with ---, ends with ---
        pattern = r'^---\s*\n.*?\n---\s*\n'
        return re.sub(pattern, '', content, flags=re.DOTALL)

    def extract_mermaid_blocks(self, content: str) -> str:
        """Extract mermaid code blocks and replace with image placeholders."""
        def replace_mermaid(match):
            self.mermaid_counter += 1
            mermaid_code = match.group(1)

            # Use GCS URL if available, otherwise placeholder
            image_filename = f"mermaid_{self.mermaid_counter}.png"
            if self.use_gcs and image_filename in self.gcs_image_urls:
                url = self.gcs_image_urls[image_filename]
                placeholder = f'<img src="{url}" alt="Mermaid Diagram {self.mermaid_counter}" />'
            else:
                placeholder = f"![Mermaid Diagram {self.mermaid_counter}](MERMAID_IMAGE_{self.mermaid_counter})"

            self.mermaid_blocks.append({
                'number': self.mermaid_counter,
                'code': mermaid_code,
                'placeholder': f"MERMAID_IMAGE_{self.mermaid_counter}",
                'filename': image_filename
            })

            return placeholder

        # Match ```mermaid ... ```
        pattern = r'```mermaid\s*\n(.*?)\n```'
        return re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)

    def extract_code_blocks(self, content: str) -> str:
        """Extract code blocks for manual Color Scripter processing."""
        def replace_code(match):
            lang = match.group(1) or 'text'
            code = match.group(2)
            block_num = len(self.code_blocks) + 1

            self.code_blocks.append({
                'number': block_num,
                'language': lang,
                'code': code
            })

            # Keep the code block but add a marker
            return f"```{lang}\n{code}\n```\n<!-- CODE_BLOCK_{block_num} -->"

        # Match ```lang ... ``` (but not mermaid, already handled)
        pattern = r'```(\w+)?\s*\n(.*?)\n```'
        return re.sub(pattern, replace_code, content, flags=re.DOTALL)

    def convert_wikilinks(self, content: str) -> str:
        """Convert Obsidian WikiLinks to plain text."""
        # Convert [[link]] to just "link"
        return re.sub(r'\[\[([^\]]+)\]\]', r'\1', content)

    def render_mermaid_to_image(self, mermaid_code: str, output_path: str) -> bool:
        """Render mermaid diagram to PNG using mermaid-cli (mmdc)."""
        # Check if mmdc is available
        try:
            subprocess.run(['mmdc', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

        # Create temporary mermaid file
        temp_mmd = self.output_dir / "temp.mmd"
        with open(temp_mmd, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)

        try:
            # Render with mmdc
            subprocess.run([
                'mmdc',
                '-i', str(temp_mmd),
                '-o', str(output_path),
                '-b', 'transparent',
                '-s', '2'  # 2x scale for better quality
            ], check=True, capture_output=True)
            temp_mmd.unlink()
            return True
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to render mermaid diagram: {e}")
            temp_mmd.unlink()
            return False

    def convert_to_html(self, content: str) -> str:
        """Convert markdown to HTML."""
        md = markdown.Markdown(extensions=[
            'tables',
            'fenced_code',
            'nl2br',
            'sane_lists'
        ])
        return md.convert(content)

    def clean_html(self, html: str) -> str:
        """Clean HTML for Naver blog compatibility."""
        soup = BeautifulSoup(html, 'html.parser')

        # Remove any script tags (shouldn't be any, but safety first)
        for script in soup.find_all('script'):
            script.decompose()

        # Remove iframe tags
        for iframe in soup.find_all('iframe'):
            iframe.decompose()

        # Add inline styles to bold tags to ensure they work in Naver
        for strong in soup.find_all(['strong', 'b']):
            strong['style'] = 'font-weight: bold;'

        # Add inline styles to italic tags
        for em in soup.find_all(['em', 'i']):
            em['style'] = 'font-style: italic;'

        # Style tables for better appearance in Naver
        for table in soup.find_all('table'):
            table['style'] = 'border-collapse: collapse; width: 100%; margin: 10px 0;'

            # Style table headers
            for th in table.find_all('th'):
                th['style'] = 'border: 1px solid #ddd; padding: 12px; background-color: #f2f2f2; font-weight: bold; text-align: left;'

            # Style table cells
            for td in table.find_all('td'):
                td['style'] = 'border: 1px solid #ddd; padding: 12px; text-align: left;'

        # Add blank paragraphs between elements for better spacing in Naver
        # Find all paragraph tags and add spacing
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'blockquote', 'pre', 'table']):
            # Don't add spacing if next element is <hr> (구분선 doesn't need top spacing)
            next_tag = tag.find_next_sibling()
            if next_tag and next_tag.name == 'hr':
                continue

            # Add a blank paragraph after each major block element
            blank_p = soup.new_tag('p')
            blank_p.string = '\u00A0'  # Non-breaking space
            if tag.next_sibling:
                tag.insert_after(blank_p)

        return str(soup)

    def generate_instructions(self) -> str:
        """Generate manual steps instructions."""
        instructions = ["# Manual Steps for Naver Blog Upload\n\n"]

        if self.mermaid_blocks:
            instructions.append("## Step 1: Upload Mermaid Diagram Images\n\n")
            instructions.append("The following mermaid diagrams have been converted to images:\n\n")
            for block in self.mermaid_blocks:
                img_file = f"mermaid_{block['number']}.png"
                img_exists = (self.images_dir / img_file).exists()
                status = "✓ Generated" if img_exists else "✗ Failed (see mermaid_code.txt)"
                instructions.append(f"{block['number']}. {img_file} - {status}\n")

            instructions.append("\n**Actions:**\n")
            instructions.append("1. Upload all PNG files from `images/` folder to Naver blog\n")
            instructions.append("2. Copy each image's Naver CDN URL\n")
            instructions.append("3. In the HTML file, replace `MERMAID_IMAGE_N` with actual URLs\n")
            instructions.append("   Example: Replace `MERMAID_IMAGE_1` with `https://blogpfthumb-phinf.pstatic.net/...`\n\n")

        if self.code_blocks:
            instructions.append("## Step 2: (Optional) Enhanced Code Syntax Highlighting\n\n")
            instructions.append("For better code highlighting, use Color Scripter:\n\n")
            instructions.append("1. Go to https://colorscripter.com/\n")
            instructions.append("2. For each code block below, paste code into Color Scripter\n")
            instructions.append("3. Select the correct language\n")
            instructions.append("4. Click '코드 HTML로 복사' (Copy code as HTML)\n")
            instructions.append("5. In the HTML file, replace the `<!-- CODE_BLOCK_N -->` marker with Color Scripter HTML\n\n")

            instructions.append("**Code Blocks:**\n\n")
            for block in self.code_blocks:
                instructions.append(f"### Code Block {block['number']} (Language: {block['language']})\n")
                instructions.append("```" + block['language'] + "\n")
                instructions.append(block['code'])
                instructions.append("\n```\n\n")

        instructions.append("## Step 3: Paste HTML into Naver Blog\n\n")
        instructions.append("**Method A: Using Browser DevTools** (Recommended)\n")
        instructions.append("1. Open Naver Blog post editor\n")
        instructions.append("2. Press F12 to open DevTools\n")
        instructions.append("3. Find the content editable div in Elements panel\n")
        instructions.append("4. Right-click → Edit as HTML\n")
        instructions.append("5. Paste the HTML from `output.html`\n")
        instructions.append("6. Close DevTools\n")
        instructions.append("7. Preview and publish\n\n")

        instructions.append("**Method B: Using M2N** (If Method A doesn't work)\n")
        instructions.append("1. Go to https://m2n.coderred.com\n")
        instructions.append("2. Paste the HTML from `output.html`\n")
        instructions.append("3. Follow M2N instructions to paste into Naver blog\n\n")

        instructions.append("## Important Notes\n\n")
        instructions.append("- Do NOT edit the post in Naver's WYSIWYG editor after pasting HTML\n")
        instructions.append("- If you need to make changes, edit the original markdown and re-convert\n")
        instructions.append("- Always preview before publishing\n")
        instructions.append("- Keep the original markdown file as your source of truth\n\n")

        instructions.append("## Quick Helper Script\n\n")
        instructions.append("To replace image placeholders automatically:\n\n")
        instructions.append("```bash\n")
        script_dir = Path(__file__).parent.resolve()
        instructions.append(f"cd {script_dir}\n")
        instructions.append(f"uv run python update_image_urls.py {self.output_dir}/output.html\n")
        instructions.append("```\n\n")
        instructions.append("This script will interactively prompt you for each Naver CDN URL.\n")

        return ''.join(instructions)

    def convert(self):
        """Main conversion process."""
        print(f"Converting: {self.input_file}")
        print(f"Output directory: {self.output_dir}\n")

        # Read file
        content = self.read_file()

        # Step 1: Strip frontmatter
        print("Step 1: Removing frontmatter...")
        content = self.strip_frontmatter(content)

        # Step 2: Extract mermaid blocks
        print("Step 2: Extracting mermaid diagrams...")
        content = self.extract_mermaid_blocks(content)

        # Step 3: Convert WikiLinks
        print("Step 3: Converting WikiLinks...")
        content = self.convert_wikilinks(content)

        # Step 4: Extract code blocks (for reference)
        print("Step 4: Extracting code blocks...")
        content = self.extract_code_blocks(content)

        # Step 5: Convert to HTML
        print("Step 5: Converting markdown to HTML...")
        html = self.convert_to_html(content)

        # Step 6: Clean HTML
        print("Step 6: Cleaning HTML for Naver compatibility...")
        html = self.clean_html(html)

        # Step 7: Render mermaid diagrams
        if self.mermaid_blocks:
            print(f"Step 7: Rendering {len(self.mermaid_blocks)} mermaid diagrams...")
            for block in self.mermaid_blocks:
                img_path = self.images_dir / f"mermaid_{block['number']}.png"
                success = self.render_mermaid_to_image(block['code'], img_path)
                if success:
                    print(f"  ✓ Rendered mermaid diagram {block['number']}")
                else:
                    print(f"  ✗ Failed to render diagram {block['number']} (mmdc not available)")

            # Save mermaid code for manual rendering if needed
            mermaid_file = self.output_dir / "mermaid_code.txt"
            with open(mermaid_file, 'w', encoding='utf-8') as f:
                for block in self.mermaid_blocks:
                    f.write(f"=== Diagram {block['number']} ===\n")
                    f.write(block['code'])
                    f.write("\n\n")
            print(f"  Saved mermaid code to: {mermaid_file}")

            # Step 7.5: Upload to GCS if enabled
            if self.use_gcs:
                print(f"\nStep 7.5: Uploading images to Google Cloud Storage...")
                try:
                    from gcs_uploader import GCSUploader
                    from config import GCS_SUBFOLDER
                    self.gcs_uploader = GCSUploader(self.gcs_project, self.gcs_bucket)

                    if not self.gcs_uploader.ensure_bucket_exists():
                        print("  ✗ Failed to initialize GCS bucket")
                        print("  Continuing without GCS upload...")
                    else:
                        # Use configured subfolder with trailing slash
                        prefix = f"{GCS_SUBFOLDER}/" if GCS_SUBFOLDER else ""
                        self.gcs_image_urls = self.gcs_uploader.upload_images_from_dir(self.images_dir, prefix=prefix)
                        print(f"  ✓ Uploaded {len(self.gcs_image_urls)} images to GCS")

                        # Now replace placeholders in HTML with actual URLs
                        print("\nStep 7.6: Replacing placeholders with GCS URLs...")
                        for filename, url in self.gcs_image_urls.items():
                            # Extract number from filename (e.g., mermaid_1.png -> 1)
                            number = filename.replace('mermaid_', '').replace('.png', '')
                            placeholder = f"MERMAID_IMAGE_{number}"
                            html = html.replace(placeholder, url)
                        print("  ✓ HTML updated with GCS URLs")

                except ImportError:
                    print("  ✗ GCS uploader not available (run: uv sync)")
                    print("  Continuing without GCS upload...")
                except Exception as e:
                    print(f"  ✗ GCS upload failed: {e}")
                    print("  Continuing without GCS upload...")

        # Step 8: Save output
        print("\nStep 8: Saving output files...")

        # Use input filename as base for output files
        base_name = self.input_file.stem

        # Save HTML
        html_file = self.output_dir / f"{base_name}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  ✓ HTML: {html_file}")

        # Save instructions
        instructions_file = self.output_dir / f"{base_name}_INSTRUCTIONS.md"
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_instructions())
        print(f"  ✓ Instructions: {instructions_file}")

        # Summary
        print(f"\n{'='*60}")
        print("Conversion Complete!")
        print(f"{'='*60}")
        print(f"Output directory: {self.output_dir}")
        print(f"HTML file: output.html")
        print(f"Instructions: INSTRUCTIONS.md")
        if self.mermaid_blocks:
            print(f"Mermaid diagrams: {len(self.mermaid_blocks)} PNG files in images/ folder")
        if self.code_blocks:
            print(f"Code blocks: {len(self.code_blocks)} (see INSTRUCTIONS.md for Color Scripter steps)")
        print(f"\n{'='*60}")
        print("NEXT STEPS:")
        print(f"{'='*60}")
        if self.use_gcs and self.gcs_image_urls:
            print("✓ Images uploaded to GCS - HTML ready to paste!")
            print("1. Open the HTML file from the output directory")
            print("2. Copy all content (Cmd+A, Cmd+C)")
            print("3. Paste into Naver blog via DevTools (F12)")
            print("4. Preview and publish")
        else:
            print("1. Upload PNG images from images/ to Naver blog editor")
            print("2. Get CDN URLs (right-click image → Copy image address)")
            print("3. Run helper script to replace placeholders:")
            script_dir = Path(__file__).parent.resolve()
            print(f"   cd {script_dir}")
            print(f"   uv run python update_image_urls.py {self.output_dir}/output.html")
            print("4. Paste updated HTML into Naver blog via DevTools (F12)")
        print(f"\nFull instructions: {self.output_dir}/INSTRUCTIONS.md")
        print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert markdown files to Naver blog-compatible HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python md2naver.py article.md
  python md2naver.py article.md -o my_output
  python md2naver.py article.md --gcs  # Auto-upload to Google Cloud Storage

For more info, see README.md and GCS_SETUP.md
        """
    )
    parser.add_argument('input', help='Input markdown file path')
    parser.add_argument('-o', '--output', help='Output directory (default: naver_output_TIMESTAMP)')
    parser.add_argument('--gcs', action='store_true', help='Upload images to Google Cloud Storage')
    parser.add_argument('--gcs-project', help='GCS project ID (required with --gcs, or set GCS_PROJECT_ID env var)')
    parser.add_argument('--gcs-bucket', help='GCS bucket name (required with --gcs, or set GCS_BUCKET_NAME env var)')

    args = parser.parse_args()

    try:
        converter = NaverBlogConverter(
            args.input,
            args.output,
            use_gcs=args.gcs,
            gcs_project=args.gcs_project,
            gcs_bucket=args.gcs_bucket
        )
        converter.convert()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
