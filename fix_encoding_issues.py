#!/usr/bin/env python3
"""
Fix encoding issues in posts by removing problematic Unicode characters
that cause Jekyll/HTML generation to fail
"""

import os
from pathlib import Path
from tqdm import tqdm


def has_problematic_unicode(text):
    """Check for problematic Unicode characters that Jekyll can't handle"""
    problematic_ranges = [
        (0xD800, 0xDFFF),  # Surrogate pairs - MAIN ISSUE
        (0xFDD0, 0xFDEF),  # Noncharacters
        (0xFFFE, 0xFFFF),  # Noncharacters
    ]

    for ch in text:
        code = ord(ch)
        for start, end in problematic_ranges:
            if start <= code <= end:
                return True, ch, code
    return False, None, None


def clean_post_content(content):
    """Clean problematic characters from post content"""
    cleaned = []
    issues_found = []

    for i, ch in enumerate(content):
        code = ord(ch)

        # Check for surrogate pairs (U+D800 to U+DFFF)
        if 0xD800 <= code <= 0xDFFF:
            issues_found.append(f"Surrogate pair U+{code:04X} at position {i}")
            # Skip this character
            continue

        # Check for noncharacters
        if (0xFDD0 <= code <= 0xFDEF) or (0xFFFE <= code <= 0xFFFF):
            issues_found.append(f"Noncharacter U+{code:04X} at position {i}")
            # Skip this character
            continue

        # Keep valid characters
        cleaned.append(ch)

    return ''.join(cleaned), issues_found


def fix_post(post_file):
    """Fix a single post file"""
    try:
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_length = len(content)
        cleaned_content, issues = clean_post_content(content)
        cleaned_length = len(cleaned_content)

        if issues:
            # Write cleaned content
            with open(post_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)

            return {
                'file': post_file.name,
                'status': 'fixed',
                'issues_count': len(issues),
                'chars_removed': original_length - cleaned_length,
                'issues': issues[:3]  # Show first 3 issues
            }
        else:
            return {
                'file': post_file.name,
                'status': 'ok',
                'issues_count': 0,
                'chars_removed': 0,
                'issues': []
            }

    except Exception as e:
        return {
            'file': post_file.name,
            'status': 'error',
            'error': str(e)[:100]
        }


def fix_all_posts():
    """Fix encoding issues in all posts"""
    posts_dir = Path('_posts')
    results = []

    print("Scanning and fixing encoding issues...\n")

    post_files = sorted(posts_dir.glob('*.md'))
    for post_file in tqdm(post_files, desc="Processing", unit="post"):
        result = fix_post(post_file)
        results.append(result)

    return results


if __name__ == '__main__':
    results = fix_all_posts()

    # Summary
    print(f"\n{'='*60}")
    print("ENCODING FIX SUMMARY")
    print(f"{'='*60}\n")

    fixed = [r for r in results if r['status'] == 'fixed']
    ok = [r for r in results if r['status'] == 'ok']
    errors = [r for r in results if r['status'] == 'error']

    total_chars_removed = sum(r.get('chars_removed', 0) for r in fixed)
    total_issues = sum(r.get('issues_count', 0) for r in fixed)

    print(f"✅ Posts fixed: {len(fixed)}")
    print(f"ℹ️  Posts OK: {len(ok)}")
    if errors:
        print(f"❌ Errors: {len(errors)}")
    print(f"\nTotal problematic characters removed: {total_issues}")
    print(f"Total characters deleted: {total_chars_removed}\n")

    # Show fixed posts
    if fixed:
        print(f"{'─'*60}")
        print("Posts with encoding issues fixed:")
        print(f"{'─'*60}\n")
        for r in sorted(fixed, key=lambda x: x['issues_count'], reverse=True)[:10]:
            print(f"📄 {r['file']}")
            print(f"   Issues fixed: {r['issues_count']}")
            if r['issues']:
                for issue in r['issues'][:2]:
                    print(f"   - {issue}")
            print()

        if len(fixed) > 10:
            print(f"... and {len(fixed) - 10} more posts\n")

    # Show errors
    if errors:
        print(f"{'─'*60}")
        print("Errors:")
        print(f"{'─'*60}\n")
        for r in errors:
            print(f"  {r['file']}: {r.get('error', 'Unknown error')}\n")

    print(f"{'='*60}")
    print(f"Total processed: {len(results)}")
    print(f"{'='*60}\n")
