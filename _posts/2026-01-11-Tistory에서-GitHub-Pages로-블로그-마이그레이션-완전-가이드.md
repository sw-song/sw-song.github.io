---
layout: post
title: Tistory에서 GitHub Pages로 블로그 마이그레이션 완전 가이드
date: 2026-01-11
categories: ["Technology"]
---

# Tistory에서 GitHub Pages로 블로그 마이그레이션 완전 가이드

블로그를 Tistory에서 GitHub Pages(Jekyll)로 마이그레이션하는 과정은 생각보다 복잡합니다. 이 글에서는 112개의 포스트, 788개의 이미지를 성공적으로 마이그레이션한 전체 과정과 발생했던 에러들, 그리고 해결 방법을 공유하고자 합니다.

## 왜 GitHub Pages로 이전했나?

Tistory는 사용하기 쉽지만, 다음과 같은 한계가 있습니다:
- **플랫폼 의존성**: Tistory 서비스 종료 시 데이터 손실 위험
- **완전한 커스터마이징 불가**: 제한된 HTML/CSS 수정만 가능
- **버전 관리 불가**: 포스트 변경 이력 관리 어려움
- **데이터 포팅 어려움**: 다른 플랫폼으로 이전 시 복잡한 과정

GitHub Pages는 이러한 문제를 해결합니다:
- **완전한 소유권**: 모든 데이터를 git 저장소로 관리
- **버전 제어**: git을 통한 완전한 변경 이력 관리
- **무제한 커스터마이징**: 전체 코드 제어 가능
- **무료 호스팅**: 백업 및 배포 자동화
- **마크다운 기반**: 포맷 독립적인 콘텐츠 관리

---

## 전체 마이그레이션 프로세스

### 1단계: 포스트 추출 및 마이그레이션

#### 1.1 Tistory 스크래핑

먼저 Tistory 블로그에서 모든 포스트를 추출해야 합니다.

```python
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time

BASE_URL = "https://songseungwon.tistory.com"
PAGES = 12  # 페이지 수

def scrape_tistory_posts():
    """Tistory에서 모든 포스트 URL 추출"""
    posts = []
    for page in range(1, PAGES + 1):
        url = f"{BASE_URL}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 포스트 링크 추출
        for link in soup.find_all('a', {'class': 'post-link'}):
            post_url = link.get('href')
            if post_url:
                posts.append(post_url)

        time.sleep(0.5)  # 서버 부하 분산

    return posts
```

#### 1.2 포스트 내용 추출

```python
def extract_post_content(url):
    """개별 포스트에서 제목, 날짜, 내용 추출"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 제목 추출
    title = soup.find('h1', {'class': 'title-article'})
    title_text = title.get_text(strip=True) if title else "Untitled"

    # 날짜 추출 (형식: 2025. 6. 10. 18:54)
    date_elem = soup.find('span', {'class': 'date'})
    date_text = date_elem.get_text(strip=True) if date_elem else ""
    date_formatted = convert_date_format(date_text)  # 2025-06-10

    # 본문 추출
    article = soup.find('div', {'class': 'article-view'})

    return {
        'title': title_text,
        'date': date_formatted,
        'content': article,
        'url': url
    }

def convert_date_format(date_str):
    """Tistory 날짜 형식을 Jekyll 형식으로 변환
    2025. 6. 10. 18:54 -> 2025-06-10
    """
    parts = date_str.split('.')
    year = parts[0].strip()
    month = parts[1].strip().zfill(2)
    day = parts[2].strip().zfill(2)
    return f"{year}-{month}-{day}"
```

---

### 2단계: 이미지 추출 및 최적화

#### 2.1 이미지 다운로드

```python
def download_images(article, post_id):
    """포스트에서 모든 이미지를 다운로드하고 URL 업데이트"""
    images_dir = Path("assets/images/posts")
    images_dir.mkdir(parents=True, exist_ok=True)

    img_counter = 0
    for img in article.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if not src:
            continue

        try:
            # 이미지 URL 정규화
            img_url = resolve_image_url(src, BASE_URL)
            response = requests.get(img_url, timeout=5)
            response.raise_for_status()

            # 파일 형식 감지
            ext = get_image_extension(img_url, response)
            img_name = f"{post_id}-{img_counter}{ext}"
            img_dest = images_dir / img_name

            # 이미지 저장
            with open(img_dest, 'wb') as f:
                f.write(response.content)

            # 로컬 경로로 업데이트 (중요!)
            img['src'] = f"/assets/images/posts/{img_name}"
            img_counter += 1

        except Exception as e:
            print(f"이미지 다운로드 실패: {img_url} - {e}")
            img.decompose()  # 실패한 이미지 제거

def resolve_image_url(src, base_url):
    """상대경로, CDN URL, 프로토콜 없는 URL 등 처리"""
    if src.startswith('http'):
        return src
    elif src.startswith('//'):
        return 'https:' + src
    elif src.startswith('/'):
        return base_url + src
    else:
        return base_url + '/' + src

def get_image_extension(url, response):
    """Content-Type으로부터 파일 확장자 감지"""
    content_type = response.headers.get('content-type', '').lower()

    type_to_ext = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/webp': '.webp'
    }

    for mime_type, ext in type_to_ext.items():
        if mime_type in content_type:
            return ext

    # URL에서 확장자 추출
    path = url.split('?')[0]
    return Path(path).suffix or '.jpg'
```

#### 2.2 WebP 압축 (75% 크기 감소)

원본 이미지: 167.51 MB → 압축 후: 41.08 MB (126.43 MB 절약)

```python
from PIL import Image

def compress_to_webp(image_path, quality=85):
    """이미지를 WebP 형식으로 압축"""
    try:
        img = Image.open(image_path)

        # RGBA를 RGB로 변환 (압축률 향상)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')

        # WebP로 저장
        webp_path = image_path.with_suffix('.webp')
        img.save(
            webp_path,
            'WEBP',
            quality=quality,
            method=6  # 최대 압축
        )

        # 원본 이미지 삭제
        image_path.unlink()

        return webp_path

    except Exception as e:
        print(f"WebP 압축 실패: {image_path} - {e}")
        return None
```

#### 2.3 마크다운으로 변환

HTML을 마크다운으로 변환하면서 이미지 링크 보존이 중요합니다.

```python
from markdownify import markdownify

def convert_to_markdown(article):
    """HTML을 마크다운으로 변환
    이미지 링크 보존이 핵심!
    """
    # 먼저 이미지를 다운로드하고 src를 업데이트
    download_images(article, post_id)

    # 그 후에 마크다운으로 변환
    markdown_content = markdownify(
        str(article),
        heading_style="underlined"
    )

    # 과도한 줄바꿈 정리
    markdown_content = re.sub(r'\n\s*\n\s*\n', '\n\n', markdown_content).strip()

    return markdown_content
```

---

### 3단계: Jekyll 포스트 생성

#### 3.1 YAML Front Matter 작성

```python
def create_jekyll_post(title, date, content, categories, post_id):
    """Jekyll 형식의 포스트 파일 생성"""

    # 파일명 생성 (YYYY-MM-DD-title.md)
    safe_title = re.sub(r'[^\w\s-]', '', title)
    safe_title = re.sub(r'[-\s]+', '-', safe_title)
    filename = f"_posts/{date}-{safe_title}.md"

    # YAML Front Matter
    front_matter = f"""---
layout: post
title: {title}
date: {date}
categories: {categories}
---

"""

    # 포스트 저장
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(front_matter + content)

    return filename
```

---

### 4단계: 카테고리 추출 및 매핑

#### 4.1 Tistory에서 카테고리 추출

```python
def extract_tistory_categories():
    """Tistory의 모든 카테고리 추출"""
    url = "https://songseungwon.tistory.com/category"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    categories = {}
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if '/category/' in href:
            text = link.get_text(strip=True)
            if text:
                categories[text] = href

    return categories
```

#### 4.2 포스트에 카테고리 매핑

```python
def infer_category_from_title(title):
    """포스트 제목에서 카테고리 추론"""
    title_lower = title.lower()

    # 키워드 기반 카테고리 분류
    category_keywords = {
        "Web/JavaScript": ['javascript', 'html', 'css', 'nodejs', 'npm'],
        "ML/DL": ['machine', 'deep', 'learning', 'neural', 'gan', 'xgboost'],
        "Finance": ['주식', 'stock', 'etf', 'bitcoin', 'crypto', '금융', 'finance'],
        "Server/Data/Cloud": ['docker', 'kubernetes', 'elastic', 'gcp', 'cloud'],
        "Quantitative Investment": ['정량', 'quantitative', '매크로', 'macro'],
    }

    for category, keywords in category_keywords.items():
        if any(kw in title_lower for kw in keywords):
            return category

    return "Technology"  # 기본값

def add_category_to_post(post_file, category):
    """포스트의 YAML에 카테고리 추가"""
    with open(post_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # YAML 파싱
    parts = content.split('---', 2)
    front_matter = parts[1]
    body = parts[2]

    # 카테고리 추가
    front_matter = re.sub(
        r'(date: [^\n]+\n)',
        r'\1categories: ["' + category + '"]\n',
        front_matter
    )

    # 저장
    with open(post_file, 'w', encoding='utf-8') as f:
        f.write(f"---{front_matter}---{body}")
```

---

### 5단계: 에러 처리 및 검증

#### 5.1 발생한 주요 에러들

**에러 1: 제어 문자 (Control Characters)**

```
Error: YAML Exception reading post file:
control characters are not allowed at line 1 column 1
ERROR: Input contains prohibited control code point U+0008
```

**원인**: Tistory에서 추출한 일부 포스트에 백스페이스(U+0008) 등의 제어 문자 포함

**해결**:
```python
def remove_control_characters(text):
    """제어 문자 제거"""
    cleaned = ''.join(
        ch for ch in text
        if ord(ch) >= 32 or ch in '\n\t\r'
    )
    return cleaned.replace('\x00', '')
```

**에러 2: 파일명의 과도한 대시**

예: `2019-09-23---NodeJS---NPM--PM2.md` (3개 이상의 대시)

**해결**:
```python
def clean_filename(filename):
    """연속된 대시 제거"""
    clean = re.sub(r'-{2,}', '-', filename)
    return clean.strip('- ')
```

**에러 3: 이미지 링크 누락**

```
원인: HTML을 `.get_text()`로 변환하면 모든 HTML 태그가 제거되어
     이미지 태그도 함께 삭제됨
```

**해결**:
```python
# 잘못된 방법 ❌
content = article.get_text()  # 이미지 링크 손실

# 올바른 방법 ✅
# 1단계: 이미지 다운로드 및 src 업데이트
for img in article.find_all('img'):
    # ... 이미지 다운로드
    img['src'] = f"/assets/images/posts/{img_name}"

# 2단계: 마크다운으로 변환 (이미지 링크 보존)
content = markdownify(str(article))
```

**에러 4: 잘못된 HTML 태그로 인한 빌드 실패**

```
ERROR: Invalid first code point of tag name U+D0DC
```

**원인**: 마크다운 코드블록의 HTML 예제가 실제 HTML 태그로 렌더링됨

예: `<태그>`, `< 46`, `< 0.05`가 HTML로 해석됨

**해결**:
```markdown
# 잘못된 방법 ❌
```html
<script src="bg.js"></script>
```

# 올바른 방법 ✅
```html
&lt;script src="bg.js"&gt;&lt;/script&gt;
```
```

**에러 5: Tistory 아티팩트 텍스트**

포스트 하단에 다음 텍스트가 자동으로 추가됨:
- 공유하기
- 게시글 관리
- 관성을 이기는 데이터
- 저작자표시 (새창열림)

**해결**:
```python
def remove_tistory_artifacts(content):
    """Tistory 아티팩트 제거"""
    artifacts = [
        r"^\s*공유하기\s*$",
        r"^\s*게시글 관리\s*$",
        r"^\s*관성을 이기는 데이터\s*$",
        r"^\s*저작자표시\s*\(새창열림\)\s*$",
    ]

    for pattern in artifacts:
        content = re.sub(pattern, '', content, flags=re.MULTILINE)

    return content
```

#### 5.2 검증 스크립트

```python
import yaml

def validate_posts():
    """모든 포스트 검증"""
    posts_dir = Path('_posts')
    valid_count = 0
    error_count = 0

    for post_file in posts_dir.glob('*.md'):
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # YAML 파싱 (문법 체크)
            if content.startswith('---'):
                parts = content.split('---', 2)
                yaml.safe_load(parts[1])

            # 제어 문자 확인
            if any(ord(ch) < 32 and ch not in '\n\t\r' for ch in content):
                print(f"제어 문자 발견: {post_file.name}")
                error_count += 1
                continue

            valid_count += 1

        except Exception as e:
            print(f"오류: {post_file.name} - {e}")
            error_count += 1

    print(f"\n✅ 유효한 포스트: {valid_count}")
    print(f"❌ 오류: {error_count}")

    return valid_count, error_count
```

---

## 최종 결과

### 마이그레이션 통계

| 항목 | 수치 |
|------|------|
| **총 포스트** | 112개 |
| **총 이미지** | 788개 |
| **원본 이미지 크기** | 167.51 MB |
| **압축 후 이미지 크기** | 41.08 MB |
| **크기 감소** | 126.43 MB (75.5% 절약) |
| **포스트 검증 성공률** | 100% (112/112) |
| **카테고리 매핑** | 100% (112/112) |

### 카테고리 분포

| 카테고리 | 포스트 수 | 비율 |
|---------|----------|-----|
| Finance (금융) | 32 | 28.6% |
| Technology (기술) | 23 | 20.5% |
| Web/JavaScript | 17 | 15.2% |
| ML/DL (머신러닝) | 16 | 14.3% |
| Server/Data/Cloud | 13 | 11.6% |
| Quantitative Investment | 8 | 7.1% |
| Business Analytics | 3 | 2.7% |

---

## Git 커밋 히스토리

마이그레이션 전체 과정은 다음과 같은 커밋으로 기록되었습니다:

```
002797c migrated 112 posts from Tistory
7092b7f Fix HTML code blocks in Web-HTML post
14cf009 Fix all remaining HTML code blocks
06010c6 Fix HTML code blocks - escape all tags
7f974a4 Remove Tistory blog artifacts from all posts
aac9db5 Add categories to all posts
```

---

## 배운 점 및 권장사항

### 1. 사전 계획의 중요성

마이그레이션 전에 다음을 확인하세요:
- 포스트 수 및 이미지 수
- 파일 명명 규칙
- 카테고리 구조
- 예상 소요 시간

### 2. 자동화 스크립트 작성

수동으로 하나씩 처리하는 것은 비현실적입니다. Python으로 자동화 스크립트를 작성하세요.

### 3. 단계별 검증

각 단계 후 검증을 수행하세요:
- 포스트 추출 후: 포스트 수 확인
- 이미지 다운로드 후: 이미지 개수 및 링크 확인
- 마크다운 변환 후: YAML 문법 검증
- 최종: 모든 포스트 빌드 테스트

### 4. 버전 관리 활용

Git을 활용하여 각 단계를 기록하세요:
```bash
git add -A
git commit -m "Step 1: Extract posts from Tistory"
git commit -m "Step 2: Download and compress images"
git commit -m "Step 3: Convert to Jekyll format"
```

### 5. 에러 로깅

모든 오류를 기록하고 분류하세요:

```python
import logging

logging.basicConfig(
    filename='migration.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    # 작업 수행
    pass
except Exception as e:
    logging.error(f"Error: {e}", exc_info=True)
```

---

## 마이그레이션 스크립트 제공

전체 마이그레이션 프로세스를 위한 통합 스크립트는 다음 저장소에서 확인할 수 있습니다:

```
https://github.com/sw-song/sw-song.github.io
```

포함된 스크립트:
- `migrate.py`: 메인 마이그레이션 스크립트
- `compress_images.py`: WebP 압축
- `remove_tistory_artifacts.py`: 아티팩트 제거
- `map_post_categories.py`: 카테고리 매핑
- `validate_posts.py`: 포스트 검증

---

## 결론

Tistory에서 GitHub Pages로의 마이그레이션은 초기에는 복잡해 보이지만, 체계적으로 접근하면 성공할 수 있습니다. 주요 포인트는:

1. **자동화**: 수백 개의 포스트는 수동으로 처리 불가능
2. **검증**: 각 단계에서 결과를 확인하고 오류 처리
3. **문서화**: 각 단계와 오류를 기록
4. **버전 관리**: Git으로 진행 상황 추적

이 가이드가 여러분의 블로그 마이그레이션에 도움이 되길 바랍니다!

---

## 참고 자료

- [Jekyll 공식 문서](https://jekyllrb.com/)
- [GitHub Pages 가이드](https://pages.github.com/)
- [Markdownify 문서](https://github.com/matthewwithanm/python-markdownify)
- [BeautifulSoup 문서](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

