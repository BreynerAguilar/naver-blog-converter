# How to Use Naver Blog CDN for Images

## Problem

The HTML file contains placeholders like `MERMAID_IMAGE_1`, `MERMAID_IMAGE_2`, etc. These are **not actual URLs** - they're just text that you need to replace with real image URLs after uploading to Naver.

## Why This Approach?

Naver Blog has strict restrictions:
- **No local file paths** - `file:///path/to/image.png` won't work
- **No base64 encoding** - Inline images are blocked
- **Must use Naver's CDN** - Images must be uploaded through Naver's interface

## Step-by-Step: Getting Naver CDN URLs

### Method 1: Upload via Post Editor (Recommended)

1. **Open Naver Blog post editor**
   - Go to https://blog.naver.com/
   - Click "글쓰기" (Write)

2. **Upload image**
   - Click the image icon in the toolbar
   - Select "사진 올리기" (Upload photo)
   - Choose `mermaid_1.png` from your `images/` folder
   - Wait for upload to complete

3. **Get CDN URL**
   - After upload, you'll see the image in the editor
   - Right-click on the image
   - Select "이미지 주소 복사" (Copy image address)
   - The URL will look like:
     ```
     https://postfiles.pstatic.net/MjAyNTEwMTJfMjcw/...
     ```
   - **Save this URL** - you'll need it to replace `MERMAID_IMAGE_1`

4. **Repeat for all images**
   - Upload `mermaid_2.png` → get URL → save for `MERMAID_IMAGE_2`
   - Upload `mermaid_3.png` → get URL → save for `MERMAID_IMAGE_3`
   - And so on...

### Method 2: Upload via 사진첩 (Photo Album)

1. **Go to photo album**
   - In your blog management page, click "사진첩" (Photo Album)

2. **Create album**
   - Create a new album (e.g., "Blog Images")

3. **Upload images**
   - Upload all PNG files from `images/` folder

4. **Get URLs**
   - Click on each uploaded image
   - Right-click → "이미지 주소 복사"
   - URLs will look like:
     ```
     https://blogpfthumb-phinf.pstatic.net/...
     ```

## Replacing Placeholders with URLs

### Option A: Use the Helper Script (Easy)

```bash
cd /Users/julius/Documents/naver_blog

# Run the interactive script
uv run python update_image_urls.py naver_output_20251012_153527/output.html
```

The script will:
1. Find all `MERMAID_IMAGE_N` placeholders
2. Prompt you to paste each Naver CDN URL
3. Automatically replace placeholders
4. Create a backup of the original file
5. Save the updated HTML

### Option B: Manual Find & Replace

1. **Open output.html in a text editor**

2. **Find and replace each placeholder:**
   - Find: `MERMAID_IMAGE_1`
   - Replace with: `https://postfiles.pstatic.net/MjAyNTEwMTJfMjcw/...` (your actual URL)

3. **Repeat for all 8 images**

4. **Save the file**

## Example: Complete Workflow

### Starting Point
```html
<p><img alt="Mermaid Diagram 1" src="MERMAID_IMAGE_1"/></p>
<p><img alt="Mermaid Diagram 2" src="MERMAID_IMAGE_2"/></p>
```

### After Uploading to Naver and Getting URLs

| Image File | Placeholder | Naver CDN URL |
|------------|-------------|---------------|
| mermaid_1.png | MERMAID_IMAGE_1 | https://postfiles.pstatic.net/MjAyNTEwMTJfMjcw/MDAxNzI4NzE... |
| mermaid_2.png | MERMAID_IMAGE_2 | https://postfiles.pstatic.net/MjAyNTEwMTJfMTU2/MDAxNzI4NzE... |

### After Replacement
```html
<p><img alt="Mermaid Diagram 1" src="https://postfiles.pstatic.net/MjAyNTEwMTJfMjcw/MDAxNzI4NzE..."/></p>
<p><img alt="Mermaid Diagram 2" src="https://postfiles.pstatic.net/MjAyNTEwMTJfMTU2/MDAxNzI4NzE..."/></p>
```

Now the images will display correctly in Naver blog!

## Understanding Naver CDN URLs

### URL Structure
```
https://postfiles.pstatic.net/[ENCODED_DATE]_[RANDOM]/[HASH]_[FILENAME]?type=w966
```

Example breakdown:
- `postfiles.pstatic.net` - Naver's CDN domain
- `MjAyNTEwMTJfMjcw` - Base64 encoded date/identifier
- `MDAxNzI4NzE...` - Hash/unique identifier
- `?type=w966` - Optional size parameter

### Alternative CDN Domains
You might see:
- `blogpfthumb-phinf.pstatic.net` - Thumbnail CDN
- `blogfiles.pstatic.net` - File CDN
- `postfiles.pstatic.net` - Post image CDN

**All are valid** - Naver uses different CDNs for different purposes.

## Tips

1. **Upload all images first** - Get all URLs before replacing
2. **Save URLs in a text file** - So you don't lose them
3. **Use the helper script** - It's faster and less error-prone
4. **Keep image order** - mermaid_1.png → MERMAID_IMAGE_1, etc.
5. **Test one image first** - Upload one, replace, and verify before doing all

## Troubleshooting

**Q: Image doesn't show after replacement**
- Check URL is complete (no truncation)
- Ensure URL starts with `https://`
- Verify image was actually uploaded to Naver
- Check if URL has special characters that need encoding

**Q: Can I use external image hosting (Imgur, Cloudinary)?**
- Technically yes, but:
  - Naver may block external URLs
  - Images may break if hosting changes
  - Slower loading than Naver CDN
  - **Not recommended**

**Q: Can I automate uploading to Naver?**
- Naver Blog has no public API for image upload
- Manual upload is required
- This is a one-time step per blog post

**Q: Do URLs expire?**
- No, Naver CDN URLs are permanent
- They remain valid as long as your blog exists
- Safe to use in published posts

## Complete Example

For your test file with 8 mermaid diagrams:

1. Upload 8 PNG files to Naver blog editor
2. Get 8 CDN URLs
3. Run helper script:
   ```bash
   uv run python update_image_urls.py naver_output_20251012_153527/output.html
   ```
4. Paste each URL when prompted
5. Script creates `output.html.backup` and updates `output.html`
6. Open updated `output.html` and copy all content
7. Use DevTools (F12) to paste into Naver blog
8. Preview and publish

Done! All images will now display correctly in your blog post.
