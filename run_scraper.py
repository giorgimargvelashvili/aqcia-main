import sys
import os
import time
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.scraper import run_scrape

if __name__ == "__main__":
    while True:
        try:
            run_scrape()
            print(f"[{datetime.now()}] Scrape complete. Sleeping for 24 hours...\n")
        except Exception as e:
            print(f"[{datetime.now()}] An unexpected error occurred: {e}")
        
        # Sleep for 24 hours
        time.sleep(86400) 