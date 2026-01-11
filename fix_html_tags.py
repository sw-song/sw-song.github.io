#!/usr/bin/env python3
"""
Fix HTML tag issues in posts by properly escaping angle brackets
that contain non-ASCII characters or invalid tag names
"""

import re
from pathlib import Path
from tqdm import tqdm


def escape_invalid_tags(content):
    """
    Find and escape angle brackets that don't contain valid HTML tag names
    Valid HTML tags only contain ASCII letters, numbers, and hyphens
    """
    issues_found = []

    # Pattern to find potential tags: <...>
    # But we need to be careful not to break real HTML tags
    pattern = r'<([^>]+)>'

    def replace_tag(match):
        tag_content = match.group(1)

        # Check if this looks like a real HTML tag (only ASCII alphanumeric and hyphens)
        # Real tags: <div>, <h1>, <span>, <br />, etc.
        # Invalid: <태그>, <div class="한글">, etc.

        # If tag content has non-ASCII, or contains spaces with non-ASCII, it's likely not a real tag
        # Also check if first character after < is a letter (for real tags)
        if not re.match(r'^/?[a-zA-Z0-9]', tag_content):
            # Not a valid tag start (should start with letter or /)
            issues_found.append(f"Invalid tag: <{tag_content}>")
            return f"&lt;{tag_content}&gt;"

        # If it has Korean characters or other problematic characters
        if any(ord(ch) > 127 and ch not in ' ="\'/-' for ch in tag_content):
            issues_found.append(f"Non-ASCII in tag: <{tag_content}>")
            return f"&lt;{tag_content}&gt;"

        # Otherwise keep as-is (it's a real HTML tag)
        return match.group(0)

    cleaned = re.sub(pattern, replace_tag, content)
    return cleaned, issues_found


def fix_post(post_file):
    """Fix a single post file"""
    try:
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split YAML front matter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                front_matter = parts[1]
                body = parts[2]

                # Only fix the body, not front matter
                cleaned_body, issues = escape_invalid_tags(body)

                if issues:
                    # Reconstruct file
                    cleaned_content = f"---{front_matter}---{cleaned_body}"

                    with open(post_file, 'w', encoding='utf-8') as f:
                        f.write(cleaned_content)

                    return {
                        'file': post_file.name,
                        'status': 'fixed',
                        'issues_count': len(issues),
                        'issues': issues[:5]
                    }
                else:
                    return {
                        'file': post_file.name,
                        'status': 'ok',
                        'issues_count': 0,
                        'issues': []
                    }
        else:
            # No YAML, process entire content
            cleaned_content, issues = escape_invalid_tags(content)

            if issues:
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)

                return {
                    'file': post_file.name,
                    'status': 'fixed',
                    'issues_count': len(issues),
                    'issues': issues[:5]
                }
            else:
                return {
                    'file': post_file.name,
                    'status': 'ok',
                    'issues_count': 0,
                    'issues': []
                }

    except Exception as e:
        return {
            'file': post_file.name,
            'status': 'error',
            'error': str(e)[:100]
        }


def fix_all_posts():
    """Fix HTML tag issues in all posts"""
    posts_dir = Path('_posts')
    results = []

    print("Scanning and fixing HTML tag issues...\n")

    post_files = sorted(posts_dir.glob('*.md'))
    for post_file in tqdm(post_files, desc="Processing", unit="post"):
        result = fix_post(post_file)
        results.append(result)

    return results


if __name__ == '__main__':
    results = fix_all_posts()

    # Summary
    print(f"\n{'='*60}")
    print("HTML TAG FIX SUMMARY")
    print(f"{'='*60}\n")

    fixed = [r for r in results if r['status'] == 'fixed']
    ok = [r for r in results if r['status'] == 'ok']
    errors = [r for r in results if r['status'] == 'error']

    total_issues = sum(r.get('issues_count', 0) for r in fixed)

    print(f"✅ Posts fixed: {len(fixed)}")
    print(f"ℹ️  Posts OK: {len(ok)}")
    if errors:
        print(f"❌ Errors: {len(errors)}")
    print(f"\nTotal invalid tags escaped: {total_issues}\n")

    # Show fixed posts
    if fixed:
        print(f"{'─'*60}")
        print("Posts with invalid HTML tags fixed:")
        print(f"{'─'*60}\n")
        for r in sorted(fixed, key=lambda x: x['issues_count'], reverse=True):
            print(f"📄 {r['file']}")
            print(f"   Tags escaped: {r['issues_count']}")
            if r['issues']:
                for issue in r['issues']:
                    print(f"   - {issue}")
            print()

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
