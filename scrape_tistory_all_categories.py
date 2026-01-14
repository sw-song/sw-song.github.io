#!/usr/bin/env python3
"""
Scrape all posts from Tistory category pages to build complete post-to-category mapping.

This script:
1. Fetches each Tistory category page
2. Extracts all posts from the category
3. Builds a complete mapping of post_title -> category
4. Saves to JSON for use in matching
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from tqdm import tqdm
from collections import defaultdict

# Tistory categories structure
TISTORY_CATEGORIES = {
    "1. 기술": {
        "인프라, 네트워크": "/category/1.%20%EA%B8%B0%EC%88%A0/%EC%9D%B8%ED%94%84%EB%9D%BC%2C%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC",
        "서버, 데이터, 클라우드": "/category/1.%20%EA%B8%B0%EC%88%A0/%EC%84%9C%EB%B2%84%2C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%2C%20%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C",
        "웹, 자바스크립트": "/category/1.%20%EA%B8%B0%EC%88%A0/%EC%9B%B9%2C%20%EC%9E%90%EB%B0%94%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8",
        "머신러닝, 딥러닝": "/category/1.%20%EA%B8%B0%EC%88%A0/%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D%2C%20%EB%94%A5%EB%9F%AC%EB%8B%9D",
        "통계, 시계열": "/category/1.%20%EA%B8%B0%EC%88%A0/%ED%86%B5%EA%B3%84%2C%20%EC%8B%9C%EA%B3%84%EC%97%B4",
    },
    "2. 도메인": {
        "금융": "/category/2.%20%EB%8F%84%EB%A9%94%EC%9D%B8/%EA%B8%88%EC%9C%B5",
        "비즈니스": "/category/2.%20%EB%8F%84%EB%A9%94%EC%9D%B8/%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4",
        "자산운용": "/category/2.%20%EB%8F%84%EB%A9%94%EC%9D%B8/%EC%9E%90%EC%82%B0%EC%9A%B4%EC%9A%A9",
    },
    "3. 튜토리얼": {
        "금융 분석 프로그래밍 기초": "/category/3.%20%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC/%EA%B8%88%EC%9C%B5%20%EB%B6%84%EC%84%9D%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%20%EA%B8%B0%EC%B4%88",
        "금융 분석 프로그래밍 응용": "/category/3.%20%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC/%EA%B8%88%EC%9C%B5%20%EB%B6%84%EC%84%9D%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%20%EC%9D%91%EC%9A%A9",
        "비즈니스 통계 분석 프로그래밍": "/category/3.%20%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC/%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%20%ED%86%B5%EA%B3%84%20%EB%B6%84%EC%84%9D%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D",
        "시계열 예측 및 계량 분석 방법론": "/category/3.%20%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC/%EC%8B%9C%EA%B3%84%EC%97%B4%20%EC%98%88%EC%B8%A1%20%EB%B0%8F%20%EA%B3%84%EB%9F%89%20%EB%B6%84%EC%84%9D%20%EB%B0%A9%EB%B2%95%EB%A1%A0",
        "자연어 처리 및 텍스트 분석 방법론": "/category/3.%20%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC/%EC%9E%90%EC%97%B0%EC%96%B4%20%EC%B2%98%EB%A6%AC%20%EB%B0%8F%20%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EB%B6%84%EC%84%9D%20%EB%B0%A9%EB%B2%95%EB%A1%A0",
    },
    "4. 실전": {
        "글로벌 매크로 분석": "/category/4.%20%EC%8B%A4%EC%A0%84/%EA%B8%80%EB%A1%9C%EB%B2%8C%20%EB%A7%A4%ED%81%AC%EB%A1%9C%20%EB%B6%84%EC%84%9D",
        "계량 투자 분석": "/category/4.%20%EC%8B%A4%EC%A0%84/%EA%B3%84%EB%9F%89%20%ED%88%AC%EC%9E%90%20%EB%B6%84%EC%84%9D",
    },
}

BASE_URL = "https://songseungwon.tistory.com"

def fetch_category_posts(category_path, main_cat, sub_cat):
    """
    Fetch all posts from a category page.

    Returns:
        list of dicts: [{"title": "...", "url": "...", "post_id": "...", "category": "main/sub"}, ...]
    """
    posts = []
    url = f"{BASE_URL}{category_path}"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all post links in the category
        # Tistory uses different selectors, try multiple approaches

        # Method 1: Look for post items with common Tistory selectors
        post_items = soup.find_all('div', {'class': ['post-item', 'item', 'article-item']})

        if not post_items:
            # Method 2: Look for links that look like post links
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href', '')
                # Post URLs typically have numeric IDs: /123
                if href.startswith('/') and href[-1].isdigit():
                    title = link.get_text(strip=True)
                    if title:
                        post_id = href.strip('/')
                        posts.append({
                            'title': title,
                            'url': f"{BASE_URL}{href}",
                            'post_id': post_id,
                            'category': f"{main_cat}/{sub_cat}"
                        })
        else:
            # Parse post items
            for item in post_items:
                # Extract title
                title_elem = item.find('a', {'class': 'title'}) or item.find('a')
                if not title_elem:
                    title_elem = item.find('span', {'class': 'title'})

                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True) if title_elem else "Unknown"

                # Extract URL
                link_elem = item.find('a', href=True)
                if link_elem:
                    href = link_elem.get('href', '')
                    # Extract post ID from URL
                    post_id = href.split('/')[-1]

                    posts.append({
                        'title': title,
                        'url': href if href.startswith('http') else f"{BASE_URL}{href}",
                        'post_id': post_id,
                        'category': f"{main_cat}/{sub_cat}"
                    })

        return posts

    except Exception as e:
        print(f"Error fetching {main_cat}/{sub_cat}: {e}")
        return []


def main():
    """Main scraping function"""

    print("\n" + "=" * 90)
    print("SCRAPING TISTORY CATEGORIES FOR ALL POSTS")
    print("=" * 90 + "\n")

    all_posts = []
    total_expected = 0

    # Count total expected posts
    for main_cat in TISTORY_CATEGORIES:
        for sub_cat in TISTORY_CATEGORIES[main_cat]:
            subcats = TISTORY_CATEGORIES[main_cat]
            total_expected += 1  # Just count categories

    # Fetch posts from each category
    category_count = 0
    for main_cat in sorted(TISTORY_CATEGORIES.keys()):
        sub_categories = TISTORY_CATEGORIES[main_cat]

        for sub_cat in sorted(sub_categories.keys()):
            category_count += 1
            category_path = sub_categories[sub_cat]

            print(f"[{category_count}] Fetching {main_cat} > {sub_cat}...")

            posts = fetch_category_posts(category_path, main_cat, sub_cat)
            all_posts.extend(posts)

            print(f"  → Found {len(posts)} posts")

            # Be nice to Tistory servers
            time.sleep(0.5)

    print(f"\n{'='*90}")
    print(f"SCRAPING COMPLETE")
    print(f"{'='*90}")
    print(f"Total posts found: {len(all_posts)}")
    print()

    # Show distribution
    category_dist = defaultdict(int)
    for post in all_posts:
        category_dist[post['category']] += 1

    print("Distribution by category:")
    print("-" * 90)
    for cat in sorted(category_dist.keys()):
        print(f"  {cat}: {category_dist[cat]} posts")

    # Save to JSON
    output_file = 'tistory_all_posts_categories.json'
    output_data = {
        'total': len(all_posts),
        'scraped_at': str(time.time()),
        'posts': all_posts,
        'category_distribution': dict(category_dist)
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Saved to {output_file}")
    print()

    return all_posts


if __name__ == '__main__':
    posts = main()
