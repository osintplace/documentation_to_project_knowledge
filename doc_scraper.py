
"""
📘 doc_scraper.py
Flexible, documented Python tool for scraping and converting documentation websites to Markdown and JSON.
"""

import requests
from bs4 import BeautifulSoup
import markdownify
from urllib.parse import urljoin, urlparse
from tqdm import tqdm
import argparse
import time
from datetime import datetime
import os
import logging
import json

# Setup logging
logging.basicConfig(filename="errors.log", level=logging.ERROR, format="%(asctime)s - %(message)s")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; generic-doc-scraper/1.0)'
}

def get_sidebar_links(base_url):
    """Scrape all internal documentation links from sidebars."""
    response = requests.get(base_url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    sidebar_links = set()
    for nav_tag in soup.find_all(['nav', 'aside']):
        for a in nav_tag.find_all('a', href=True):
            href = a['href']
            if href.startswith('#') or 'mailto:' in href:
                continue
            if any(href.endswith(ext) for ext in [".pdf", ".zip", ".jpg", ".png"]):
                continue
            full_url = urljoin(base_url, href)
            parsed_url = urlparse(full_url)._replace(query="", fragment="")
            if parsed_url.netloc == urlparse(base_url).netloc:
                sidebar_links.add(parsed_url.geturl())

    return sorted(sidebar_links)

def fetch_and_convert(url):
    """Fetch and convert main content of a page to Markdown."""
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
    except Exception as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return ""

    soup = BeautifulSoup(res.text, 'html.parser')
    content = soup.find('main')
    if not content:
        candidates = soup.find_all('article') + soup.find_all('div', class_='theme-doc-markdown')
        content = max(candidates, key=lambda el: len(str(el)), default=None)

    if not content:
        logging.error(f"No readable content found on {url}")
        return ""

    h1 = soup.find('h1') or soup.find('h2')
    title = h1.get_text(strip=True) if h1 else (soup.title.string.strip() if soup.title else url)
    markdown = markdownify.markdownify(str(content), heading_style="ATX")
    return f"# {title}\n\n{markdown.strip()}\n\n---\n"

def convert_md_to_json(md_file_path, json_output_path):
    """Convert Markdown to structured JSON."""
    sections = []
    current_section = {"title": None, "content": []}

    with open(md_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('# '):
                if current_section["title"]:
                    sections.append(current_section)
                current_section = {"title": line.strip('# ').strip(), "content": []}
            else:
                current_section["content"].append(line.strip())

        if current_section["title"]:
            sections.append(current_section)

    with open(json_output_path, 'w', encoding='utf-8') as jf:
        json.dump(sections, jf, indent=2, ensure_ascii=False)

def main():
    """Main entrypoint for CLI execution."""
    parser = argparse.ArgumentParser(description="Documentation Site to Markdown & JSON")
    parser.add_argument("base_url", help="Base documentation URL")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests (in seconds)")
    parser.add_argument("--output-dir", default=".", help="Directory to save outputs")
    args = parser.parse_args()

    base_url = args.base_url.rstrip('/')
    domain = urlparse(base_url).netloc.replace("www.", "")
    timestamp = datetime.now().strftime("%Y%m%d")
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    md_file = os.path.join(output_dir, f"docs_{domain}_{timestamp}.md")
    json_file = os.path.join(output_dir, f"docs_{domain}_{timestamp}.json")
    partial_file = os.path.join(output_dir, "docs_partial.md")

    try:
        print("📚 Crawling documentation structure...")
        links = get_sidebar_links(base_url)
        if base_url not in links:
            links.insert(0, base_url)

        print(f"🔗 Found {len(links)} links to process.\n")

        with open(md_file, "w", encoding="utf-8") as full_out, \
             open(partial_file, "w", encoding="utf-8") as partial_out:

            for url in tqdm(links, desc="Processing pages"):
                md = fetch_and_convert(url)
                full_out.write(md)
                partial_out.write(md)
                time.sleep(args.delay)

        print(f"\n✅ Markdown saved to: {md_file}")
        convert_md_to_json(md_file, json_file)
        print(f"✅ JSON version saved to: {json_file}")

    except KeyboardInterrupt:
        print("\n⛔ Interrupted by user. Partial output saved.")

if __name__ == "__main__":
    main()
