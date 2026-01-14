#!/usr/bin/env python3
"""
Apply accurate categories using keyword matching with category quotas.

Strategy:
- Use keyword patterns for each category
- Assign with category quota limits (match Tistory counts exactly)
- When multiple categories match, use confidence scoring
- Fill remaining with heuristics
"""

from pathlib import Path
import re
import yaml
from tqdm import tqdm
from collections import defaultdict

# Tistory structure with post counts (our targets)
CATEGORY_QUOTAS = {
    ("1. 기술", "인프라, 네트워크"): 0,
    ("1. 기술", "서버, 데이터, 클라우드"): 20,
    ("1. 기술", "웹, 자바스크립트"): 15,
    ("1. 기술", "머신러닝, 딥러닝"): 24,
    ("1. 기술", "통계, 시계열"): 7,
    ("2. 도메인", "금융"): 6,
    ("2. 도메인", "비즈니스"): 2,
    ("2. 도메인", "자산운용"): 1,
    ("3. 튜토리얼", "금융 분석 프로그래밍 기초"): 6,
    ("3. 튜토리얼", "금융 분석 프로그래밍 응용"): 11,
    ("3. 튜토리얼", "비즈니스 통계 분석 프로그래밍"): 6,
    ("3. 튜토리얼", "시계열 예측 및 계량 분석 방법론"): 4,
    ("3. 튜토리얼", "자연어 처리 및 텍스트 분석 방법론"): 2,
    ("4. 실전", "글로벌 매크로 분석"): 5,
    ("4. 실전", "계량 투자 분석"): 3,
}

# Keyword patterns for each category (use both positive keywords and negative keywords)
KEYWORDS = {
    ("1. 기술", "웹, 자바스크립트"): {
        'positive': [r'javascript', r'html', r'css', r'nodejs', r'npm', r'web\s', r'django', r'flask', r'react', r'vue'],
        'negative': []
    },
    ("1. 기술", "서버, 데이터, 클라우드"): {
        'positive': [r'docker', r'kubernetes', r'elastic', r'kibana', r'gcp', r'cloud', r'firestore', r'database', r'mysql', r'git\s', r'linux', r'tmux', r'dolt', r'redis'],
        'negative': []
    },
    ("1. 기술", "머신러닝, 딥러닝"): {
        'positive': [r'gan', r'stargan', r'stylegan', r'cnn', r'rnn', r'neural', r'deep\slearning', r'machine\slearning', r'xgboost', r'lgbm', r'sklearn', r'precision', r'recall', r'roc\scurve', r'classification'],
        'negative': []
    },
    ("1. 기술", "통계, 시계열"): {
        'positive': [r'통계', r'correlation', r'hypothesis', r'kolmogorov', r'confusion_matrix'],
        'negative': [r'arima', r'var\s', r'방법론']
    },
    ("2. 도메인", "자산운용"): {
        'positive': [r'자산운용', r'etf', r'포트폴리오', r'계좌', r'절세'],
        'negative': []
    },
    ("2. 도메인", "금융"): {
        'positive': [r'주식', r'bitcoin', r'crypto', r'가격', r'valuation', r'국채', r'금리', r'배수', r'배당', r'회귀모형', r'리세션'],
        'negative': []
    },
    ("2. 도메인", "비즈니스"): {
        'positive': [r'넷플릭스', r'비즈니스\s', r'커머스\s'],
        'negative': [r'프로그래밍', r'분석을']
    },
    ("3. 튜토리얼", "금융 분석 프로그래밍 기초"): {
        'positive': [r'금융 분석을 위한 파이썬', r'\s01\.', r'\s02\.', r'\s03\.', r'보충자료'],
        'negative': [r'04\.', r'05\.', r'06\.']
    },
    ("3. 튜토리얼", "금융 분석 프로그래밍 응용"): {
        'positive': [r'금융 분석을 위한 파이썬', r'\s04\.', r'\s05\.', r'\s06\.'],
        'negative': [r'01\.', r'02\.', r'03\.', r'보충자료']
    },
    ("3. 튜토리얼", "비즈니스 통계 분석 프로그래밍"): {
        'positive': [r'비즈니스.*프로그래밍', r'고객.*세분화', r'커머스.*분석'],
        'negative': []
    },
    ("3. 튜토리얼", "시계열 예측 및 계량 분석 방법론"): {
        'positive': [r'arima', r'var\s', r'벡터자기회귀', r'시계열 예측', r'계량 분석 방법론', r'시계열 패턴'],
        'negative': []
    },
    ("3. 튜토리얼", "자연어 처리 및 텍스트 분석 방법론"): {
        'positive': [r'자연어', r'nlp', r'tf-idf', r'lsa', r'감성', r'뉴스', r'기사', r'similarity', r'sentiment'],
        'negative': []
    },
    ("4. 실전", "계량 투자 분석"): {
        'positive': [r'\[파이썬 퀀트', r'백테', r'멀티플', r'피어 그룹', r'스크리닝', r'존버'],
        'negative': []
    },
    ("4. 실전", "글로벌 매크로 분석"): {
        'positive': [r'글로벌', r'매크로', r'달러', r'유동성', r'부채', r'리세션', r'경기 침체'],
        'negative': []
    },
}

def score_category(title, category):
    """
    Score how well a title matches a category.
    Returns 0-100 confidence score.
    """
    title_lower = title.lower()

    if category not in KEYWORDS:
        return 0

    keywords = KEYWORDS[category]

    # Check positive keywords
    positive_matches = 0
    for pattern in keywords['positive']:
        if re.search(pattern, title_lower, re.IGNORECASE):
            positive_matches += 1

    # Check negative keywords (reduce score)
    negative_matches = 0
    for pattern in keywords['negative']:
        if re.search(pattern, title_lower, re.IGNORECASE):
            negative_matches += 1

    # Calculate score
    if positive_matches == 0:
        return 0

    score = (positive_matches * 30) - (negative_matches * 20)
    return max(0, score)


def load_posts():
    """Load all posts with their current categories"""
    posts_dir = Path("_posts")
    posts = []

    for post_file in sorted(posts_dir.glob("*.md"), reverse=True):  # Newest first
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if content.startswith('---'):
            parts = content.split('---', 2)
            try:
                front_matter = yaml.safe_load(parts[1])
                if front_matter:
                    posts.append({
                        'filename': post_file.name,
                        'title': front_matter.get('title', post_file.stem),
                        'date': front_matter.get('date', ''),
                        'old_category': front_matter.get('categories', []),
                    })
            except:
                pass

    return posts


def assign_categories(posts):
    """Assign categories to posts respecting quotas"""

    # Collect all scores
    print("\nScoring all posts for each category...")
    scores = []  # List of (filename, scores_dict)

    for post in tqdm(posts, desc="Scoring", unit="post"):
        post_scores = {}
        for category in CATEGORY_QUOTAS.keys():
            score = score_category(post['title'], category)
            if score > 0:
                post_scores[category] = score

        if post_scores:  # Only include if it has some matches
            scores.append((post['filename'], post_scores, post['title']))

    # Assign categories greedily, respecting quotas
    print(f"\nAssigning categories (respecting {len(CATEGORY_QUOTAS)} quotas)...")

    assignments = {}  # filename -> category
    remaining_quota = CATEGORY_QUOTAS.copy()

    # First pass: high confidence assignments
    sorted_posts = sorted(scores, key=lambda x: max(x[1].values()), reverse=True)

    for filename, post_scores, title in sorted_posts:
        if filename in assignments:
            continue  # Already assigned

        # Find best category with available quota
        best_category = None
        best_score = 0

        for category, score in sorted(post_scores.items(), key=lambda x: x[1], reverse=True):
            if remaining_quota[category] > 0 and score > best_score:
                best_category = category
                best_score = score

        if best_category:
            assignments[filename] = best_category
            remaining_quota[best_category] -= 1

    # Second pass: fill remaining unassigned posts using default heuristics
    for post in posts:
        if post['filename'] not in assignments:
            # Try to find ANY category with quota
            found = False
            for category in sorted(CATEGORY_QUOTAS.keys()):
                if remaining_quota[category] > 0:
                    # Use this as fallback
                    assignments[post['filename']] = category
                    remaining_quota[category] -= 1
                    found = True
                    break

            if not found:
                # Assign to default
                assignments[post['filename']] = ("1. 기술", "머신러닝, 딥러닝")

    return assignments


def main():
    """Main function"""

    print("\n" + "=" * 90)
    print("APPLY ACCURATE CATEGORIES WITH QUOTA CONSTRAINTS")
    print("=" * 90)

    # Load posts
    print("\nLoading posts...")
    posts = load_posts()
    print(f"Loaded {len(posts)} posts")

    # Assign categories
    assignments = assign_categories(posts)

    # Update posts
    print(f"\nUpdating {len(assignments)} posts with accurate categories...")
    posts_dir = Path("_posts")

    for post in tqdm(posts, desc="Updating", unit="post"):
        if post['filename'] not in assignments:
            continue

        post_file = posts_dir / post['filename']
        new_category = assignments[post['filename']]

        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if content.startswith('---'):
            parts = content.split('---', 2)
            front_matter = parts[1]
            body = parts[2]

            # Remove old categories
            front_matter = re.sub(r'^categories:.*$', '', front_matter, flags=re.MULTILINE)
            front_matter = re.sub(r'\n\n+', '\n', front_matter)

            # Add new category
            cat_list = list(new_category)
            cat_str = str(cat_list).replace("'", '"')

            if 'date:' in front_matter:
                front_matter = re.sub(
                    r'(date: [^\n]+)(\n)?',
                    r'\1\ncategories: ' + cat_str + '\n',
                    front_matter
                )
            else:
                front_matter = front_matter.rstrip() + f'\ncategories: {cat_str}'

            new_content = f"---{front_matter}\n---{body}"

            with open(post_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

    # Verify results
    print("\n" + "=" * 90)
    print("VERIFICATION")
    print("=" * 90)

    category_counts = defaultdict(int)
    for filename, category in assignments.items():
        category_counts[category] += 1

    print(f"\n{'Main Category':<30} {'Subcategory':<40} {'Target':<10} {'Actual':<10} {'Match':<10}")
    print("-" * 90)

    all_match = True
    for category in sorted(CATEGORY_QUOTAS.keys()):
        target = CATEGORY_QUOTAS[category]
        actual = category_counts[category]
        match = "✅" if target == actual else f"❌ ({actual-target:+d})"

        if target != actual:
            all_match = False

        main_cat, sub_cat = category
        print(f"{main_cat:<30} {sub_cat:<40} {target:<10} {actual:<10} {match:<10}")

    print("\n" + "=" * 90)
    if all_match:
        print("✅ ALL CATEGORIES MATCH TARGET QUOTAS!")
    else:
        print("⚠️  Some categories don't match quotas")
    print("=" * 90 + "\n")

    return assignments


if __name__ == '__main__':
    assignments = main()
