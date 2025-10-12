# Google Cloud Storage Setup for Naver Blog Converter

## Prerequisites

You have a GCP project: `n8nprojects`

## Step 1: Authenticate with Google Cloud

### Option A: Using gcloud CLI (Recommended - Easiest)

```bash
# Install gcloud CLI if you haven't
# Download from: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth application-default login

# Set your project
gcloud config set project n8nprojects
```

This creates Application Default Credentials that the converter will use automatically.

### Option B: Using Service Account (More Secure for Production)

1. **Create Service Account:**
   - Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=n8nprojects
   - Click "Create Service Account"
   - Name: `naver-blog-uploader`
   - Grant role: `Storage Admin`

2. **Create Key:**
   - Click on the service account
   - Go to "Keys" tab
   - Add Key → Create new key → JSON
   - Save as: `/Users/julius/Documents/naver_blog/gcs-credentials.json`

3. **Set environment variable:**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/Users/julius/Documents/naver_blog/gcs-credentials.json"
   ```

## Step 2: Create GCS Bucket

### Option A: Let the converter create it automatically

The converter will create a bucket named `n8nprojects-naverblog` if it doesn't exist.

### Option B: Create manually

```bash
# Create bucket in Seoul region
gsutil mb -l asia-northeast3 gs://n8nprojects-naverblog

# Make bucket public (for serving images)
gsutil iam ch allUsers:objectViewer gs://n8nprojects-naverblog
```

## Step 3: Configure the Converter

Edit the converter to use your GCS settings:

```python
# In md2naver.py, add:
GCS_PROJECT_ID = "n8nprojects"
GCS_BUCKET_NAME = "n8nprojects-naverblog"
```

## Step 4: Install Dependencies

```bash
cd /Users/julius/Documents/naver_blog
uv sync
```

This installs:
- `google-cloud-storage`
- `google-auth`

## Step 5: Test Upload

```bash
# Test uploading images from a previous conversion
uv run python gcs_uploader.py n8nprojects n8nprojects-naverblog naver_output_20251012_153527/images
```

Expected output:
```
✓ Using existing bucket: n8nprojects-naverblog
Uploading 8 images to GCS...
  ✓ mermaid_1.png → https://storage.googleapis.com/n8nprojects-naverblog/naverblog/mermaid_1.png
  ✓ mermaid_2.png → https://storage.googleapis.com/n8nprojects-naverblog/naverblog/mermaid_2.png
  ...
```

## Step 6: Use with Converter

Once set up, the converter will:
1. Generate mermaid PNG files
2. **Automatically upload to GCS** (in `naverblog/` folder)
3. Generate HTML with **real GCS URLs** (no placeholders!)
4. Ready to paste into Naver blog immediately

## Bucket Structure

```
n8nprojects-naverblog/
└── naverblog/
    ├── mermaid_1.png
    ├── mermaid_2.png
    └── ...
```

All images go in `naverblog/` subfolder for organization.

## URL Format

Images will be accessible at:
```
https://storage.googleapis.com/n8nprojects-naverblog/naverblog/FILENAME.png
```

Example:
```
https://storage.googleapis.com/n8nprojects-naverblog/naverblog/mermaid_1.png
```

## Cost

**Free tier:**
- 5 GB storage per month (free)
- 1 GB egress to China/Australia (free)
- 5 GB egress to other regions per month (free)

**For your use case:**
- ~100 KB per image × 10 images per post × 10 posts = ~10 MB
- Well within free tier!

**Paid (after free tier):**
- Storage: $0.02/GB/month (Seoul region)
- Egress: $0.12/GB (first 10 TB)
- Very cheap for blog images

## Security Notes

**Public Bucket:**
- Images are publicly accessible (required for Naver blog)
- No sensitive data should be uploaded
- Only blog images

**Credentials:**
- Add `gcs-credentials.json` to `.gitignore` (already done)
- Never commit credentials to git

## Troubleshooting

### "Permission denied"
```bash
# Check authentication
gcloud auth application-default print-access-token

# Re-authenticate if needed
gcloud auth application-default login
```

### "Bucket already exists" (owned by another project)
Choose a different bucket name:
```python
GCS_BUCKET_NAME = "julius-naverblog-images"
```

### "Module not found: google.cloud"
```bash
cd /Users/julius/Documents/naver_blog
uv sync
```

### Images not showing in Naver
- Check bucket is public
- Verify URL is accessible in browser
- Ensure URL uses `https://`

## Next Steps

After setup is complete:
1. Run converter with `--gcs` flag
2. Images upload automatically
3. HTML has working URLs immediately
4. Copy-paste to Naver blog - done! ✓

No more manual URL replacement needed!
