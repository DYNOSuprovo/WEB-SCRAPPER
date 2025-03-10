import requests
from bs4 import BeautifulSoup
import ollama
from fpdf import FPDF
import argparse
from playwright.sync_api import sync_playwright
import time
import re

def extract_main_content(page):
    # Try to extract meaningful content
    selectors = [
        'main', 'article', '[role="main"]', '[role="article"]', 'section'
    ]
    content = ""

    for selector in selectors:
        try:
            element = page.query_selector(selector)
            if element:
                content = element.inner_text()
                if len(content.split()) > 100:  # Ensure meaningful content
                    return content
        except Exception:
            continue

    # Fallback to body text if no main content found
    return page.inner_text('body')


def scrape_website(url):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/121.0.0.0"
        )
        page = context.new_page()

        try:
            page.goto(url, wait_until='load', timeout=120000)
            time.sleep(5)
            for i in range(10):
                page.mouse.wheel(0, 1000)
                time.sleep(1)

            text_content = extract_main_content(page)
            title = page.title()
        except Exception as e:
            print(f"[!] Failed to load page: {e}")
            text_content = "Content could not be loaded."
            title = "Unknown Company"

        browser.close()
    return title, text_content


def generate_summary(content):
    prompt = f"""
    You are an expert content summarizer. Summarize the following content in a clear, concise, and professional tone:

    {content}
    """
    response = ollama.chat(model='mistral', messages=[{"role": "user", "content": prompt}])
    return response['message']['content']


def generate_brochure(company_name, summary):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt=company_name.encode('latin-1', 'ignore').decode('latin-1'), ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    sanitized_summary = summary.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=sanitized_summary)

    # Sanitize filename by removing invalid characters
    safe_company_name = re.sub(r'[\\/*?"<>|,:]', '_', company_name)
    pdf_file = f"{safe_company_name}_Brochure.pdf"
    pdf.output(pdf_file)
    print(f"[+] Brochure saved as {pdf_file}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help='Company website URL')
    args = parser.parse_args()

    print("[+] Scraping website...")
    company_name, content = scrape_website(args.url)

    print("[+] Generating summary using Mistral 7B...")
    summary = generate_summary(content)

    print("[+] Creating PDF brochure...")
    generate_brochure(company_name, summary)


if __name__ == "__main__":
    main()
