# Naver Blog Converter with Google Cloud Storage

Transform Obsidian markdown files with mermaid diagrams into Naver blog-compatible HTML with automatic image hosting on Google Cloud Storage.

## Features

✅ **Automatic mermaid diagram rendering** to PNG
✅ **Auto-upload to Google Cloud Storage** (no manual URL replacement!)
✅ **One-command conversion** from markdown to ready-to-paste HTML
✅ **Table conversion** to HTML
✅ **Frontmatter stripping** and WikiLink conversion
✅ **Code block preservation** with optional Color Scripter enhancement

## Quick Start

### 1. Install Dependencies

```bash
cd /Users/julius/Documents/naver_blog
uv sync
```

### 2. Authenticate with Google Cloud

```bash
gcloud auth application-default login
gcloud config set project n8nprojects-444223
```

### 3. Convert Your Markdown

```bash
# With automatic GCS upload (recommended)
uv run python md2naver.py "your-file.md" --gcs

# Without GCS (manual URL replacement needed)
uv run python md2naver.py "your-file.md"
```

### 4. Paste to Naver Blog

1. Open the generated `naver_output_TIMESTAMP/output.html`
2. Copy all content (Cmd+A, Cmd+C)
3. Paste into Naver blog editor
4. Done! Images work immediately with GCS.

## Usage from Obsidian Vault

Use the `/naver` slash command:

```
/naver "1011 산일전기와 전력 시장 공급망 분석.md"
```

Claude will automatically:
- Find the file in your vault
- Convert with GCS upload
- Show you the results
- Tell you where to find output.html

## How It Works

### With `--gcs` Flag

1. **Render** mermaid diagrams to PNG (8 diagrams → 8 PNG files)
2. **Upload** PNGs to Google Cloud Storage automatically
3. **Generate** HTML with real GCS URLs embedded
4. **Output** ready-to-paste HTML file

**Result:** No placeholders, no manual work - just copy and paste!

### Without `--gcs` Flag

1. **Render** mermaid diagrams to PNG
2. **Generate** HTML with `MERMAID_IMAGE_N` placeholders
3. **Manual step:** Use helper script to replace placeholders

## Project Structure

```
naver_blog/
├── md2naver.py              # Main converter
├── gcs_uploader.py          # GCS upload module
├── update_image_urls.py     # Helper for manual URL replacement
├── config.py                # Configuration management
├── pyproject.toml           # Dependencies
├── .env.example             # Configuration template
├── README.md                # This file
├── README_REUSE.md          # Guide for using in other projects
├── GCS_SETUP.md             # Detailed GCS setup instructions
├── QUICKSTART_GCS.md        # Quick GCS guide
└── NAVER_CDN_GUIDE.md       # Alternative: Naver CDN workflow
```

## Configuration

### Current Setup

- **GCS Project:** `n8nprojects-444223`
- **GCS Bucket:** `n8nprojects-naverblog`
- **Image Location:** `naverblog/` subfolder
- **Region:** Seoul (ASIA-NORTHEAST3)

### For Other Projects

See `README_REUSE.md` for complete instructions on using this converter in different projects with different GCS configurations.

## Command-Line Options

```bash
# Basic usage
uv run python md2naver.py INPUT.md

# With GCS upload
uv run python md2naver.py INPUT.md --gcs

# Custom output directory
uv run python md2naver.py INPUT.md -o my_output

# Different GCS project/bucket
uv run python md2naver.py INPUT.md --gcs \
  --gcs-project other-project \
  --gcs-bucket other-bucket
```

## Output Files

Each conversion creates:

```
naver_output_20251012_164509/
├── output.html              # Ready to paste into Naver blog
├── INSTRUCTIONS.md          # Manual steps (if needed)
├── mermaid_code.txt         # Backup of mermaid source
└── images/                  # PNG files (also uploaded to GCS)
    ├── mermaid_1.png
    ├── mermaid_2.png
    └── ...
```

## Supported Markdown Features

| Feature | Status | Notes |
|---------|--------|-------|
| Headers (H1-H6) | ✅ | Fully supported |
| Bold/Italic | ✅ | Fully supported |
| Lists | ✅ | Fully supported |
| Tables | ✅ | Converted to HTML |
| Code blocks | ✅ | Preserved, optional Color Scripter enhancement |
| Blockquotes | ✅ | Fully supported |
| Links | ✅ | Fully supported |
| Images (external) | ✅ | Fully supported |
| **Mermaid diagrams** | ✅ | **Converted to PNG, auto-uploaded to GCS** |
| WikiLinks `[[link]]` | ⚠️ | Converted to plain text |
| YAML frontmatter | ⚠️ | Stripped |

## GCS Image URLs

Images are accessible at:
```
https://storage.googleapis.com/n8nprojects-naverblog/naverblog/mermaid_1.png
https://storage.googleapis.com/n8nprojects-naverblog/naverblog/mermaid_2.png
...
```

- **Public:** Anyone can view (required for Naver blog)
- **Permanent:** URLs never expire
- **Fast:** Google CDN delivery
- **Cost:** Free tier covers typical usage

## Troubleshooting

### "Permission denied" or "401 Unauthorized"

Re-authenticate:
```bash
gcloud auth application-default login
```

### "Module not found: google.cloud"

Install dependencies:
```bash
uv sync
```

### "mmdc not found" (mermaid rendering fails)

Install mermaid-cli:
```bash
npm install -g @mermaid-js/mermaid-cli
```

Or render manually at https://mermaid.live/

### Images don't show in Naver

1. Verify bucket is public (converter does this automatically)
2. Check URL works in browser
3. Ensure you copied the HTML after "Step 7.6: Replacing placeholders with GCS URLs"

## Cost Estimate

**Free tier:**
- 5 GB storage/month (free)
- 1 GB egress (free)

**Your usage (~10 blog posts/month):**
- ~100 KB per image × 8 images × 10 posts = ~8 MB storage
- Minimal egress (visitors viewing images)

**Result:** Well within free tier! (~$0/month)

## Alternative Workflows

### Option 1: GCS Upload (Recommended)
```bash
uv run python md2naver.py file.md --gcs
```
✅ Fully automated
✅ No manual steps
✅ Reliable hosting

### Option 2: Naver CDN Upload
```bash
uv run python md2naver.py file.md
# Then upload images to Naver and use helper script
uv run python update_image_urls.py output_dir/output.html
```
⚠️ Manual URL replacement
⚠️ More steps
✅ Images on Naver's infrastructure

### Option 3: Manual Everything
See `NAVER_CDN_GUIDE.md` for complete manual workflow.

## Examples

### Convert File from Obsidian Vault

```bash
uv run python md2naver.py \
  "../Obsidian Vault/base/글감/1011 산일전기와 전력 시장 공급망 분석.md" \
  --gcs
```

### Batch Convert Multiple Files

```bash
for file in "../Obsidian Vault/base/글감"/*.md; do
  uv run python md2naver.py "$file" --gcs
done
```

### Use in Different Project

```bash
cd /other/project
uv run python /Users/julius/Documents/naver_blog/md2naver.py \
  article.md --gcs \
  --gcs-project other-project-123 \
  --gcs-bucket other-bucket
```

## Resources

- **Mermaid Live Editor:** https://mermaid.live/
- **Color Scripter:** https://colorscripter.com/ (code highlighting for Naver)
- **GCS Console:** https://console.cloud.google.com/storage/browser/n8nprojects-naverblog
- **Naver Blog:** https://blog.naver.com/

## Documentation

- `README_REUSE.md` - Using in other projects
- `GCS_SETUP.md` - Detailed GCS setup
- `QUICKSTART_GCS.md` - Quick GCS guide
- `NAVER_CDN_GUIDE.md` - Manual Naver CDN workflow

## License

Personal tool for converting Obsidian markdown to Naver blog format.

---

**Need help?** Check the documentation files or the generated `INSTRUCTIONS.md` after conversion.
