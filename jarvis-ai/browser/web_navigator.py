from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import html2text

class BrowserIntegration:
    def __init__(self):
        # We will initialize playwright on demand instead of globally 
        # to avoid thread-blocking issues in FastAPI
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True
        self.html_converter.bypass_tables = False

    def browse_url(self, url: str) -> str:
        """Opens a headless Chrome browser, goes to the URL, and scrapes the text content."""
        if not url.startswith("http"):
            url = "http://" + url
            
        print(f"[Browser] Fietao navigating to: {url}")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                # 15 second timeout to prevent hanging forever
                page.goto(url, timeout=15000)
                
                # Get the page HTML content
                html_content = page.content()
                
                browser.close()
                
                # Use BeautifulSoup to strip out all the scripts, styles, etc.
                soup = BeautifulSoup(html_content, "html.parser")
                
                # Remove unwanted tags
                for tag in soup(["script", "style", "nav", "footer", "header"]):
                    tag.decompose()
                    
                # Convert what's left into clean Markdown for the LLM
                clean_text = self.html_converter.handle(str(soup))
                
                # Limit the length so we don't blow up the LLM context window (e.g., max 4000 chars)
                if len(clean_text) > 4000:
                    clean_text = clean_text[:4000] + "\n...[TRUNCATED FOR LENGTH]..."
                    
                return clean_text
                
        except Exception as e:
            return f"[Browser Error] Failed to scrape {url}. Reason: {e}"

# Export an instance
browser_ext = BrowserIntegration()
