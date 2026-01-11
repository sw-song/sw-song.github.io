#!/usr/bin/env python3
"""
Identify problematic posts with control characters or YAML issues
"""

import os
import yaml
import re
from pathlib import Path


def has_control_characters(text):
    """Check if text contains control characters"""
    return any(ord(ch) < 32 and ch not in '\n\t\r' for ch in text)


def scan_posts():
    """Scan all posts for issues"""
    posts_dir = Path('_posts')
    issues = []
    valid_count = 0

    print("Scanning posts...")

    for post_file in sorted(posts_dir.glob('*.md')):
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()

            file_issues = []

            # Check filename
            if has_control_characters(post_file.name):
                file_issues.append('Control characters in filename')

            # Check YAML front matter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 2:
                    try:
                        yaml.safe_load(parts[1])
                    except yaml.YAMLError as e:
                        file_issues.append(f'YAML parse error')

            # Check for control characters in content
            if has_control_characters(content):
                file_issues.append('Control characters in content')

            if file_issues:
                issues.append({
                    'file': post_file.name,
                    'issues': file_issues
                })
            else:
                valid_count += 1

        except Exception as e:
            issues.append({
                'file': post_file.name,
                'issues': [f'Read error: {str(e)[:50]}']
            })

    return issues, valid_count


if __name__ == '__main__':
    issues, valid_count = scan_posts()

    print(f"\n{'='*60}")
    print(f"Valid posts: {valid_count}")
    print(f"Problematic posts: {len(issues)}")
    print(f"{'='*60}\n")

    if issues:
        print("Problematic posts found:\n")
        for issue in issues:
            print(f"📄 {issue['file']}")
            for problem in issue['issues']:
                print(f"   ⚠️  {problem}")
            print()
    else:
        print("✅ No problematic posts found!")
