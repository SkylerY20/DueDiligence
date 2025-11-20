from celery import Celery
import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(__name__, broker=redis_url, backend=redis_url)

@celery_app.task
def analyze_task(data):
    url = data.get("url")
    if not url:
        return {"error": "No URL provided"}

    results = {}
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            
            # Create scans directory if it doesn't exist
            os.makedirs("/scans", exist_ok=True)
            
            # Generate filename based on URL or timestamp (simplification for now: "scan.png")
            # In a real app, you'd want unique filenames. 
            # Using a simple name for this task as requested.
            screenshot_path = "/scans/scan.png"
            page.screenshot(path=screenshot_path)
            
            title = page.title()
            content = page.content()
            soup = BeautifulSoup(content, "html.parser")
            
            # Extract text from body
            body_text = soup.body.get_text(separator=" ", strip=True) if soup.body else ""
            text_preview = body_text[:500]
            
            results = {
                "title": title,
                "text_preview": text_preview,
                "screenshot_file": screenshot_path
            }
            
            browser.close()
            
    except Exception as e:
        return {"error": str(e)}

    return results
