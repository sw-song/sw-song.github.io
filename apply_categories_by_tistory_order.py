#!/usr/bin/env python3
"""
Apply categories to GitHub blog posts based on Tistory post ordering.

Strategy:
- Tistory posts are ordered from newest (top) to oldest (bottom)
- Posts are numbered (date descending)
- Use post order + Tistory category distribution to assign categories
"""

from pathlib import Path
import re
from tqdm import tqdm
import yaml
from collections import defaultdict

# Tistory category structure with post counts
# Posts are ordered from most recent to oldest
# We know the distribution and can estimate which posts belong to which category

TISTORY_DISTRIBUTION = [
    # 4. 실전 categories (most recent posts)
    (5, "4. 실전", "글로벌 매크로 분석"),           # 5 recent posts
    (3, "4. 실전", "계량 투자 분석"),               # 3 posts

    # 3. 튜토리얼 categories
    (11, "3. 튜토리얼", "금융 분석 프로그래밍 응용"),    # 11 posts - APPLIED
    (6, "3. 튜토리얼", "금융 분석 프로그래밍 기초"),    # 6 posts - BASICS (including supplements)
    (6, "3. 튜토리얼", "비즈니스 통계 분석 프로그래밍"),  # 6 posts
    (4, "3. 튜토리얼", "시계열 예측 및 계량 분석 방법론"), # 4 posts
    (2, "3. 튜토리얼", "자연어 처리 및 텍스트 분석 방법론"), # 2 posts

    # 2. 도메인 categories
    (1, "2. 도메인", "자산운용"),                   # 1 post
    (6, "2. 도메인", "금융"),                       # 6 posts
    (2, "2. 도메인", "비즈니스"),                    # 2 posts

    # 1. 기술 categories (oldest posts, highest volume)
    (7, "1. 기술", "통계, 시계열"),                 # 7 posts
    (24, "1. 기술", "머신러닝, 딥러닝"),             # 24 posts
    (20, "1. 기술", "서버, 데이터, 클라우드"),        # 20 posts
    (15, "1. 기술", "웹, 자바스크립트"),             # 15 posts
    (0, "1. 기술", "인프라, 네트워크"),              # 0 posts
]

def build_category_assignment(posts):
    """
    Build category assignment based on post order.
    Posts are typically ordered from newest to oldest in GitHub (matching Tistory order).
    Assign categories based on the Tistory distribution.
    """

    # Calculate cumulative positions
    assignment = {}
    current_pos = 0

    for count, main_cat, sub_cat in TISTORY_DISTRIBUTION:
        for i in range(count):
            if current_pos < len(posts):
                assignment[posts[current_pos]] = [main_cat, sub_cat]
                current_pos += 1

    return assignment, current_pos


def update_post_with_category(post_file, categories):
    """Update post's YAML with new category"""
    try:
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return False, "No YAML front matter"

        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "Malformed YAML"

        front_matter = parts[1]
        body = parts[2]

        # Remove old categories
        front_matter = re.sub(r'^categories:.*$', '', front_matter, flags=re.MULTILINE)
        front_matter = re.sub(r'\n\n+', '\n', front_matter)

        # Add new category
        cat_str = str(categories).replace("'", '"')
        if 'date:' in front_matter:
            front_matter = re.sub(
                r'(date: [^\n]+)(\n)?',
                r'\1\ncategories: ' + cat_str + '\n',
                front_matter
            )
        else:
            front_matter = front_matter.rstrip() + f'\ncategories: {cat_str}'

        # Reconstruct
        new_content = f"---{front_matter}\n---{body}"
        with open(post_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True, categories

    except Exception as e:
        return False, str(e)


def main():
    """Main function"""
    posts_dir = Path('_posts')

    print("\n" + "=" * 90)
    print("APPLYING CATEGORIES BY TISTORY POST ORDERING")
    print("=" * 90 + "\n")

    # Get all posts sorted by date (descending - newest first, matching Tistory order)
    post_files = sorted(posts_dir.glob('*.md'), reverse=True)
    post_names = [p.name for p in post_files]

    print(f"Total posts in GitHub: {len(post_names)}")
    print(f"Posts in Tistory: 112")
    print(f"Extra posts (not in Tistory): {len(post_names) - 112}")
    print()

    # Skip the newest post(s) that are not in Tistory (e.g., migration guide)
    # These are typically the most recent posts
    posts_to_assign = post_names[len(post_names) - 112:]  # Take 112 oldest posts (Tistory posts)
    extra_posts = post_names[:len(post_names) - 112]      # Skip 1 newest post

    print(f"Posts to assign from Tistory structure: {len(posts_to_assign)}")
    print(f"Extra posts (will keep current category): {len(extra_posts)}")
    if extra_posts:
        print(f"  Extra posts: {extra_posts}")
    print()

    # Build category assignment for Tistory posts only
    assignment, assigned_count = build_category_assignment(posts_to_assign)

    print(f"Posts assigned: {assigned_count}/{len(post_names)}")
    if assigned_count < len(post_names):
        print(f"⚠️  {len(post_names) - assigned_count} posts could not be assigned (mismatch with Tistory count)")
    print()

    # Apply categories
    results = []
    category_counts = defaultdict(int)

    for post_file in tqdm(post_files, desc="Processing", unit="post"):
        post_name = post_file.name

        if post_name in assignment:
            categories = assignment[post_name]
            success, result = update_post_with_category(post_file, categories)

            if success:
                cat_key = str(categories)
                category_counts[cat_key] += 1
                results.append({'file': post_name, 'categories': categories, 'success': True})
            else:
                results.append({'file': post_name, 'categories': result, 'success': False})
        else:
            results.append({'file': post_name, 'categories': "NOT_ASSIGNED", 'success': False})

    # Print summary
    print("\n" + "=" * 90)
    print("CATEGORIZATION RESULTS")
    print("=" * 90 + "\n")

    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    print(f"✅ Successfully categorized: {len(successful)}")
    print(f"❌ Failed: {len(failed)}\n")

    print("Category Distribution:")
    print("-" * 90)
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count} posts")

    # Verify against Tistory structure
    print("\n" + "=" * 90)
    print("VERIFICATION AGAINST TISTORY STRUCTURE")
    print("=" * 90 + "\n")

    tistory_structure = {
        "1. 기술": {
            "인프라, 네트워크": 0,
            "서버, 데이터, 클라우드": 20,
            "웹, 자바스크립트": 15,
            "머신러닝, 딥러닝": 24,
            "통계, 시계열": 7,
        },
        "2. 도메인": {
            "금융": 6,
            "비즈니스": 2,
            "자산운용": 1,
        },
        "3. 튜토리얼": {
            "금융 분석 프로그래밍 기초": 6,
            "금융 분석 프로그래밍 응용": 11,
            "비즈니스 통계 분석 프로그래밍": 6,
            "시계열 예측 및 계량 분석 방법론": 4,
            "자연어 처리 및 텍스트 분석 방법론": 2,
        },
        "4. 실전": {
            "글로벌 매크로 분석": 5,
            "계량 투자 분석": 3,
        },
    }

    current_structure = {}
    for post_file in posts_dir.glob('*.md'):
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if content.startswith('---'):
            parts = content.split('---', 2)
            try:
                front_matter = yaml.safe_load(parts[1])
                if front_matter and 'categories' in front_matter:
                    cats = front_matter['categories']
                    if len(cats) == 2:
                        main, sub = cats
                        if main not in current_structure:
                            current_structure[main] = {}
                        current_structure[main][sub] = current_structure[main].get(sub, 0) + 1
            except:
                pass

    print(f"{'Main Category':<30} {'Subcategory':<40} {'Tistory':<10} {'Current':<10} {'Match':<10}")
    print("-" * 90)

    all_match = True
    for main_name in sorted(tistory_structure.keys()):
        tist_subs = tistory_structure[main_name]
        curr_subs = current_structure.get(main_name, {})

        for sub_name in sorted(tist_subs.keys()):
            tist_count = tist_subs[sub_name]
            curr_count = curr_subs.get(sub_name, 0)
            match = "✅" if tist_count == curr_count else "❌"

            if tist_count != curr_count:
                all_match = False

            print(f"{main_name:<30} {sub_name:<40} {tist_count:<10} {curr_count:<10} {match:<10}")

    print("\n" + "=" * 90)
    print(f"Total processed: {len(results)}")
    print("=" * 90 + "\n")

    if all_match:
        print("✅ ALL CATEGORIES NOW MATCH TISTORY STRUCTURE PERFECTLY!")
    else:
        print("⚠️  Some categories still don't match. Review assignment logic.")

    return results


if __name__ == '__main__':
    results = main()
