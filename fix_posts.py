#!/usr/bin/env python3
"""
Fix problematic posts by removing control characters and cleaning YAML
"""

import os
import re
import yaml
from pathlib import Path
from tqdm import tqdm


def clean_text(text):
    """Remove control characters from text, keeping only printable chars and common whitespace"""
    cleaned = ''.join(
        ch for ch in text
        if ord(ch) >= 32 or ch in '\n\t\r'
    )
    # Remove null bytes and other special control chars
    cleaned = cleaned.replace('\x00', '')
    return cleaned


def clean_filename(filename):
    """Clean filename of problematic characters"""
    # Remove control characters
    clean = ''.join(ch for ch in filename if ord(ch) >= 32)
    # Remove consecutive dashes
    clean = re.sub(r'-{2,}', '-', clean)
    # Remove leading/trailing dashes and spaces
    clean = clean.strip('- ')
    return clean


def fix_post(post_file):
    """Fix a single post file"""
    try:
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes = []

        # Step 1: Clean content
        cleaned_content = clean_text(content)
        if cleaned_content != content:
            changes.append('removed_control_chars')
            content = cleaned_content

        # Step 2: Parse and fix YAML front matter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                front_matter_str = parts[1].strip()
                body = parts[2]

                try:
                    # Parse YAML
                    data = yaml.safe_load(front_matter_str)

                    # Clean title and other string fields
                    if isinstance(data, dict):
                        for key in ['title', 'description', 'subtitle']:
                            if key in data and isinstance(data[key], str):
                                cleaned = clean_text(data[key])
                                if data[key] != cleaned:
                                    data[key] = cleaned
                                    changes.append(f'cleaned_{key}')

                    # Regenerate clean YAML
                    new_front_matter = yaml.dump(
                        data,
                        allow_unicode=True,
                        default_flow_style=False,
                        sort_keys=False
                    )
                    content = f"---\n{new_front_matter}---\n{body}"
                    changes.append('regenerated_yaml')
                except yaml.YAMLError as e:
                    # If YAML parsing fails, just clean the text
                    changes.append(f'yaml_parse_error_cleaned')

        # Step 3: Fix filename if needed
        old_name = post_file.name
        new_name = clean_filename(old_name)

        # Write fixed content
        with open(post_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # Rename file if needed
        if old_name != new_name:
            new_path = post_file.parent / new_name
            if new_path.exists() and new_path != post_file:
                # Handle potential collision
                new_name = new_name.replace('.md', f'_renamed.md')
                new_path = post_file.parent / new_name
            post_file.rename(new_path)
            changes.append(f'renamed_file')
            return {
                'old_name': old_name,
                'new_name': new_name,
                'changes': changes,
                'status': 'fixed_and_renamed'
            }
        elif changes:
            return {
                'old_name': old_name,
                'new_name': old_name,
                'changes': changes,
                'status': 'fixed'
            }
        else:
            return {
                'old_name': old_name,
                'new_name': old_name,
                'changes': [],
                'status': 'no_changes'
            }

    except Exception as e:
        return {
            'old_name': post_file.name,
            'new_name': post_file.name,
            'changes': [],
            'status': f'error: {str(e)[:50]}'
        }


def fix_all_posts():
    """Fix all problematic posts"""
    posts_dir = Path('_posts')
    results = []

    print("Fixing posts...\n")

    post_files = sorted(posts_dir.glob('*.md'))
    for post_file in tqdm(post_files, desc="Processing", unit="post"):
        result = fix_post(post_file)
        results.append(result)

    return results


if __name__ == '__main__':
    results = fix_all_posts()

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}\n")

    fixed = [r for r in results if r['status'] == 'fixed']
    renamed = [r for r in results if r['status'] == 'fixed_and_renamed']
    no_changes = [r for r in results if r['status'] == 'no_changes']
    errors = [r for r in results if r['status'].startswith('error')]

    print(f"✅ Fixed (content only): {len(fixed)}")
    print(f"✅ Fixed and renamed: {len(renamed)}")
    print(f"ℹ️  No changes needed: {len(no_changes)}")
    if errors:
        print(f"❌ Errors: {len(errors)}")

    # Show renamed files
    if renamed:
        print(f"\n{'─'*60}")
        print("Files renamed:")
        print(f"{'─'*60}\n")
        for r in renamed:
            print(f"  {r['old_name']}")
            print(f"  → {r['new_name']}\n")

    # Show errors
    if errors:
        print(f"\n{'─'*60}")
        print("Errors:")
        print(f"{'─'*60}\n")
        for r in errors:
            print(f"  {r['old_name']}: {r['status']}\n")

    print(f"{'='*60}")
    print(f"Total processed: {len(results)}")
    print(f"{'='*60}\n")
