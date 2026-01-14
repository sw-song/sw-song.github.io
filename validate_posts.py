#!/usr/bin/env python3
"""
Validate all posts to ensure they have valid YAML and no control characters
"""

import yaml
from pathlib import Path
from tqdm import tqdm


def has_control_characters(text):
    """Check if text contains control characters"""
    return any(ord(ch) < 32 and ch not in '\n\t\r' for ch in text)


def validate_post(post_file):
    """Validate a single post"""
    errors = []

    try:
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check YAML front matter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                try:
                    yaml.safe_load(parts[1])
                except yaml.YAMLError as e:
                    errors.append(f"YAML error: {str(e)[:50]}")
            else:
                errors.append("Malformed YAML front matter")

        # Check filename for control characters
        if has_control_characters(post_file.name):
            errors.append("Filename contains control characters")

        # Check content for control characters
        if has_control_characters(content):
            errors.append("Content contains control characters")

    except Exception as e:
        errors.append(f"Read error: {str(e)[:50]}")

    return errors


def validate_all_posts():
    """Validate all posts"""
    posts_dir = Path('_posts')
    results = {
        'valid': [],
        'invalid': [],
        'total': 0
    }

    print("Validating posts...\n")

    post_files = sorted(posts_dir.glob('*.md'))
    for post_file in tqdm(post_files, desc="Validating", unit="post"):
        results['total'] += 1
        errors = validate_post(post_file)
        if errors:
            results['invalid'].append({
                'file': post_file.name,
                'errors': errors
            })
        else:
            results['valid'].append(post_file.name)

    return results


if __name__ == '__main__':
    results = validate_all_posts()

    print(f"\n{'='*60}")
    print("VALIDATION RESULTS")
    print(f"{'='*60}\n")

    print(f"✅ Valid posts: {len(results['valid'])}")
    print(f"❌ Invalid posts: {len(results['invalid'])}")
    print(f"📊 Total: {results['total']}\n")

    if results['invalid']:
        print(f"{'─'*60}")
        print("Problematic posts:")
        print(f"{'─'*60}\n")
        for issue in results['invalid']:
            print(f"📄 {issue['file']}")
            for error in issue['errors']:
                print(f"   ⚠️  {error}")
            print()
    else:
        print("🎉 All posts are valid!")

    print(f"{'='*60}\n")

    # Exit with appropriate code
    exit(0 if len(results['invalid']) == 0 else 1)
