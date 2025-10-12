#!/usr/bin/env python3
"""
Google Cloud Storage uploader for blog images.

Uploads mermaid diagram PNGs to GCS and returns public URLs.
"""

import os
from pathlib import Path
from typing import List, Dict

try:
    from google.cloud import storage
    from google.oauth2 import service_account
    import google.auth
except ImportError:
    print("ERROR: Google Cloud Storage library not installed.")
    print("Run: uv sync")
    exit(1)


class GCSUploader:
    """Upload images to Google Cloud Storage."""

    def __init__(self, project_id: str, bucket_name: str, credentials_path: str = None):
        """
        Initialize GCS uploader.

        Args:
            project_id: GCP project ID (e.g., 'my-project-123')
            bucket_name: GCS bucket name for blog images
            credentials_path: Path to service account JSON (optional, uses default auth if not provided)
        """
        self.project_id = project_id
        self.bucket_name = bucket_name

        # Initialize client
        if credentials_path and Path(credentials_path).exists():
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            self.client = storage.Client(credentials=credentials, project=project_id)
        else:
            # Use Application Default Credentials (gcloud auth)
            self.client = storage.Client(project=project_id)

        self.bucket = None

    def ensure_bucket_exists(self, location: str = "ASIA-NORTHEAST3") -> bool:
        """
        Ensure bucket exists, create if it doesn't.

        Args:
            location: GCS location (default: ASIA-NORTHEAST3 = Seoul)

        Returns:
            True if bucket exists or was created successfully
        """
        try:
            self.bucket = self.client.get_bucket(self.bucket_name)
            print(f"✓ Using existing bucket: {self.bucket_name}")
            return True
        except Exception:
            # Bucket doesn't exist, try to create
            try:
                self.bucket = self.client.create_bucket(
                    self.bucket_name,
                    location=location
                )
                print(f"✓ Created new bucket: {self.bucket_name}")

                # Make bucket public for image serving
                self.bucket.make_public(recursive=True)
                print(f"✓ Made bucket public")
                return True
            except Exception as e:
                print(f"✗ Failed to create bucket: {e}")
                return False

    def upload_image(self, local_path: Path, blob_name: str = None) -> str:
        """
        Upload a single image to GCS.

        Args:
            local_path: Local file path
            blob_name: Name in GCS (defaults to filename)

        Returns:
            Public URL of uploaded image
        """
        if not self.bucket:
            raise RuntimeError("Bucket not initialized. Call ensure_bucket_exists() first.")

        if not blob_name:
            blob_name = local_path.name

        # Create blob
        blob = self.bucket.blob(blob_name)

        # Upload file
        blob.upload_from_filename(str(local_path), content_type='image/png')

        # Make blob public
        blob.make_public()

        # Return public URL
        return blob.public_url

    def upload_images_from_dir(self, images_dir: Path, prefix: str = "") -> Dict[str, str]:
        """
        Upload all PNG images from a directory.

        Args:
            images_dir: Directory containing images
            prefix: Optional prefix for blob names (e.g., "blog-images/" or "" for root)

        Returns:
            Dict mapping local filename to public URL
        """
        if not images_dir.exists():
            raise FileNotFoundError(f"Images directory not found: {images_dir}")

        image_files = sorted(images_dir.glob("*.png"))

        if not image_files:
            print(f"No PNG files found in {images_dir}")
            return {}

        print(f"\nUploading {len(image_files)} images to GCS...")

        url_map = {}
        for image_file in image_files:
            blob_name = f"{prefix}{image_file.name}" if prefix else image_file.name
            try:
                url = self.upload_image(image_file, blob_name)
                url_map[image_file.name] = url
                print(f"  ✓ {image_file.name} → {url}")
            except Exception as e:
                print(f"  ✗ Failed to upload {image_file.name}: {e}")

        return url_map


def test_upload():
    """Test GCS upload with sample configuration."""
    import sys

    if len(sys.argv) < 4:
        print("Usage: python gcs_uploader.py <project_id> <bucket_name> <images_dir>")
        print("\nExample:")
        print("  python gcs_uploader.py my-gcp-project my-bucket-name naver_output_20251012_153527/images")
        sys.exit(1)

    project_id = sys.argv[1]
    bucket_name = sys.argv[2]
    images_dir = Path(sys.argv[3])

    uploader = GCSUploader(project_id, bucket_name)

    if not uploader.ensure_bucket_exists():
        print("Failed to initialize bucket")
        sys.exit(1)

    url_map = uploader.upload_images_from_dir(images_dir)

    print(f"\n{'='*60}")
    print("Upload Complete!")
    print(f"{'='*60}")
    print(f"Uploaded {len(url_map)} images")
    print("\nURLs:")
    for filename, url in url_map.items():
        print(f"  {filename}: {url}")


if __name__ == '__main__':
    test_upload()
