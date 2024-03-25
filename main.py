from scraper import Scraper

if __name__ == "__main__":
    ip = input("Enter a search term: ")
    print(f"Scraping images of {ip}...")
    Scraper(ip, screenshot=True).scrape()
