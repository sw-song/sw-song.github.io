#!/usr/bin/env python3
"""
Apply accurate categories to GitHub blog posts matching Tistory structure.

Strategy:
1. Use Tistory post counts as ground truth
2. Analyze post titles and content to assign correct categories
3. Use episode numbers and specific title patterns to identify tutorials
4. Apply proper keyword matching for accurate categorization
"""

from pathlib import Path
import re
from tqdm import tqdm
import yaml

# Tistory ground truth: actual post counts by category
TISTORY_STRUCTURE = {
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

def infer_accurate_category(title, filename):
    """Infer accurate category from title and filename using improved heuristics"""
    title_lower = title.lower()
    filename_lower = filename.lower()

    # TUTORIAL CATEGORIES - Check first before generic keywords
    # These have specific patterns and should be detected first

    # 금융 분석 프로그래밍 기초 (Finance Programming Basics)
    # Episodes 01, 02, 03, and supplementary materials
    if "금융 분석을 위한 파이썬" in title:
        if "보충자료" in title or any(x in title for x in [" 01.", " 02.", " 03."]):
            return ["3. 튜토리얼", "금융 분석 프로그래밍 기초"]
        # 금융 분석 프로그래밍 응용 (Finance Programming Applied)
        # Episodes 04, 05+
        elif any(x in title for x in [" 04.", " 05.", " 06."]):
            return ["3. 튜토리얼", "금융 분석 프로그래밍 응용"]
        else:
            # If it has the series name but no episode, it's basics by default
            return ["3. 튜토리얼", "금융 분석 프로그래밍 기초"]

    # 비즈니스 통계 분석 프로그래밍
    if ("비즈니스" in title or "커머스" in title or "고객" in title or "customer" in title_lower) and ("분석" in title or "세분화" in title or "프로그래밍" in title):
        return ["3. 튜토리얼", "비즈니스 통계 분석 프로그래밍"]

    # 자연어 처리 및 텍스트 분석 방법론
    if any(x in title_lower for x in ["자연어", "nlp", "tf-idf", "lsa", "감성", "뉴스", "기사", "similarity"]):
        return ["3. 튜토리얼", "자연어 처리 및 텍스트 분석 방법론"]

    # 시계열 예측 및 계량 분석 방법론
    # This is for methodology posts, not just any time series
    if any(x in title_lower for x in ["arima", "var ", "벡터자기회귀", "시계열 예측", "계량 분석 방법론", "시계열 패턴"]):
        return ["3. 튜토리얼", "시계열 예측 및 계량 분석 방법론"]

    # TECHNICAL CATEGORIES - General technology posts

    # 웹, 자바스크립트
    if any(x in title_lower for x in ["javascript", "html", "css", "nodejs", "npm", "web", "django", "flask", "web framework"]):
        return ["1. 기술", "웹, 자바스크립트"]

    # 서버, 데이터, 클라우드
    if any(x in title_lower for x in ["docker", "kubernetes", "elastic", "kibana", "gcp", "cloud", "firestore", "database", "mysql", "git", "linux", "tmux", "dolt", "backend"]):
        return ["1. 기술", "서버, 데이터, 클라우드"]

    # 머신러닝, 딥러닝 - SPECIFIC ML/DL posts only
    if any(x in title_lower for x in ["gan", "stargan", "stylegan", "cnn", "rnn", "neural", "deep learning", "machine learning"]):
        return ["1. 기술", "머신러닝, 딥러닝"]

    # 통계, 시계열 - General statistics posts (not tutorials, not time series analysis)
    if (any(x in title_lower for x in ["통계", "hypothesis", "kolmogorov", "correlation matrix", "confusion_matrix"])
        and "방법론" not in title and "arima" not in title_lower and "var " not in title_lower):
        return ["1. 기술", "통계, 시계열"]

    # PRACTICAL/REAL-WORLD CATEGORIES - Check before domain categories
    # 계량 투자 분석 (Quantitative Investment Analysis)
    if any(x in title_lower for x in ["퀀트", "[파이썬 퀀트", "백테", "멀티플", "피어 그룹", "스크리닝", "존버"]):
        return ["4. 실전", "계량 투자 분석"]

    # 글로벌 매크로 분석 (Global Macro Analysis)
    if any(x in title_lower for x in ["글로벌", "매크로", "달러", "유동성", "부채사이클", "리세션", "경기 침체", "부채"]):
        return ["4. 실전", "글로벌 매크로 분석"]

    # DOMAIN CATEGORIES

    # 자산운용 (Asset Management) - investment portfolios, ETF, asset allocation
    if any(x in title_lower for x in ["자산운용", "etf", "포트폴리오", "계좌", "절세"]):
        return ["2. 도메인", "자산운용"]

    # 금융 (Finance) - stock market, crypto, valuation, general finance
    if any(x in title_lower for x in ["주식", "bitcoin", "crypto", "가격", "valuation", "국채", "금리", "배수모형", "배당성장"]):
        return ["2. 도메인", "금융"]

    # 비즈니스 (Business) - business strategy, commerce, general business topics
    # But not if already matched as tutorial
    if ("비즈니스" in title or "커머스" in title or "넷플릭스" in title or "콘텐츠" in title) and "프로그래밍" not in title and "분석" not in title:
        return ["2. 도메인", "비즈니스"]

    # DEFAULT - Use statistics category as default (more neutral than ML/DL)
    # But prefer ML/DL only if there's strong evidence
    if "파이썬" in title or "python" in title_lower:
        # If it mentions Python but doesn't fit elsewhere, it's likely infrastructure/basics
        return ["1. 기술", "서버, 데이터, 클라우드"]

    return ["1. 기술", "머신러닝, 딥러닝"]


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
    results = []
    category_counts = {}

    print("\n" + "=" * 80)
    print("APPLYING ACCURATE CATEGORIES TO GITHUB BLOG POSTS")
    print("=" * 80 + "\n")

    post_files = sorted(posts_dir.glob('*.md'))

    for post_file in tqdm(post_files, desc="Processing", unit="post"):
        # Extract title from filename and front matter
        filename = post_file.stem

        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        title = filename
        if content.startswith('---'):
            parts = content.split('---', 2)
            try:
                front_matter = yaml.safe_load(parts[1])
                title = front_matter.get('title', filename)
            except:
                pass

        # Infer accurate category
        categories = infer_accurate_category(title, filename)

        # Update post
        success, result = update_post_with_category(post_file, categories)

        # Count categories
        cat_key = str(categories)
        category_counts[cat_key] = category_counts.get(cat_key, 0) + 1

        results.append({
            'file': post_file.name,
            'title': title[:60],
            'categories': categories if success else "ERROR",
            'success': success
        })

    # Print summary
    print("\n" + "=" * 80)
    print("CATEGORIZATION RESULTS")
    print("=" * 80 + "\n")

    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    print(f"✅ Successfully categorized: {len(successful)}")
    print(f"❌ Failed: {len(failed)}\n")

    print("Category Distribution:")
    print("-" * 80)
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count} posts")

    if failed:
        print("\n" + "-" * 80)
        print("Failed posts:")
        for r in failed:
            print(f"  {r['file']}: {r['categories']}")

    # Verify against Tistory structure
    print("\n" + "=" * 80)
    print("VERIFICATION AGAINST TISTORY STRUCTURE")
    print("=" * 80 + "\n")

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
    print("-" * 80)

    all_match = True
    for main_name in sorted(TISTORY_STRUCTURE.keys()):
        tist_subs = TISTORY_STRUCTURE[main_name]
        curr_subs = current_structure.get(main_name, {})

        for sub_name in sorted(tist_subs.keys()):
            tist_count = tist_subs[sub_name]
            curr_count = curr_subs.get(sub_name, 0)
            match = "✅" if tist_count == curr_count else "❌"

            if tist_count != curr_count:
                all_match = False

            print(f"{main_name:<30} {sub_name:<40} {tist_count:<10} {curr_count:<10} {match:<10}")

    print("\n" + "=" * 80)
    print(f"Total processed: {len(results)}")
    print("=" * 80 + "\n")

    if all_match:
        print("✅ ALL CATEGORIES NOW MATCH TISTORY STRUCTURE!")
    else:
        print("⚠️  Some categories still don't match. Review mismatches above.")

    return results


if __name__ == '__main__':
    results = main()
