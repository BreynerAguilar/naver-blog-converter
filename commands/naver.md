---
description: Convert markdown to Naver blog HTML with auto-upload to GCS
argument-hint: <filename>
---

Convert markdown file to Naver blog format with automatic Google Cloud Storage upload.

Usage: /naver <filename>

Example: /naver "1011 산일전기와 전력 시장 공급망 분석.md"

Steps:
1. Find the markdown file in the vault (prioritize 글감/ folder if no path given)
2. Run converter with GCS auto-upload:
   ```bash
   cd /path/to/naver-blog-converter && \
   uv run python md2naver.py "<full-path-to-file>" --gcs
   ```
3. Show conversion output summary with image upload status
4. Explain the result:
   - Mermaid diagrams rendered to PNG
   - Images automatically uploaded to GCS
   - HTML generated with real GCS URLs (no placeholders!)
   - Ready to copy-paste into Naver blog immediately
5. Provide next steps:
   - Open the HTML file from the generated naver_FILENAME_TIMESTAMP/ folder
   - Copy all content (Cmd+A, Cmd+C)
   - Paste into Naver blog editor (use DevTools F12 method if needed)
   - Images will work immediately - no manual URL replacement needed!

Important:
- If filename doesn't include path, search in common folders (글감/, writing/, posts/, etc.)
- Images are hosted at: https://storage.googleapis.com/YOUR-BUCKET/naverblog/
- Show the exact path to the output HTML file
- Mention that images are publicly accessible and permanent

Technical Details:
- Uses Google Cloud Storage for image hosting
- Mermaid diagrams auto-rendered with mmdc
- Tables styled with borders and padding
- Bold text with inline styles for Naver compatibility
- No blank space above horizontal rules (구분선)
