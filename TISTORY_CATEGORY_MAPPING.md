# Tistory Category Structure Analysis

**Blog:** 관성을 이기는 데이터
**Author:** swsong
**Total Posts:** 112
**Extraction Date:** 2026-01-11
**URL:** https://songseungwon.tistory.com

---

## Overview

The Tistory blog uses a **two-level hierarchical category system** with 4 main categories and 14 subcategories total. All category names are in Korean, and main categories are prefixed with numbers (1-4) for ordering.

---

## Category Hierarchy

### 1. 기술 (Technology/Technical) - 66 posts

The largest category covering all technical topics:

- **인프라, 네트워크** (Infrastructure, Network) - 0 posts
- **서버, 데이터, 클라우드** (Server, Database, Cloud) - 20 posts
- **웹, 자바스크립트** (Web, JavaScript) - 15 posts
- **머신러닝, 딥러닝** (Machine Learning, Deep Learning) - 24 posts
- **통계, 시계열** (Statistics, Time Series) - 7 posts

### 2. 도메인 (Domain) - 9 posts

Domain knowledge and business topics:

- **금융** (Finance) - 6 posts
- **비즈니스** (Business) - 2 posts
- **자산운용** (Asset Management) - 1 post

### 3. 튜토리얼 (Tutorial) - 29 posts

Educational and tutorial content:

- **금융 분석 프로그래밍 기초** (Finance Analysis Programming Basics) - 6 posts
- **금융 분석 프로그래밍 응용** (Finance Analysis Programming Applied) - 11 posts
- **비즈니스 통계 분석 프로그래밍** (Business Statistics Analysis Programming) - 6 posts
- **시계열 예측 및 계량 분석 방법론** (Time Series Forecasting & Quantitative Analysis Methodology) - 4 posts
- **자연어 처리 및 텍스트 분석 방법론** (NLP & Text Analysis Methodology) - 2 posts

### 4. 실전 (Practical/Real-World) - 8 posts

Real-world applications and case studies:

- **글로벌 매크로 분석** (Global Macro Analysis) - 5 posts
- **계량 투자 분석** (Quantitative Investment Analysis) - 3 posts

---

## Sample Posts with Category Information

| Post ID | Title | Category | Category Clean |
|---------|-------|----------|-----------------|
| 157 | 국내/해외 ETF 매매시 일반 위탁 계좌 vs 절세 계좌(연금저축, IRP, ISA) 세금 차이 정리 | 2. 도메인/자산운용 | 도메인 > 자산운용 |
| 156 | [Dolt + Python + MySQL] 금융 분석을 위한 재무제표 데이터베이스 구축과 실행 | 1. 기술/서버, 데이터, 클라우드 | 기술 > 서버, 데이터, 클라우드 |
| 155 | [파이썬 퀀트 투자] 벨류에이션 멀티플 기반 피어 그룹 스크리닝 | 4. 실전/계량 투자 분석 | 실전 > 계량 투자 분석 |
| 154 | [파이썬 퀀트 투자] 좋은 기업을 찾아보자 - 미국 기술주 멀티플 EDA | 4. 실전/계량 투자 분석 | 실전 > 계량 투자 분석 |
| 153 | [파이썬 퀀트 투자] 시장은 정말 효율적일까? - 통계적 차익거래(Statistical Arbitrage) 백테스팅 시뮬레이션 | 4. 실전/계량 투자 분석 | 실전 > 계량 투자 분석 |
| 152 | 2025년 장단기 국채금리 기반 마켓 베타 국면 분석 - 단기 금리 급락시 기저 원인을 포착할 것 | 2. 도메인/금융 | 도메인 > 금융 |
| 151 | 달러 통화량과 유동성 비율을 활용한 금, 비트코인 가치평가 | 4. 실전/글로벌 매크로 분석 | 실전 > 글로벌 매크로 분석 |
| 150 | [파이썬 금융 데이터 분석] 미국 부채사이클 기반 2025년 리세션 리스크 평가 | 4. 실전/글로벌 매크로 분석 | 실전 > 글로벌 매크로 분석 |

---

## Category Format Details

### In URLs
Categories are URL-encoded in the format: `/category/[Main]/[Sub]`

Example:
```
/category/1.%20%EA%B8%B0%EC%88%A0/%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D%2C%20%EB%94%A5%EB%9F%AC%EB%8B%9D
```
Decoded: `/category/1. 기술/머신러닝, 딥러닝`

### In HTML/Posts
Posts display category as `Main/Sub` format:
```
2. 도메인/자산운용
1. 기술/서버, 데이터, 클라우드
```

### In JavaScript
Posts include `categoryLabel` in JSON:
```javascript
window.T.entryInfo = {
  "entryId": 157,
  "categoryId": 1216643,
  "categoryLabel": "2. 도메인/자산운용"
}
```

---

## Post Distribution Analysis

### By Main Category (Percentage)
- **1. 기술:** 58.9% (66/112)
- **3. 튜토리얼:** 25.9% (29/112)
- **2. 도메인:** 8.0% (9/112)
- **4. 실전:** 7.1% (8/112)

### Most Active Subcategories
1. **머신러닝, 딥러닝:** 24 posts
2. **금융 분석 프로그래밍 응용:** 11 posts
3. **서버, 데이터, 클라우드:** 20 posts
4. **글로벌 매크로 분석:** 5 posts

### Empty Subcategories
- **인프라, 네트워크:** 0 posts

---

## Suggested GitHub Blog Category Mapping

For migration to GitHub Pages/blog, suggested normalized categories:

### Technical (1. 기술)
- `Infrastructure` ← 인프라, 네트워크
- `Backend` ← 서버, 데이터, 클라우드
- `Frontend` ← 웹, 자바스크립트
- `ML` / `Deep Learning` / `AI` ← 머신러닝, 딥러닝
- `Statistics` / `Time Series` / `Data Analysis` ← 통계, 시계열

### Domain (2. 도메인)
- `Finance` / `Finance Analysis` ← 금융
- `Business` / `Business Analysis` ← 비즈니스
- `Asset Management` / `Investment` ← 자산운용

### Tutorial (3. 튜토리얼)
- `Tutorial-FinanceAnalysisProgramming-Basics` ← 금융 분석 프로그래밍 기초
- `Tutorial-FinanceAnalysisProgramming-Advanced` ← 금융 분석 프로그래밍 응용
- `Tutorial-BusinessStatistics` ← 비즈니스 통계 분석 프로그래밍
- `Tutorial-TimeSeriesAnalysis` ← 시계열 예측 및 계량 분석 방법론
- `Tutorial-NLP` / `Tutorial-TextAnalysis` ← 자연어 처리 및 텍스트 분석 방법론

### Practical (4. 실전)
- `Macro Analysis` / `Global Markets` ← 글로벌 매크로 분석
- `Quantitative Investment` / `Trading` ← 계량 투자 분석

---

## Key Observations

1. **Technical Focus:** The blog is heavily focused on technical content (58.9% of posts), with ML/DL being the most active subcategory.

2. **Finance Integration:** A significant portion of tutorials and practical articles combine programming with financial analysis, indicating a strong fintech focus.

3. **Two-Level Hierarchy:** Simple and clear two-level structure makes navigation straightforward.

4. **Numerical Prefixes:** Main categories use numbers (1-4) which helps with ordering and visual hierarchy.

5. **Post Distribution:** Posts are fairly concentrated in specific subcategories (ML, tutorials), with some subcategories having minimal content.

6. **URL Encoding:** All category names are URL-encoded due to Korean character support.

---

## Files Generated

- `tistory_category_structure.json` - Comprehensive JSON structure with all categories, post counts, and mappings
- `TISTORY_CATEGORY_MAPPING.md` - This markdown file with detailed category analysis
