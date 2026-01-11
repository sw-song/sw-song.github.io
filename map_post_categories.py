#!/usr/bin/env python3
"""
Map each post to its Tistory category by scraping post pages.
Then update Jekyll posts with category information.
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import time
from tqdm import tqdm

TISTORY_URL = "https://songseungwon.tistory.com"

# Main categories mapping (from Tistory)
MAIN_CATEGORIES = {
    "기술": "Technology",
    "도메인": "Domain",
    "튜토리얼": "Tutorial"
}

# Subcategories mapping
SUBCATEGORIES = {
    "서버, 데이터, 클라우드": "Server/Data/Cloud",
    "금융": "Finance",
    "자산운용": "Asset Management",
    "머신러닝, 딥러닝": "ML/DL",
    "웹, 자바스크립트": "Web/JavaScript",
    "인프라, 네트워크": "Infrastructure/Network",
    "비즈니스": "Business",
    "계량 투자 분석": "Quantitative Investment",
    "글로벌 매크로 분석": "Global Macro Analysis",
    "금융 분석 프로그래밍 기초": "Financial Programming Basics",
    "금융 분석 프로그래밍 응용": "Financial Programming Applied",
    "비즈니스 통계 분석 프로그래밍": "Business Analytics Programming",
    "시계열 예측 및 계량 분석 방법론": "Time Series & Quantitative Analysis",
    "자연어 처리 및 텍스트 분석 방법론": "NLP & Text Analysis",
    "통계, 시계열": "Statistics/Time Series"
}

def get_post_category_from_tistory(post_number):
    """
    Fetch a post from Tistory and extract its category.
    Post number can be found from the URL like /123
    """
    try:
        url = f"{TISTORY_URL}/{post_number}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=5)
        response.encoding = 'utf-8'

        if response.status_code == 404:
            return None

        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Try to find category information
        # Tistory usually shows category in the post header or metadata
        category_elem = soup.find('span', {'class': 'category'})
        if not category_elem:
            category_elem = soup.find('a', {'class': 'link_cate'})
        if not category_elem:
            category_elem = soup.find('div', {'class': 'category_text'})

        if category_elem:
            return category_elem.get_text(strip=True)

        return None

    except Exception as e:
        print(f"Error fetching post {post_number}: {e}")
        return None


def infer_category_from_title(filename):
    """
    Infer category from post filename and title.
    This is a fallback method if we can't fetch from Tistory.
    """
    title_lower = filename.lower()

    # JavaScript/Web related
    if any(x in title_lower for x in ['javascript', 'html', 'web', 'css', 'nodejs', 'npm']):
        return "Web/JavaScript"

    # Machine Learning/Deep Learning
    if any(x in title_lower for x in ['machine', 'deep', 'learning', 'neural', 'gan', 'lgbm', 'xgboost', 'sklearn', 'tf-idf', 'lsa']):
        return "ML/DL"

    # Data/Server/Cloud
    if any(x in title_lower for x in ['docker', 'kubernetes', 'elastic', 'kibana', 'gcp', 'cloud', 'database', 'git', 'linux', 'tmux']):
        return "Server/Data/Cloud"

    # Finance related
    if any(x in title_lower for x in ['주식', 'stock', 'etf', 'bitcoin', 'crypto', '가격', 'price', '예측', 'forecast', '금융', 'finance', '투자', 'investment', '주가', 'arima', '회귀', 'regression']):
        return "Finance"

    # Quantitative/Macro Analysis
    if any(x in title_lower for x in ['정량', 'quantitative', 'macro', '매크로', '분석', 'analysis', '경제', 'economic', 'vae', 'var', 'statistical']):
        return "Quantitative Investment"

    # Business Analytics
    if any(x in title_lower for x in ['비즈니스', 'business', '고객', 'customer', '커머스', 'commerce', '분석', '판매', 'sales']):
        return "Business Analytics Programming"

    # NLP
    if any(x in title_lower for x in ['자연어', 'nlp', 'text', 'sentiment', '감성']):
        return "NLP & Text Analysis"

    # Statistics/Time Series
    if any(x in title_lower for x in ['통계', 'statistics', 'time', 'series', '시계열', 'correlation']):
        return "Statistics/Time Series"

    # Default to Technology
    return "Technology"


def update_post_with_category(post_file, category):
    """
    Add or update category in post's YAML front matter.
    """
    try:
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse YAML front matter
        if not content.startswith('---'):
            return False, "No YAML front matter"

        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "Malformed YAML"

        front_matter = parts[1]
        body = parts[2]

        # Check if category already exists
        if 'categories:' in front_matter or 'category:' in front_matter:
            # Remove old category
            front_matter = re.sub(r'^categories?:.*$', '', front_matter, flags=re.MULTILINE)
            front_matter = front_matter.rstrip()

        # Add new category
        # Find the right place to insert (after date)
        if 'date:' in front_matter:
            # Insert after date line
            front_matter = re.sub(
                r'(date: [^\n]+\n)',
                r'\1categories: ["' + category + '"]\n',
                front_matter
            )
        else:
            # Insert at the end of front matter
            front_matter = front_matter.rstrip() + f'\ncategories: ["{category}"]'

        # Reconstruct the file
        new_content = f"---{front_matter}\n---{body}"

        with open(post_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True, category

    except Exception as e:
        return False, str(e)


def main():
    """Main function to map and update categories"""
    posts_dir = Path('_posts')
    results = []

    print("\n" + "=" * 70)
    print("MAPPING POSTS TO CATEGORIES")
    print("=" * 70 + "\n")

    post_files = sorted(posts_dir.glob('*.md'))

    for post_file in tqdm(post_files, desc="Processing", unit="post"):
        # Infer category from filename
        filename = post_file.stem  # Remove .md extension
        category = infer_category_from_title(filename)

        # Update post with category
        success, result = update_post_with_category(post_file, category)

        results.append({
            'file': post_file.name,
            'category': category if success else "ERROR",
            'success': success
        })

        # Be nice to the server
        time.sleep(0.1)

    # Summary
    print("\n" + "=" * 70)
    print("CATEGORIZATION SUMMARY")
    print("=" * 70 + "\n")

    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    print(f"✅ Successfully categorized: {len(successful)}")
    print(f"❌ Failed: {len(failed)}\n")

    # Group by category
    categories_count = {}
    for r in successful:
        cat = r['category']
        categories_count[cat] = categories_count.get(cat, 0) + 1

    print("Category Distribution:")
    print("─" * 70)
    for cat, count in sorted(categories_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count} posts")

    if failed:
        print("\n" + "─" * 70)
        print("Failed posts:")
        for r in failed:
            print(f"  {r['file']}: {r['category']}")

    print("\n" + "=" * 70)
    print(f"Total processed: {len(results)}")
    print("=" * 70 + "\n")

    return results


if __name__ == '__main__':
    results = main()
