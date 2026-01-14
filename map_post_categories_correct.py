#!/usr/bin/env python3
"""
Correctly map posts to Tistory 2-level hierarchical categories.

Tistory has 4 main categories with 2-level subcategories:
1. 기술 (Technology)
   - 서버, 데이터, 클라우드
   - 머신러닝, 딥러닝
   - 웹, 자바스크립트
   - 통계, 시계열
   - 인프라, 네트워크

2. 도메인 (Domain)
   - 금융
   - 자산운용
   - 비즈니스

3. 튜토리얼 (Tutorial)
   - 금융 분석 프로그래밍 기초
   - 금융 분석 프로그래밍 응용
   - 비즈니스 통계 분석 프로그래밍
   - 시계열 예측 및 계량 분석 방법론
   - 자연어 처리 및 텍스트 분석 방법론

4. 실전 (Practice)
   - 계량 투자 분석
   - 글로벌 매크로 분석
"""

from pathlib import Path
import re
from tqdm import tqdm

# 2-level 카테고리 매핑
CATEGORY_MAPPING = {
    # 1. 기술 (Technology)
    "web": ["웹, 자바스크립트"],  # JavaScript, HTML, CSS, Node.js, npm
    "ml": ["머신러닝, 딥러닝"],  # Machine Learning, Deep Learning, GAN, etc.
    "server": ["서버, 데이터, 클라우드"],  # Docker, Kubernetes, Elastic, etc.
    "stats": ["통계, 시계열"],  # Statistics, Time Series
    "infra": ["인프라, 네트워크"],  # Infrastructure, Network

    # 2. 도메인 (Domain)
    "finance_domain": ["2. 도메인", "금융"],  # Finance domain posts
    "asset": ["2. 도메인", "자산운용"],  # Asset management
    "business_domain": ["2. 도메인", "비즈니스"],  # Business domain

    # 3. 튜토리얼 (Tutorial)
    "finance_basic": ["3. 튜토리얼", "금융 분석 프로그래밍 기초"],
    "finance_advanced": ["3. 튜토리얼", "금융 분석 프로그래밍 응용"],
    "business_stats": ["3. 튜토리얼", "비즈니스 통계 분석 프로그래밍"],
    "time_series_tutorial": ["3. 튜토리얼", "시계열 예측 및 계량 분석 방법론"],
    "nlp_tutorial": ["3. 튜토리얼", "자연어 처리 및 텍스트 분석 방법론"],

    # 4. 실전 (Practice)
    "quant_practice": ["4. 실전", "계량 투자 분석"],
    "macro_practice": ["4. 실전", "글로벌 매크로 분석"],
}

def infer_category_from_title(title):
    """포스트 제목에서 정확한 2-level 카테고리 추론"""
    title_lower = title.lower()

    # 웹/자바스크립트 관련
    if any(x in title_lower for x in ['javascript', 'html', 'css', 'nodejs', 'npm', 'web']):
        return ["1. 기술", "웹, 자바스크립트"]

    # 머신러닝/딥러닝 관련
    if any(x in title_lower for x in ['machine', 'deep', 'learning', 'neural', 'gan', 'lgbm', 'xgboost', 'cnn', 'rnn', 'stargan']):
        return ["1. 기술", "머신러닝, 딥러닝"]

    # 서버/데이터/클라우드 관련
    if any(x in title_lower for x in ['docker', 'kubernetes', 'elastic', 'kibana', 'gcp', 'cloud', 'firestore', 'database', 'git', 'linux', 'tmux']):
        return ["1. 기술", "서버, 데이터, 클라우드"]

    # 금융 분석 프로그래밍 - 기초
    if '금융 분석을 위한 파이썬 프로그래밍' in title and ('01' in title or '02' in title or '03' in title):
        return ["3. 튜토리얼", "금융 분석 프로그래밍 기초"]

    # 금융 분석 프로그래밍 - 응용
    if '금융 분석을 위한 파이썬 프로그래밍' in title and ('04' in title or '05' in title):
        return ["3. 튜토리얼", "금융 분석 프로그래밍 응용"]

    # 금융 분석 프로그래밍 - 보충자료
    if '금융 분석을 위한 파이썬 프로그래밍' in title and '보충자료' in title:
        return ["3. 튜토리얼", "금융 분석 프로그래밍 기초"]

    # 비즈니스 통계 분석 프로그래밍
    if any(x in title_lower for x in ['비즈니스', 'business', 'customer', '고객', '커머스', 'commerce']) and '통계' in title:
        return ["3. 튜토리얼", "비즈니스 통계 분석 프로그래밍"]

    # 시계열/통계 관련 튜토리얼
    if any(x in title_lower for x in ['시계열', 'time series', 'var', 'arima', '벡터자기회귀']):
        return ["3. 튜토리얼", "시계열 예측 및 계량 분석 방법론"]

    # 자연어 처리 관련 튜토리얼
    if any(x in title_lower for x in ['자연어', 'nlp', 'text', 'sentiment', '감성']):
        return ["3. 튜토리얼", "자연어 처리 및 텍스트 분석 방법론"]

    # 금융 도메인 - 주식/투자 분석
    if any(x in title_lower for x in ['주식', 'stock', 'etf', 'bitcoin', 'crypto', '가격', 'price', 'valuation']):
        return ["2. 도메인", "금융"]

    # 금융 도메인 - 매크로/경제
    if any(x in title_lower for x in ['매크로', 'macro', '경제', 'economic', 'gdp', 'inflation', 'interest', 'rate']):
        return ["2. 도메인", "금융"]

    # 금융 도메인 - 자산운용
    if any(x in title_lower for x in ['자산운용', 'asset', 'portfolio', '포트폴리오']):
        return ["2. 도메인", "자산운용"]

    # 비즈니스 도메인
    if any(x in title_lower for x in ['비즈니스', 'business', '상권', 'commerce']):
        return ["2. 도메인", "비즈니스"]

    # 정량 투자 분석 - 실전
    if any(x in title_lower for x in ['정량', 'quantitative', 'backtest', '백테', 'algorithm']):
        return ["4. 실전", "계량 투자 분석"]

    # 글로벌 매크로 분석 - 실전
    if any(x in title_lower for x in ['글로벌', 'global', 'macro', 'macro', '달러', 'dollar', 'fred']):
        return ["4. 실전", "글로벌 매크로 분석"]

    # 통계/시계열 - 기술
    if any(x in title_lower for x in ['통계', 'statistics', 'correlation', 'hypothesis']):
        return ["1. 기술", "통계, 시계열"]

    # 기본값
    return ["1. 기술", "머신러닝, 딥러닝"]  # 기본값


def update_post_with_category(post_file, categories):
    """포스트의 YAML에 카테고리 추가"""
    try:
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # YAML 파싱
        if not content.startswith('---'):
            return False, "No YAML front matter"

        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "Malformed YAML"

        front_matter = parts[1]
        body = parts[2]

        # 기존 카테고리 제거
        front_matter = re.sub(r'^categories:.*$', '', front_matter, flags=re.MULTILINE)
        # 잉여 줄바꿈 정리하되 날짜 뒤의 줄바꿈은 보존
        front_matter = re.sub(r'\n\n+', '\n', front_matter)

        # 새 카테고리 추가
        cat_str = str(categories).replace("'", '"')
        if 'date:' in front_matter:
            # date 라인 뒤에 카테고리 추가
            front_matter = re.sub(
                r'(date: [^\n]+)(\n)?',
                r'\1\ncategories: ' + cat_str + '\n',
                front_matter
            )
        else:
            front_matter = front_matter.rstrip() + f'\ncategories: {cat_str}'

        # 저장
        new_content = f"---{front_matter}\n---{body}"
        with open(post_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True, categories

    except Exception as e:
        return False, str(e)


def main():
    """메인 함수"""
    posts_dir = Path('_posts')
    results = []

    print("\n" + "=" * 70)
    print("CORRECT MAPPING OF POSTS TO TISTORY 2-LEVEL CATEGORIES")
    print("=" * 70 + "\n")

    post_files = sorted(posts_dir.glob('*.md'))

    for post_file in tqdm(post_files, desc="Processing", unit="post"):
        # 포스트 제목 추론
        filename = post_file.stem
        categories = infer_category_from_title(filename)

        # 카테고리 업데이트
        success, result = update_post_with_category(post_file, categories)

        results.append({
            'file': post_file.name,
            'categories': categories if success else "ERROR",
            'success': success
        })

    # 요약
    print("\n" + "=" * 70)
    print("CATEGORIZATION RESULTS")
    print("=" * 70 + "\n")

    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    print(f"✅ Successfully categorized: {len(successful)}")
    print(f"❌ Failed: {len(failed)}\n")

    # 카테고리별 분류
    categories_count = {}
    for r in successful:
        cat_str = str(r['categories'])
        categories_count[cat_str] = categories_count.get(cat_str, 0) + 1

    print("Category Distribution:")
    print("─" * 70)
    for cat, count in sorted(categories_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count} posts")

    if failed:
        print("\n" + "─" * 70)
        print("Failed posts:")
        for r in failed:
            print(f"  {r['file']}: {r['categories']}")

    print("\n" + "=" * 70)
    print(f"Total processed: {len(results)}")
    print("=" * 70 + "\n")

    return results


if __name__ == '__main__':
    results = main()
