# Reusing Naver Blog Converter in Other Projects

This converter can be used in any project. Here's how to set it up.

## Quick Setup for New Project

### 1. Copy the Converter

```bash
# Copy the entire naver_blog directory to your project
cp -r /Users/julius/Documents/naver_blog /path/to/your/project/
```

### 2. Install Dependencies

```bash
cd /path/to/your/project/naver_blog
uv sync
```

### 3. Configure for Your Project

Create a `.env` file:

```bash
cp .env.example .env
nano .env
```

Edit the values:

```env
# Your GCS project
GCS_PROJECT_ID=your-project-id

# Your bucket name (will be created if doesn't exist)
GCS_BUCKET_NAME=your-bucket-name

# Region (default: Seoul)
GCS_LOCATION=ASIA-NORTHEAST3

# Subfolder for images
GCS_SUBFOLDER=blog-images
```

### 4. Authenticate

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### 5. Use It

```bash
uv run python md2naver.py your-file.md --gcs
```

## Using with Different GCS Projects

### Option A: Environment Variables

```bash
export GCS_PROJECT_ID="other-project-123"
export GCS_BUCKET_NAME="other-bucket"
uv run python md2naver.py file.md --gcs
```

### Option B: Command-Line Args

```bash
uv run python md2naver.py file.md --gcs \
  --gcs-project other-project-123 \
  --gcs-bucket other-bucket
```

### Option C: Multiple .env Files

Create project-specific configs:

```bash
# Create configs
cat > .env.project1 <<EOF
GCS_PROJECT_ID=project1-id
GCS_BUCKET_NAME=project1-bucket
EOF

cat > .env.project2 <<EOF
GCS_PROJECT_ID=project2-id
GCS_BUCKET_NAME=project2-bucket
EOF

# Use specific config
cp .env.project1 .env
uv run python md2naver.py file.md --gcs
```

## Integration Examples

### In a Python Script

```python
from md2naver import NaverBlogConverter

# Custom configuration
converter = NaverBlogConverter(
    "article.md",
    use_gcs=True,
    gcs_project="my-project",
    gcs_bucket="my-bucket"
)
converter.convert()
```

### In a Makefile

```makefile
# Makefile
.PHONY: blog

blog:
	cd naver_blog && \
	uv run python md2naver.py ../articles/latest.md --gcs
```

### In a CI/CD Pipeline

```yaml
# .github/workflows/publish-blog.yml
name: Publish to Blog

on:
  push:
    paths:
      - 'articles/*.md'

jobs:
  convert:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install uv
        run: pip install uv

      - name: Authenticate GCS
        env:
          GCP_SA_KEY: ${{ secrets.GCP_SA_KEY }}
        run: |
          echo "$GCP_SA_KEY" > key.json
          gcloud auth activate-service-account --key-file=key.json

      - name: Convert and Upload
        run: |
          cd naver_blog
          uv sync
          uv run python md2naver.py ../articles/latest.md --gcs
```

### As a Node.js Package Script

```json
{
  "scripts": {
    "blog": "cd naver_blog && uv run python md2naver.py ../content/post.md --gcs"
  }
}
```

## Project-Specific Slash Commands

If using Claude Code in different projects, create project-specific commands:

### Project 1: Tech Blog

`.claude/commands/tech-blog.md`:
```markdown
---
description: Convert to tech blog format
---

cd /path/to/project1/naver_blog && \
uv run python md2naver.py "<file>" --gcs \
  --gcs-project tech-blog-project \
  --gcs-bucket tech-blog-images
```

### Project 2: Company Blog

`.claude/commands/company-blog.md`:
```markdown
---
description: Convert to company blog format
---

cd /path/to/project2/naver_blog && \
uv run python md2naver.py "<file>" --gcs \
  --gcs-project company-site-123 \
  --gcs-bucket company-blog-assets
```

## Sharing Across Team

### Option 1: Git Submodule

```bash
# In main project
git submodule add https://github.com/you/naver-blog-converter tools/naver_blog

# Team members
git submodule update --init --recursive
```

### Option 2: Package It

Create `pyproject.toml`:

```toml
[project]
name = "naver-blog-converter"
version = "1.0.0"

[project.scripts]
naver-blog = "md2naver:main"
```

Install as package:

```bash
pip install -e /path/to/naver_blog
naver-blog article.md --gcs
```

### Option 3: Docker Container

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv sync

ENTRYPOINT ["uv", "run", "python", "md2naver.py"]
```

Use it:

```bash
docker build -t naver-blog-converter .
docker run -v $(pwd):/work naver-blog-converter /work/article.md --gcs
```

## Configuration Best Practices

### 1. Never Commit Credentials

Add to `.gitignore`:

```
.env
gcs-credentials.json
*-credentials.json
```

### 2. Document Project-Specific Settings

Create `BLOG_SETUP.md` in each project:

```markdown
# Blog Setup for This Project

GCS Project: `project-name-123`
GCS Bucket: `project-blog-images`
Region: Seoul (ASIA-NORTHEAST3)

Setup:
1. `gcloud auth application-default login`
2. `cd naver_blog && uv sync`
3. `uv run python md2naver.py ../content/article.md --gcs`
```

### 3. Use Consistent Naming

```
project-name-blog          # Bucket name
project-name-blog/assets   # Subfolder
```

## Multi-Environment Support

```python
# config_prod.py
GCS_PROJECT_ID = "company-prod-123"
GCS_BUCKET_NAME = "blog-prod"

# config_dev.py
GCS_PROJECT_ID = "company-dev-456"
GCS_BUCKET_NAME = "blog-dev"

# Use environment variable to switch
# export BLOG_ENV=prod
import os
if os.getenv('BLOG_ENV') == 'prod':
    from config_prod import *
else:
    from config_dev import *
```

## Cost Management

### Per Project

Each project can have its own:
- GCS bucket (for cost tracking)
- Storage location (optimize for your region)
- Lifecycle policies (auto-delete old images)

### Example Lifecycle Policy

```bash
# Delete images older than 90 days
gsutil lifecycle set lifecycle.json gs://your-bucket

# lifecycle.json
{
  "rule": [{
    "action": {"type": "Delete"},
    "condition": {"age": 90}
  }]
}
```

## Summary

The converter is fully portable. To use in a new project:

1. **Copy** the `naver_blog/` directory
2. **Configure** GCS settings (`.env` or args)
3. **Authenticate** with gcloud
4. **Run** with `--gcs` flag

That's it! Each project can have its own GCS bucket, settings, and workflow.
