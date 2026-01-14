#!/usr/bin/env python3
"""
Match GitHub blog posts to Tistory posts using title similarity.

Strategy:
1. Load GitHub posts with titles and dates
2. Load Tistory posts with titles and categories
3. For each GitHub post, find best matching Tistory post
4. Use exact match, fuzzy match, or date match
5. Generate mapping JSON with confidence scores
"""

import json
from pathlib import Path
import yaml
from difflib import SequenceMatcher
from collections import defaultdict

def similarity(a, b):
    """Calculate string similarity ratio (0-1)"""
    return SequenceMatcher(None, a, b).ratio()

def load_github_posts():
    """Load all GitHub posts with title and date"""
    posts_dir = Path("_posts")
    github_posts = {}

    for post_file in sorted(posts_dir.glob("*.md")):
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if content.startswith('---'):
            parts = content.split('---', 2)
            try:
                front_matter = yaml.safe_load(parts[1])
                if front_matter:
                    title = front_matter.get('title', post_file.stem)
                    date = str(front_matter.get('date', ''))
                    github_posts[post_file.name] = {
                        'title': title,
                        'date': date,
                        'title_lower': title.lower()
                    }
            except:
                pass

    return github_posts


def load_tistory_posts():
    """Load Tistory posts from scraped JSON"""
    try:
        with open('tistory_all_posts_categories.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['posts']
    except FileNotFoundError:
        print("Error: tistory_all_posts_categories.json not found. Run scraper first.")
        return []


def find_best_match(github_post, tistory_posts, github_file):
    """
    Find the best matching Tistory post for a GitHub post.

    Matching strategy:
    1. Exact title match (case-insensitive)
    2. High similarity fuzzy match (> 0.85)
    3. Check for known title variations
    4. Return best match with confidence score
    """

    github_title = github_post['title'].lower()
    github_title_orig = github_post['title']

    best_match = None
    best_score = 0
    best_method = None

    # Strategy 1: Exact match (case-insensitive)
    for tistory_post in tistory_posts:
        tistory_title = tistory_post['title'].lower()
        if github_title == tistory_title:
            return {
                'tistory_post': tistory_post,
                'confidence': 1.0,
                'method': 'exact_match'
            }

    # Strategy 2: Handle common transformations
    # GitHub posts may have titles with hyphens changed to spaces or vice versa
    github_title_normalized = github_title.replace('-', ' ').replace('_', ' ')
    github_title_normalized = ' '.join(github_title_normalized.split())  # Normalize spaces

    for tistory_post in tistory_posts:
        tistory_title = tistory_post['title'].lower()
        tistory_title_normalized = tistory_title.replace('-', ' ').replace('_', ' ')
        tistory_title_normalized = ' '.join(tistory_title_normalized.split())

        if github_title_normalized == tistory_title_normalized:
            return {
                'tistory_post': tistory_post,
                'confidence': 0.99,
                'method': 'normalized_match'
            }

    # Strategy 3: Fuzzy matching (high similarity)
    for tistory_post in tistory_posts:
        tistory_title = tistory_post['title'].lower()

        # Try different normalization approaches for fuzzy matching
        variants = [
            (github_title, tistory_title),
            (github_title_normalized, tistory_title_normalized),
            (github_title.replace('[', '').replace(']', ''), tistory_title.replace('[', '').replace(']', '')),
        ]

        for variant_gh, variant_tist in variants:
            score = similarity(variant_gh, variant_tist)

            if score > best_score:
                best_score = score
                best_match = tistory_post
                best_method = 'fuzzy_match'

    if best_score > 0.85:
        return {
            'tistory_post': best_match,
            'confidence': best_score,
            'method': best_method
        }

    # Strategy 4: If still no match, return None
    return None


def main():
    """Main matching function"""

    print("\n" + "=" * 100)
    print("MATCHING GITHUB POSTS TO TISTORY POSTS")
    print("=" * 100 + "\n")

    # Load posts
    print("Loading GitHub posts...")
    github_posts = load_github_posts()
    print(f"  → Loaded {len(github_posts)} GitHub posts\n")

    print("Loading Tistory posts...")
    tistory_posts = load_tistory_posts()
    print(f"  → Loaded {len(tistory_posts)} Tistory posts\n")

    # Match posts
    matches = []
    unmatched = []
    matched_count = 0

    print("Matching posts...")
    print("-" * 100)

    for github_file, github_post in sorted(github_posts.items()):
        match_result = find_best_match(github_post, tistory_posts, github_file)

        if match_result and match_result['confidence'] > 0.7:
            matched_count += 1
            tistory_post = match_result['tistory_post']

            matches.append({
                'github_file': github_file,
                'github_title': github_post['title'],
                'github_date': github_post['date'],
                'tistory_title': tistory_post['title'],
                'tistory_url': tistory_post['url'],
                'category': tistory_post['category'],
                'confidence': match_result['confidence'],
                'method': match_result['method']
            })

            print(f"✅ {github_file}")
            print(f"   → {github_post['title'][:70]}")
            print(f"   → Category: {tistory_post['category']} (conf: {match_result['confidence']:.2f})")
        else:
            unmatched.append({
                'github_file': github_file,
                'github_title': github_post['title'],
                'github_date': github_post['date'],
                'reason': 'No good match found'
            })
            print(f"❌ {github_file}")
            print(f"   → {github_post['title'][:70]}")
            print(f"   → No match (migration guide or new post)")

    print()
    print("=" * 100)
    print(f"MATCHING COMPLETE")
    print("=" * 100)
    print(f"\n✅ Matched: {matched_count}/{len(github_posts)}")
    print(f"❌ Unmatched: {len(unmatched)}/{len(github_posts)}\n")

    # Show distribution of matches by category
    category_dist = defaultdict(int)
    for match in matches:
        category_dist[match['category']] += 1

    print("Matched posts by category:")
    print("-" * 100)
    for cat in sorted(category_dist.keys()):
        print(f"  {cat}: {category_dist[cat]} posts")

    # Save mapping
    output_file = 'github_to_tistory_mapping.json'
    output_data = {
        'total_github_posts': len(github_posts),
        'matched': len(matches),
        'unmatched': len(unmatched),
        'match_rate': f"{len(matches) / len(github_posts) * 100:.1f}%",
        'matches': matches,
        'unmatched_files': unmatched,
        'category_distribution': dict(category_dist)
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Saved mapping to {output_file}")

    # Show unmatched files
    if unmatched:
        print(f"\nUnmatched files ({len(unmatched)}):")
        print("-" * 100)
        for post in unmatched:
            print(f"  {post['github_file']}: {post['github_title'][:70]}")

    return matches, unmatched


if __name__ == '__main__':
    matches, unmatched = main()
