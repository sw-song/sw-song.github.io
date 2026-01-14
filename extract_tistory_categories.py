#!/usr/bin/env python3
"""
Extract categories from Tistory blog by scraping the category page.
This will help us understand the category structure and apply it to GitHub blog posts.
"""

import requests
from bs4 import BeautifulSoup
import json
from collections import defaultdict

TISTORY_URL = "https://songseungwon.tistory.com"
CATEGORY_PAGE = f"{TISTORY_URL}/category"

def extract_categories():
    """Extract all categories from Tistory blog"""
    try:
        print("Fetching Tistory category page...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(CATEGORY_PAGE, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find category elements - Tistory uses specific class names
        categories = {}

        # Try different possible selectors for Tistory categories
        # Tistory typically uses .category or .side_category classes
        category_elements = soup.find_all('div', {'class': 'category'})

        if not category_elements:
            # Try alternative selectors
            category_elements = soup.find_all('a', {'class': 'link_cate'})

        if not category_elements:
            # Try to find category list
            category_list = soup.find('div', {'class': 'area_category'})
            if category_list:
                category_elements = category_list.find_all('a')

        if not category_elements:
            print("Could not find category elements. Trying alternative method...")
            # Try to extract from category links
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                if '/category/' in href:
                    text = link.get_text(strip=True)
                    if text and text != 'category':
                        categories[text] = href

        else:
            for elem in category_elements:
                text = elem.get_text(strip=True)
                href = elem.get('href', '')
                if text and text != 'category':
                    categories[text] = href

        if not categories:
            print("Warning: Could not extract categories from Tistory page")
            print("HTML content sample:")
            print(soup.prettify()[:1000])

        return categories

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Tistory: {e}")
        return {}

def extract_categories_from_posts(categories_dict):
    """
    Alternative method: Extract categories from individual post pages
    by following links from the main blog page
    """
    try:
        print("\nFetching main blog page...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(TISTORY_URL, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Try to find category information from post elements
        post_elements = soup.find_all('div', {'class': 'post'})

        if not post_elements:
            # Try alternative class names
            post_elements = soup.find_all('article', {'class': 'item'})

        category_map = defaultdict(set)

        for post in post_elements:
            # Look for category info in post
            category_elem = post.find('a', {'class': 'category'})
            if not category_elem:
                category_elem = post.find('span', {'class': 'cate'})

            if category_elem:
                category_text = category_elem.get_text(strip=True)
                # Try to find post title
                title_elem = post.find('a', {'class': 'title'})
                if title_elem:
                    post_title = title_elem.get_text(strip=True)
                    category_map[category_text].add(post_title)

        return dict(category_map)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching main blog: {e}")
        return {}

if __name__ == '__main__':
    print("=" * 70)
    print("TISTORY CATEGORY EXTRACTION")
    print("=" * 70)
    print()

    # Try to extract categories
    categories = extract_categories()

    if categories:
        print(f"\n✅ Found {len(categories)} categories:\n")
        for i, (cat_name, cat_url) in enumerate(sorted(categories.items()), 1):
            print(f"{i}. {cat_name}")
            print(f"   URL: {cat_url}\n")
    else:
        print("\n⚠️  Could not extract categories using standard method")
        print("Trying alternative extraction method...\n")

        categories = extract_categories_from_posts(categories)
        if categories:
            print(f"\n✅ Found categories in posts:\n")
            for i, (cat_name, posts) in enumerate(sorted(categories.items()), 1):
                print(f"{i}. {cat_name} ({len(posts)} posts)")

    print("\n" + "=" * 70)
    print("Save this list for manual category assignment to posts")
    print("=" * 70)

    # Save to JSON for reference
    output_file = 'tistory_categories.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Categories saved to {output_file}")
