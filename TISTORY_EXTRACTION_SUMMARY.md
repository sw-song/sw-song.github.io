# Tistory Blog Category Extraction Summary

**Date:** 2026-01-11
**Blog URL:** https://songseungwon.tistory.com
**Blog Title:** 관성을 이기는 데이터 (Overcoming Inertia with Data)
**Author:** swsong

---

## Executive Summary

Successfully extracted and analyzed the complete category structure from the Tistory blog. The blog contains **112 total posts** organized into **4 main categories** with **14 subcategories** using a two-level hierarchical structure.

---

## What Was Extracted

### 1. Complete Category Hierarchy
- All 4 main categories with Korean names
- All 14 subcategories with exact names and post counts
- URL paths for each category
- Verification of post count accuracy (66+9+29+8 = 112)

### 2. Sample Posts (8 posts analyzed)
- Post IDs: 157, 156, 155, 154, 153, 152, 151, 150
- Extracted exact category labels from each post
- Verified category consistency across the blog
- Captured full post titles and URLs

### 3. Metadata
- Category IDs (from JSON: `categoryId`)
- Category labels (from JSON: `categoryLabel`)
- Post dates
- Category distribution percentages

### 4. Technical Details
- URL encoding format for Korean characters
- Post metadata structure in Tistory
- Category system implementation

---

## Category Structure Overview

### Main Categories (4 total)

| ID | Name (Korean) | Name (English) | Posts | % |
|---|---|---|---|---|
| 1 | 1. 기술 | Technology | 66 | 58.9% |
| 2 | 2. 도메인 | Domain | 9 | 8.0% |
| 3 | 3. 튜토리얼 | Tutorial | 29 | 25.9% |
| 4 | 4. 실전 | Practical/Real-World | 8 | 7.1% |

### Subcategories by Main Category

**1. 기술 (66 posts)**
1. 인프라, 네트워크 (Infrastructure, Network) - 0 posts
2. 서버, 데이터, 클라우드 (Server, Data, Cloud) - 20 posts
3. 웹, 자바스크립트 (Web, JavaScript) - 15 posts
4. 머신러닝, 딥러닝 (ML, Deep Learning) - 24 posts
5. 통계, 시계열 (Statistics, Time Series) - 7 posts

**2. 도메인 (9 posts)**
1. 금융 (Finance) - 6 posts
2. 비즈니스 (Business) - 2 posts
3. 자산운용 (Asset Management) - 1 post

**3. 튜토리얼 (29 posts)**
1. 금융 분석 프로그래밍 기초 (Finance Analysis Programming Basics) - 6 posts
2. 금융 분석 프로그래밍 응용 (Finance Analysis Programming Applied) - 11 posts
3. 비즈니스 통계 분석 프로그래밍 (Business Statistics Programming) - 6 posts
4. 시계열 예측 및 계량 분석 방법론 (Time Series & Quantitative Analysis) - 4 posts
5. 자연어 처리 및 텍스트 분석 방법론 (NLP & Text Analysis) - 2 posts

**4. 실전 (8 posts)**
1. 글로벌 매크로 분석 (Global Macro Analysis) - 5 posts
2. 계량 투자 분석 (Quantitative Investment Analysis) - 3 posts

---

## Files Generated

### 1. `tistory_category_structure.json`
- Complete JSON structure with all categories
- Post counts and URLs
- Sample posts with metadata
- Category mapping for migration
- Location: `/Users/seungwonsong/project/sw-song.github.io/tistory_category_structure.json`

### 2. `TISTORY_CATEGORY_MAPPING.md`
- Detailed analysis of category structure
- Sample posts with categories
- Category format details (URLs, HTML, JavaScript)
- Post distribution analysis
- Suggested GitHub blog category mapping
- Location: `/Users/seungwonsong/project/sw-song.github.io/TISTORY_CATEGORY_MAPPING.md`

### 3. `TISTORY_CATEGORY_TREE.txt`
- Visual tree representation of category hierarchy
- All URLs (both main and subcategories)
- Sample posts by category
- Statistics and key insights
- Location: `/Users/seungwonsong/project/sw-song.github.io/TISTORY_CATEGORY_TREE.txt`

### 4. `TISTORY_EXTRACTION_SUMMARY.md`
- This file - summary of extraction process and results
- Location: `/Users/seungwonsong/project/sw-song.github.io/TISTORY_EXTRACTION_SUMMARY.md`

---

## Extraction Methodology

### 1. Category Page Analysis
- Fetched `/category` page from Tistory blog
- Parsed HTML to extract category navigation menu
- Extracted all category links and post counts

### 2. Sample Post Analysis
- Fetched individual posts (IDs 150-157)
- Extracted `categoryLabel` from JavaScript `window.T.entryInfo`
- Verified category consistency

### 3. Validation
- Verified post count totals: 66+9+29+8 = 112
- Checked category format consistency
- Confirmed URL encoding patterns

---

## Key Findings

### 1. Blog Content Distribution
- **Heavily Technical:** 58.9% of posts are technical content
- **Tutorial-Focused:** 25.9% of posts are tutorials
- **Finance Niche:** Strong fintech focus with finance analysis tutorials and practical applications
- **Sparse Areas:** Infrastructure/Network category empty, Business domain minimal

### 2. Most Active Areas
- Machine Learning/Deep Learning: 24 posts (21.4% of total)
- Finance Analysis Programming (Applied): 11 posts (9.8%)
- Backend/Cloud/Database: 20 posts (17.9%)
- Web/JavaScript: 15 posts (13.4%)

### 3. Content Progression
- Structured from basics (Tutorial category) to practical applications (Practical category)
- Clear separation between technical/domain knowledge and tutorials
- Real-world use cases in Practical category

### 4. Technical Implementation
- Two-level category hierarchy
- Numeric prefixes (1-4) for main categories
- Korean text throughout (requires URL encoding)
- Category IDs stored separately from labels
- Posts include full category path (Main/Sub format)

---

## Category Naming Patterns

### Main Categories
- Numbered format: `[1-4]. [Category Name]`
- Purpose-driven: Technology, Domain, Tutorial, Practical
- Ordered by logical flow

### Subcategories
- Descriptive names without numbers
- Multiple topics separated by commas (e.g., "서버, 데이터, 클라우드")
- Specific level of detail (e.g., "금융 분석 프로그래밍 기초" vs "금융 분석 프로그래밍 응용")

### URL Format
- Main: `/category/1.%20%EA%B8%B0%EC%88%A0` (URL-encoded Korean)
- Sub: `/category/1.%20%EA%B8%B0%EC%88%A0/%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D%2C%20%EB%94%A5%EB%9F%AC%EB%8B%9D`

---

## Data Quality Assessment

### Accuracy
- All category counts verified against main category totals
- Sample posts manually checked for category accuracy
- URL encoding validated

### Completeness
- All 4 main categories captured
- All 14 subcategories identified
- 8 sample posts with full metadata

### Limitations
- Only analyzed first 8 posts (recent posts)
- Did not fetch complete post history (would require pagination)
- URLs extracted but post content not analyzed

---

## Recommendations for GitHub Blog Migration

### 1. Simplified Category Structure
Consider flattening or reorganizing for GitHub Pages:
- Option A: Keep two-level structure but use English names
- Option B: Merge Tutorial into main categories
- Option C: Create tags system instead of categories

### 2. Category Naming
- Remove numeric prefixes (1-4)
- Use English names for better discoverability
- Separate multiple topics into individual categories

### 3. Migration Path
1. Map Tistory categories to GitHub categories (see JSON for mapping)
2. Create GitHub categories for all main and subcategories
3. Add category metadata to each post's frontmatter
4. Verify category distribution in new system

### 4. Considerations
- Maintain category hierarchy for SEO
- Plan for empty categories (Infrastructure/Network)
- Consider consolidating minimal categories (Business, Asset Management)

---

## Comparison: Tistory vs Potential GitHub Structure

### Tistory Structure
```
1. 기술 (66 posts)
   ├── 인프라, 네트워크 (0)
   ├── 서버, 데이터, 클라우드 (20)
   ├── 웹, 자바스크립트 (15)
   ├── 머신러닝, 딥러닝 (24)
   └── 통계, 시계열 (7)

2. 도메인 (9 posts)
   ├── 금융 (6)
   ├── 비즈니스 (2)
   └── 자산운용 (1)

3. 튜토리얼 (29 posts)
   ├── Finance Analysis Basics (6)
   ├── Finance Analysis Advanced (11)
   ├── Business Statistics (6)
   ├── Time Series Analysis (4)
   └── NLP & Text Analysis (2)

4. 실전 (8 posts)
   ├── 글로벌 매크로 분석 (5)
   └── 계량 투자 분석 (3)
```

### Potential GitHub Structure (Normalized)
```
Technology (66)
├── Backend/Cloud (20)
├── ML/AI (24)
├── Frontend/Web (15)
├── Statistics/TimeSeries (7)
└── Infrastructure (0)

Finance (6)
├── Analysis
└── Investment

Business (2)

Tutorials (29)
├── Finance Analysis Basics (6)
├── Finance Analysis Advanced (11)
├── Business Statistics (6)
├── Time Series Analysis (4)
└── NLP (2)

Analysis (8)
├── Macro Analysis (5)
└── Quantitative Investment (3)
```

---

## Next Steps

1. Review extracted data in the JSON and markdown files
2. Decide on migration strategy (keep structure vs. reorganize)
3. Plan post migration timeline
4. Consider tag system in addition to categories
5. Test category organization with Jekyll/Hugo templates

---

## Tools & Methods Used

- **Web Scraping:** curl for HTML fetching
- **Parsing:** Grep and basic HTML parsing
- **Analysis:** Python JSON creation and structure organization
- **Validation:** Manual verification of sample posts
- **Documentation:** Markdown and JSON for structured output

---

## Conclusion

The Tistory blog has a well-organized category structure focused on technical content with strong fintech integration. The extraction was successful and comprehensive, providing all necessary information for migration to GitHub Pages or other blogging platforms. The blog's content is suitable for migration with minimal reorganization needed.

For any questions or clarifications about specific categories, refer to the generated JSON file or visual tree representation.
