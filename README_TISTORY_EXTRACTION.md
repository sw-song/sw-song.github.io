# Tistory Blog Category Extraction - Complete Reference

This directory contains comprehensive extraction and analysis of the Tistory blog category structure.

**Blog:** 관성을 이기는 데이터 (Overcoming Inertia with Data)
**Author:** swsong
**URL:** https://songseungwon.tistory.com
**Total Posts:** 112
**Extraction Date:** 2026-01-11

---

## Quick Reference

### Category Summary
- **4 Main Categories** (prefixed with numbers 1-4)
- **14 Subcategories** (two-level hierarchy)
- **112 Total Posts**

### Top 3 Most Active Categories
1. **머신러닝, 딥러닝** (ML/DL) - 24 posts
2. **서버, 데이터, 클라우드** (Backend/Cloud) - 20 posts
3. **금융 분석 프로그래밍 응용** (Finance Analysis Advanced) - 11 posts

### Category Distribution
- **기술 (Technology):** 66 posts (58.9%)
- **튜토리얼 (Tutorial):** 29 posts (25.9%)
- **도메인 (Domain):** 9 posts (8.0%)
- **실전 (Practical):** 8 posts (7.1%)

---

## Generated Files

### 1. **tistory_category_structure.json** (10 KB)
**Format:** JSON
**Contents:**
- Complete hierarchical structure with all categories and subcategories
- Post counts for each category
- Sample posts (8 posts) with category metadata
- Category mapping suggestions for GitHub migration
- Technical notes and observations

**Use Case:** Programmatic access to category structure, JSON imports, system integration

**Sample Structure:**
```json
{
  "blog_info": { ... },
  "category_structure": {
    "total_main_categories": 4,
    "total_subcategories": 14,
    "main_categories": [ ... ]
  },
  "sample_posts_with_categories": [ ... ],
  "category_mapping_for_migration": { ... }
}
```

---

### 2. **TISTORY_CATEGORY_MAPPING.md** (6.7 KB)
**Format:** Markdown
**Contents:**
- Detailed breakdown of all categories
- Category hierarchy with post counts
- Sample posts with category information
- Category format details (URLs, HTML, JavaScript)
- Post distribution analysis
- Suggested GitHub blog category mapping

**Use Case:** Human-readable reference, documentation, planning migration strategy

**Key Sections:**
- Category Hierarchy
- Sample Posts Table
- Category Format Details
- Post Distribution Analysis
- Suggested GitHub Blog Category Mapping

---

### 3. **TISTORY_CATEGORY_TREE.txt** (7.8 KB)
**Format:** Plain Text with ASCII tree structure
**Contents:**
- Visual tree representation of entire category hierarchy
- All category URLs (both main and subcategories)
- Sample posts organized by category
- Statistics and key insights

**Use Case:** Quick visual reference, easy copy-paste for documentation

**Visual Example:**
```
ROOT
├── 1. 기술 (Technology) [66 posts]
│   ├── 인프라, 네트워크 (Infrastructure, Network) [0]
│   ├── 서버, 데이터, 클라우드 (Server, Database, Cloud) [20]
│   ├── 웹, 자바스크립트 (Web, JavaScript) [15]
│   ├── 머신러닝, 딥러닝 (Machine Learning, Deep Learning) [24]
│   └── 통계, 시계열 (Statistics, Time Series) [7]
...
```

---

### 4. **TISTORY_EXTRACTION_SUMMARY.md** (9.5 KB)
**Format:** Markdown
**Contents:**
- Executive summary of extraction process
- Complete category structure overview
- Extraction methodology
- Key findings and insights
- Category naming patterns
- Data quality assessment
- Recommendations for GitHub blog migration
- Comparison of Tistory vs. potential GitHub structure
- Next steps and tools used

**Use Case:** Project planning, migration strategy, stakeholder communication

**Key Sections:**
- Executive Summary
- Category Structure Overview
- Extraction Methodology
- Key Findings
- Recommendations for GitHub Blog Migration
- Comparison: Tistory vs Potential GitHub Structure

---

### 5. **tistory_categories.csv** (3 KB)
**Format:** CSV (Comma-Separated Values)
**Contents:**
- Tabular format with all category information
- Main category ID, name, post count
- Subcategory name and post count
- Category URLs
- English translations

**Use Case:** Import into spreadsheets, database import, data analysis

**Columns:**
```
main_category_id
main_category_name
main_category_name_en
main_category_posts
subcategory_name
subcategory_name_en
subcategory_posts
category_url
```

**Example Rows:**
```
1,1. 기술,Technology,66,인프라 네트워크,Infrastructure Network,0,[URL]
1,1. 기술,Technology,66,서버 데이터 클라우드,Server Database Cloud,20,[URL]
...
```

---

### 6. **README_TISTORY_EXTRACTION.md** (This File)
**Format:** Markdown
**Contents:**
- Overview of all extracted files
- File descriptions and use cases
- Category summary
- Quick reference guide
- How to use each file
- Recommendations for next steps

---

## How to Use These Files

### For Quick Reference
1. Start with **TISTORY_CATEGORY_TREE.txt** for visual hierarchy
2. Check **TISTORY_CATEGORY_MAPPING.md** for detailed breakdowns

### For Documentation
1. Use **TISTORY_EXTRACTION_SUMMARY.md** for complete analysis
2. Reference **tistory_category_structure.json** for technical details

### For Data Integration
1. Use **tistory_categories.csv** to import into spreadsheets or databases
2. Use **tistory_category_structure.json** for programmatic access

### For Migration Planning
1. Review **TISTORY_EXTRACTION_SUMMARY.md** recommendations section
2. Use category mapping in **tistory_category_structure.json**
3. Plan new structure using suggestions in **TISTORY_CATEGORY_MAPPING.md**

---

## Category Structure Overview

```
1. 기술 (Technology)                    [66 posts]
   ├── 인프라, 네트워크                 [0]
   ├── 서버, 데이터, 클라우드           [20]
   ├── 웹, 자바스크립트                 [15]
   ├── 머신러닝, 딥러닝                 [24]
   └── 통계, 시계열                     [7]

2. 도메인 (Domain)                      [9 posts]
   ├── 금융                             [6]
   ├── 비즈니스                         [2]
   └── 자산운용                         [1]

3. 튜토리얼 (Tutorial)                  [29 posts]
   ├── 금융 분석 프로그래밍 기초        [6]
   ├── 금융 분석 프로그래밍 응용        [11]
   ├── 비즈니스 통계 분석 프로그래밍    [6]
   ├── 시계열 예측 및 계량 분석 방법론  [4]
   └── 자연어 처리 및 텍스트 분석 방법론 [2]

4. 실전 (Practical)                     [8 posts]
   ├── 글로벌 매크로 분석                [5]
   └── 계량 투자 분석                    [3]
```

---

## Sample Posts Analyzed

| Post ID | Category | Example Title |
|---------|----------|---------------|
| 157 | 2. 도메인/자산운용 | 국내/해외 ETF 매매시 일반 위탁 계좌 vs 절세 계좌... |
| 156 | 1. 기술/서버, 데이터, 클라우드 | [Dolt + Python + MySQL] 금융 분석을 위한... |
| 155 | 4. 실전/계량 투자 분석 | [파이썬 퀀트 투자] 벨류에이션 멀티플... |
| 152 | 2. 도메인/금융 | 2025년 장단기 국채금리 기반 마켓... |
| 151 | 4. 실전/글로벌 매크로 분석 | 달러 통화량과 유동성 비율을 활용한... |

---

## Key Insights

### Content Focus
- **Heavily Technical:** 58.9% of posts are technical in nature
- **Finance Integrated:** Strong fintech focus throughout
- **Tutorial-Rich:** 25.9% of posts are educational/tutorial content
- **Practical Applied:** Real-world use cases in Practical category

### Most Active Topics
1. Machine Learning/Deep Learning (21.4%)
2. Backend/Cloud/Database (17.9%)
3. Web/JavaScript (13.4%)
4. Finance Analysis (Programming) (17%)

### Gaps
- Infrastructure/Network: 0 posts (empty category)
- Business: 2 posts (minimal coverage)
- Asset Management: 1 post (minimal coverage)

---

## Technical Details

### URL Encoding
All Tistory URLs use URL-encoded Korean characters:
- Main categories: `/category/1.%20%EA%B8%B0%EC%88%A0`
- Subcategories: `/category/1.%20%EA%B8%B0%EC%88%A0/%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D%2C%20%EB%94%A5%EB%9F%AC%EB%8B%9D`

### Category Format in Posts
Posts display full category path as: `Main/Sub`
- Example: `1. 기술/머신러닝, 딥러닝`

### Post Metadata
Each post includes:
- `categoryId`: Numeric ID (e.g., 940449)
- `categoryLabel`: Full path (e.g., "1. 기술/서버, 데이터, 클라우드")

---

## Recommendations for Next Steps

### For Blog Migration
1. **Decide Structure:** Keep hierarchical (two-level) or flatten
2. **Choose Language:** Use Korean names or English translations
3. **Plan Migration:** Timeline and automation strategy
4. **Test Implementation:** Test with Jekyll/Hugo templates

### For Content Strategy
1. **Address Gaps:** Plan content for empty categories (Infrastructure)
2. **Consolidate Small:** Consider merging minimal categories
3. **Expand Strong:** Build on existing strong categories (ML/Finance)

### For SEO & Discovery
1. **Maintain Hierarchy:** Keep two-level structure for better organization
2. **Use Tags:** Add supplementary tagging system
3. **Create Indices:** Build category landing pages

---

## File Location

All files are located in: `/Users/seungwonsong/project/sw-song.github.io/`

**Generated Files:**
- `tistory_category_structure.json`
- `TISTORY_CATEGORY_MAPPING.md`
- `TISTORY_CATEGORY_TREE.txt`
- `TISTORY_EXTRACTION_SUMMARY.md`
- `tistory_categories.csv`
- `README_TISTORY_EXTRACTION.md` (this file)

---

## Extraction Methodology

### Data Sources
- Category page: `/category`
- Sample posts: IDs 150-157

### Tools Used
- Web fetching: curl
- Parsing: grep, basic HTML parsing
- Analysis: Python JSON creation
- Validation: Manual verification

### Validation Steps
- Verified post count totals (66+9+29+8 = 112)
- Checked category format consistency
- Confirmed URL encoding patterns
- Validated sample posts against categories

---

## Questions or Issues?

Refer to:
1. **Technical questions:** See `tistory_category_structure.json` for data structure
2. **Category details:** See `TISTORY_CATEGORY_MAPPING.md` for full breakdown
3. **Quick reference:** See `TISTORY_CATEGORY_TREE.txt` for visual structure
4. **Migration planning:** See `TISTORY_EXTRACTION_SUMMARY.md` recommendations
5. **Data import:** See `tistory_categories.csv` for spreadsheet import

---

## Version Info

- **Extraction Date:** 2026-01-11
- **Blog URL:** https://songseungwon.tistory.com
- **Total Posts Analyzed:** 112 (structure) + 8 (sample posts)
- **Categories Extracted:** 4 main + 14 subcategories
- **Files Generated:** 6 files in multiple formats

---

**Last Updated:** 2026-01-11
**Status:** Complete and Ready for Migration Planning
