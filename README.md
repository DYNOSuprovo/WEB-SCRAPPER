**# Brochure Generator - Documentation**

## Overview
This project is an AI-powered CLI tool that scrapes and navigates company websites to extract key information, summarize the content using an AI model, and generate a PDF brochure.

## Libraries Used & Why

1. **requests** - Used initially to fetch webpage content (Not currently used but can be added for API-based requests).
2. **BeautifulSoup** - Parses HTML content when needed (alternative to Playwright for static websites).
3. **ollama** - Uses Mistral 7B for content summarization.
4. **fpdf** - Generates the final PDF brochure.
5. **argparse** - Handles command-line arguments.
6. **playwright** - Loads JavaScript-heavy websites and extracts main content dynamically.
7. **time** - Used for delays to ensure complete content loading.
8. **re** - Cleans and sanitizes filenames.

## How It Works

1. **Scraping Website**
   - Uses Playwright to open the given URL.
   - Extracts meaningful content using `<main>`, `<article>`, and other key sections.
   - Scrolls the page to load dynamically generated content.

2. **Summarization**
   - Sends extracted content to `Mistral 7B` via `ollama`.
   - Returns a professional and concise summary.

3. **Generating PDF Brochure**
   - Uses `fpdf` to create a structured PDF with the company name and summary.
   - Cleans file names to avoid OS restrictions.

## Alternative Approaches
- **Scraping without Playwright**: Use `requests` + `BeautifulSoup` for simpler, static sites.
- **Alternative AI Models**: Use OpenAI API or Llama for summarization.
- **UI-Based Approach**: Convert CLI to a Flask/Django web app for interactive usage.

## Usage
Run the script as follows:
```sh
python brochure_generator.py --url "https://www.example.com"
```
The final brochure is saved as a PDF in the current directory.

