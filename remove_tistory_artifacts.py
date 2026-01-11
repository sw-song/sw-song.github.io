#!/usr/bin/env python3
"""
Remove Tistory blog artifacts from migrated posts.
These unnecessary texts appear at the bottom of each post from the original blog.
"""

from pathlib import Path
from tqdm import tqdm
import re

ARTIFACTS_TO_REMOVE = [
    r"^\s*공유하기\s*$",
    r"^\s*게시글 관리\s*$",
    r"^\s*관성을 이기는 데이터\s*$",
    r"^\s*저작자표시\s*\(새창열림\)\s*$",
    r"^\s*저작자표시 \(새창열림\)\s*$",
    r"^\s*새창열림\s*$",
]

def remove_tistory_artifacts(content):
    """Remove Tistory artifacts from post content"""
    lines = content.split('\n')
    cleaned_lines = []
    removed_count = 0

    for line in lines:
        # Check if this line matches any artifact pattern
        should_remove = False
        for pattern in ARTIFACTS_TO_REMOVE:
            if re.match(pattern, line):
                should_remove = True
                removed_count += 1
                break

        if not should_remove:
            cleaned_lines.append(line)

    # Remove excessive blank lines at the end
    while cleaned_lines and cleaned_lines[-1].strip() == '':
        cleaned_lines.pop()

    return '\n'.join(cleaned_lines), removed_count


def clean_post(post_file):
    """Clean a single post file"""
    try:
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned_content, removed_count = remove_tistory_artifacts(content)

        if removed_count > 0:
            with open(post_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)

            return {
                'file': post_file.name,
                'status': 'cleaned',
                'lines_removed': removed_count
            }
        else:
            return {
                'file': post_file.name,
                'status': 'ok',
                'lines_removed': 0
            }

    except Exception as e:
        return {
            'file': post_file.name,
            'status': 'error',
            'error': str(e)[:100]
        }


def clean_all_posts():
    """Clean all posts"""
    posts_dir = Path('_posts')
    results = []

    print("Removing Tistory artifacts from posts...\n")

    post_files = sorted(posts_dir.glob('*.md'))
    for post_file in tqdm(post_files, desc="Processing", unit="post"):
        result = clean_post(post_file)
        results.append(result)

    return results


if __name__ == '__main__':
    results = clean_all_posts()

    # Summary
    print(f"\n{'='*60}")
    print("TISTORY ARTIFACT REMOVAL SUMMARY")
    print(f"{'='*60}\n")

    cleaned = [r for r in results if r['status'] == 'cleaned']
    ok = [r for r in results if r['status'] == 'ok']
    errors = [r for r in results if r['status'] == 'error']

    total_lines_removed = sum(r.get('lines_removed', 0) for r in cleaned)

    print(f"✅ Posts cleaned: {len(cleaned)}")
    print(f"ℹ️  Posts OK: {len(ok)}")
    if errors:
        print(f"❌ Errors: {len(errors)}")
    print(f"\nTotal lines removed: {total_lines_removed}\n")

    # Show cleaned posts
    if cleaned:
        print(f"{'─'*60}")
        print("Posts cleaned:")
        print(f"{'─'*60}\n")
        for r in sorted(cleaned, key=lambda x: x['lines_removed'], reverse=True):
            print(f"📄 {r['file']}")
            print(f"   Lines removed: {r['lines_removed']}\n")

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
