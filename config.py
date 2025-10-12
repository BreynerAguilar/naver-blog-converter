"""
Configuration for Naver Blog Converter

This file contains default settings that can be overridden via:
1. Environment variables
2. Command-line arguments
3. .env file

For different projects, create a .env file with your settings.
"""

import os
from pathlib import Path

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    pass  # dotenv not required

# Google Cloud Storage Configuration
# These must be set via environment variables or .env file
GCS_PROJECT_ID = os.getenv('GCS_PROJECT_ID')  # Required: Your GCP project ID
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')  # Required: Your GCS bucket name
GCS_LOCATION = os.getenv('GCS_LOCATION', 'ASIA-NORTHEAST3')  # Default: Seoul (change if needed)
GCS_SUBFOLDER = os.getenv('GCS_SUBFOLDER', 'blog-images')  # Default subfolder in bucket
GCS_CREDENTIALS_PATH = os.getenv('GCS_CREDENTIALS_PATH', None)

# Converter Settings
DEFAULT_OUTPUT_DIR = None  # None = auto-generate timestamp
MERMAID_SCALE = 2  # 2x resolution for better quality
MERMAID_BACKGROUND = 'transparent'

# Image Settings
IMAGE_FORMAT = 'png'
IMAGE_QUALITY = 95  # For JPEG if ever needed

# Markdown Extensions
MARKDOWN_EXTENSIONS = [
    'tables',
    'fenced_code',
    'nl2br',
    'sane_lists'
]

def get_gcs_config():
    """Get GCS configuration as a dict."""
    return {
        'project_id': GCS_PROJECT_ID,
        'bucket_name': GCS_BUCKET_NAME,
        'location': GCS_LOCATION,
        'subfolder': GCS_SUBFOLDER,
        'credentials_path': GCS_CREDENTIALS_PATH
    }

def display_config():
    """Display current configuration."""
    print("Current Configuration:")
    print(f"  GCS Project: {GCS_PROJECT_ID}")
    print(f"  GCS Bucket: {GCS_BUCKET_NAME}")
    print(f"  GCS Location: {GCS_LOCATION}")
    print(f"  GCS Subfolder: {GCS_SUBFOLDER}")
    if GCS_CREDENTIALS_PATH:
        print(f"  Credentials: {GCS_CREDENTIALS_PATH}")
    else:
        print(f"  Credentials: Using Application Default Credentials")
