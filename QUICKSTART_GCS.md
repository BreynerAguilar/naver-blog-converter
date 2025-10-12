# Quick Start: Using Google Cloud Storage

## What's New

The converter now supports **automatic image upload to Google Cloud Storage**!

Instead of manually replacing `MERMAID_IMAGE_N` placeholders, images are automatically:
1. Uploaded to your GCS bucket (`n8nprojects-naverblog`)
2. Stored in `naverblog/` folder
3. Embedded in HTML with real URLs
4. Ready to copy-paste into Naver blog immediately!

## Setup (One-Time)

### Step 1: Authenticate with Google Cloud

```bash
# Install gcloud CLI (if not already installed)
# https://cloud.google.com/sdk/docs/install

# Login and set project
gcloud auth application-default login
gcloud config set project n8nprojects
```

This creates credentials that the converter will use automatically.

### Step 2: Done!

That's it! The converter will:
- Auto-create bucket `n8nprojects-naverblog` if it doesn't exist
- Make it public for serving images
- Upload to `naverblog/` subfolder

## Usage

### With GCS (Recommended)

```bash
cd /Users/julius/Documents/naver_blog

# Convert with automatic GCS upload
uv run python md2naver.py "../Obsidian Vault/base/글감/YOUR_FILE.md" --gcs
```

### Without GCS (Old Way)

```bash
# Generate images only (manual URL replacement needed)
uv run python md2naver.py "YOUR_FILE.md"
```

## What Happens

**With `--gcs` flag:**

```
Converting: YOUR_FILE.md
...
Step 7: Rendering 8 mermaid diagrams...
  ✓ Rendered mermaid diagram 1
  ...
  ✓ Rendered mermaid diagram 8

Step 7.5: Uploading images to Google Cloud Storage...
✓ Using existing bucket: n8nprojects-naverblog
Uploading 8 images to GCS...
  ✓ mermaid_1.png → https://storage.googleapis.com/n8nprojects-naverblog/naverblog/mermaid_1.png
  ...
  ✓ Uploaded 8 images to GCS

Step 7.6: Regenerating HTML with GCS URLs...
  ✓ HTML regenerated with GCS URLs

Conversion Complete!
```

**Result:** HTML file contains real GCS URLs - no placeholder replacement needed!

## Final Step: Paste to Naver

1. **Open** `output.html`
2. **Copy** all content (Cmd+A, Cmd+C)
3. **Paste** into Naver blog editor (use DevTools F12 method if needed)
4. **Done!** Images show immediately

## Example: Full Workflow

```bash
# Navigate to project
cd /Users/julius/Documents/naver_blog

# Convert with GCS upload
uv run python md2naver.py \
  "../Obsidian Vault/base/글감/1011 산일전기와 전력 시장 공급망 분석.md" \
  --gcs

# Output directory created: naver_output_20251012_160000/
# - output.html (with real GCS URLs ✓)
# - images/ (also backed up locally)
# - INSTRUCTIONS.md

# Open output.html, copy content, paste to Naver blog
# Images work immediately!
```

## Using from Obsidian (Slash Command)

Update your `/naver` command to use GCS:

```bash
cd /Users/julius/Documents/naver_blog && \
uv run python md2naver.py "<full-path-to-file>" --gcs
```

Now when you type `/naver "filename.md"` it automatically uploads to GCS!

## Checking Your Images

View uploaded images at:
```
https://console.cloud.google.com/storage/browser/n8nprojects-naverblog/naverblog
```

Or access directly:
```
https://storage.googleapis.com/n8nprojects-naverblog/naverblog/mermaid_1.png
```

## Cost

**Free tier covers typical usage:**
- 5GB storage/month (free)
- 1GB egress (free)

Your blog images (~1MB per post) are well within limits.

## Troubleshooting

### "Permission denied" or "401 Unauthorized"

Re-authenticate:
```bash
gcloud auth application-default login
```

### "Bucket already exists" (different project)

Use a custom bucket name:
```bash
uv run python md2naver.py "file.md" --gcs \
  --gcs-bucket "julius-blog-images"
```

### "Module not found: google.cloud"

Install dependencies:
```bash
cd /Users/julius/Documents/naver_blog
uv sync
```

### Images don't show in Naver

1. Check bucket is public (converter does this automatically)
2. Verify URL works in browser
3. Ensure you copied the updated HTML (after Step 7.6)

## Benefits vs Manual Upload

| Method | Steps | Time | Errors |
|--------|-------|------|--------|
| **Manual** | Convert → Upload 8 images → Copy 8 URLs → Replace 8 placeholders → Paste | ~10 min | Easy to miss/mistype URLs |
| **GCS** | Convert with `--gcs` → Paste | ~1 min | Zero (automated) |

## Next Steps

1. Test with a sample file
2. Verify images show in Naver blog
3. Update your `/naver` slash command to use `--gcs`
4. Enjoy one-step conversion!

---

**Ready to try? Run:**

```bash
cd /Users/julius/Documents/naver_blog
uv run python md2naver.py \
  "../Obsidian Vault/base/글감/1011 산일전기와 전력 시장 공급망 분석.md" \
  --gcs
```

Then open `output.html` and paste into Naver blog!
