#!/usr/bin/env python3
"""
Compress all images in assets/images/posts to WebP format for repository optimization.
Reduces file sizes by 25-35% while maintaining visual quality.
"""

import os
import re
from pathlib import Path
from PIL import Image
from tqdm import tqdm

# Configuration
IMAGES_DIR = Path('assets/images/posts')
QUALITY = 85  # WebP quality (0-100, higher = better quality, larger file)
WEBP_METHOD = 6  # 0-6, higher = slower but smaller output
SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}


def compress_image_to_webp(image_path):
    """Compress a single image to WebP format"""
    try:
        # Open image
        img = Image.open(image_path)

        # Convert RGBA to RGB if needed for better compression
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            # Paste image with alpha channel
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')

        # Create WebP path
        webp_path = image_path.with_suffix('.webp')

        # Save as WebP
        img.save(
            webp_path,
            'WEBP',
            quality=QUALITY,
            method=WEBP_METHOD
        )

        # Get sizes
        original_size = image_path.stat().st_size
        webp_size = webp_path.stat().st_size
        compression_ratio = (1 - webp_size / original_size) * 100

        return {
            'status': 'success',
            'original_size': original_size,
            'webp_size': webp_size,
            'saved': original_size - webp_size,
            'compression_ratio': compression_ratio
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


def compress_all_images():
    """Compress all images in the posts directory to WebP"""
    if not IMAGES_DIR.exists():
        print(f"Error: {IMAGES_DIR} does not exist")
        return None

    # Find all image files
    image_files = []
    for ext in SUPPORTED_FORMATS:
        image_files.extend(IMAGES_DIR.glob(f'*{ext}'))
        image_files.extend(IMAGES_DIR.glob(f'*{ext.upper()}'))

    image_files = sorted(set(image_files))  # Remove duplicates and sort

    if not image_files:
        print(f"No images found in {IMAGES_DIR}")
        return {'total': 0, 'results': []}

    print(f"\nCompressing {len(image_files)} images to WebP format...\n")

    results = []
    total_original_size = 0
    total_webp_size = 0

    for image_path in tqdm(image_files, desc="Compressing", unit="image"):
        total_original_size += image_path.stat().st_size
        result = compress_image_to_webp(image_path)
        result['filename'] = image_path.name
        results.append(result)

        if result['status'] == 'success':
            total_webp_size += result['webp_size']

    return {
        'total': len(image_files),
        'successful': len([r for r in results if r['status'] == 'success']),
        'failed': len([r for r in results if r['status'] == 'error']),
        'total_original_size': total_original_size,
        'total_webp_size': total_webp_size,
        'total_saved': total_original_size - total_webp_size,
        'overall_compression_ratio': (1 - total_webp_size / total_original_size) * 100 if total_original_size > 0 else 0,
        'results': results
    }


def format_size(bytes_size):
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"


def print_summary(stats):
    """Print compression summary"""
    print(f"\n{'='*70}")
    print("WEBP COMPRESSION SUMMARY")
    print(f"{'='*70}\n")

    print(f"✅ Successfully compressed: {stats['successful']} images")
    if stats['failed'] > 0:
        print(f"❌ Failed: {stats['failed']} images")
    print(f"\n📊 Size Reduction:")
    print(f"  Original size:      {format_size(stats['total_original_size'])}")
    print(f"  Compressed size:    {format_size(stats['total_webp_size'])}")
    print(f"  Total saved:        {format_size(stats['total_saved'])}")
    print(f"  Compression ratio:  {stats['overall_compression_ratio']:.1f}%\n")

    # Show top 10 largest images
    successful_results = [r for r in stats['results'] if r['status'] == 'success']
    if successful_results:
        print(f"{'─'*70}")
        print("Top 10 largest files (after compression):")
        print(f"{'─'*70}\n")

        sorted_results = sorted(successful_results, key=lambda x: x['webp_size'], reverse=True)
        for i, result in enumerate(sorted_results[:10], 1):
            saved_pct = result['compression_ratio']
            print(f"{i:2}. {result['filename']}")
            print(f"    {format_size(result['original_size'])} → {format_size(result['webp_size'])} "
                  f"(saved {saved_pct:.1f}%)\n")

    # Show errors if any
    error_results = [r for r in stats['results'] if r['status'] == 'error']
    if error_results:
        print(f"{'─'*70}")
        print("Compression errors:")
        print(f"{'─'*70}\n")
        for result in error_results[:5]:
            print(f"  {result['filename']}: {result['error']}\n")

    print(f"{'='*70}\n")


def update_post_image_references():
    """Update all post files to reference .webp images instead of original formats"""
    posts_dir = Path('_posts')

    if not posts_dir.exists():
        print("Warning: _posts directory not found, skipping post updates")
        return {'total': 0, 'updated': 0}

    post_files = sorted(posts_dir.glob('*.md'))
    if not post_files:
        return {'total': 0, 'updated': 0}

    print(f"\nUpdating image references in {len(post_files)} posts...\n")

    updated_posts = 0
    total_replacements = 0

    for post_file in tqdm(post_files, desc="Updating posts", unit="post"):
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Replace image extensions in references
            # Match patterns like: (/assets/images/posts/image.png) or (/assets/images/posts/image.jpg)
            patterns = [
                (r'(!\[.*?\]\(/assets/images/posts/[^)]+)\.png\)', r'\1.webp)'),
                (r'(!\[.*?\]\(/assets/images/posts/[^)]+)\.jpg\)', r'\1.webp)'),
                (r'(!\[.*?\]\(/assets/images/posts/[^)]+)\.jpeg\)', r'\1.webp)'),
                (r'(!\[.*?\]\(/assets/images/posts/[^)]+)\.gif\)', r'\1.webp)'),
                (r'(!\[.*?\]\(/assets/images/posts/[^)]+)\.bmp\)', r'\1.webp)'),
                # Also handle markdown image format without parentheses
                (r'(/assets/images/posts/[^)\s]+)\.png\b', r'\1.webp'),
                (r'(/assets/images/posts/[^)\s]+)\.jpg\b', r'\1.webp'),
                (r'(/assets/images/posts/[^)\s]+)\.jpeg\b', r'\1.webp'),
                (r'(/assets/images/posts/[^)\s]+)\.gif\b', r'\1.webp'),
                (r'(/assets/images/posts/[^)\s]+)\.bmp\b', r'\1.webp'),
            ]

            replacements = 0
            for pattern, replacement in patterns:
                new_content, count = re.subn(pattern, replacement, content)
                if count > 0:
                    content = new_content
                    replacements += count

            # Write back if changed
            if content != original_content:
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_posts += 1
                total_replacements += replacements

        except Exception as e:
            print(f"Error updating {post_file.name}: {e}")

    return {
        'total': len(post_files),
        'updated': updated_posts,
        'replacements': total_replacements
    }


def delete_original_images():
    """Delete original image files after successful compression"""
    if not IMAGES_DIR.exists():
        return {'deleted': 0}

    # Find all non-webp image files
    image_files = []
    for ext in SUPPORTED_FORMATS:
        image_files.extend(IMAGES_DIR.glob(f'*{ext}'))
        image_files.extend(IMAGES_DIR.glob(f'*{ext.upper()}'))

    image_files = sorted(set(image_files))

    if not image_files:
        return {'deleted': 0}

    print(f"\nDeleting {len(image_files)} original image files...\n")

    deleted = 0
    for image_file in tqdm(image_files, desc="Deleting", unit="file"):
        try:
            image_file.unlink()
            deleted += 1
        except Exception as e:
            print(f"Error deleting {image_file.name}: {e}")

    return {'deleted': deleted}


if __name__ == '__main__':
    # Step 1: Compress images
    print("\n" + "="*70)
    print("STEP 1: COMPRESSING IMAGES TO WEBP FORMAT")
    print("="*70)
    stats = compress_all_images()

    if stats and stats['total'] > 0:
        print_summary(stats)

        # Step 2: Update post references
        print("\n" + "="*70)
        print("STEP 2: UPDATING IMAGE REFERENCES IN POSTS")
        print("="*70)
        post_update_stats = update_post_image_references()
        print(f"\n✅ Updated {post_update_stats['updated']} posts")
        print(f"✅ Updated {post_update_stats['replacements']} image references\n")

        # Step 3: Delete original images
        print("="*70)
        print("STEP 3: DELETING ORIGINAL IMAGE FILES")
        print("="*70)
        delete_stats = delete_original_images()
        print(f"\n✅ Deleted {delete_stats['deleted']} original image files\n")

        # Final summary
        print("="*70)
        print("COMPRESSION COMPLETE")
        print("="*70)
        print(f"\n✅ All {stats['successful']} images compressed to WebP")
        print(f"✅ Repository size reduced by {format_size(stats['total_saved'])}")
        print(f"✅ All image references updated in posts")
        print(f"✅ Original image files deleted\n")
        print("Next steps:")
        print("  1. Run: python validate_posts.py")
        print("  2. Review changes: git status")
        print("  3. Commit: git add -A && git commit -m 'Compress images to WebP format'")
        print("  4. Push: git push origin main\n")
    else:
        print("No images found to compress")
