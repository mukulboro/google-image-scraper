from scraper import Scraper
import argparse

cli_description = "Scrape images from Google Images"
parser = argparse.ArgumentParser(description=cli_description)\

parser.add_argument('-k', '--keyword', type=str, help='Keyword to search for images', required=True)
parser.add_argument('-s', '--screenshot', type=int, help='Take a screenshot instead of downloading images (0 or 1)', default=0)

args = parser.parse_args()

if args.screenshot == 0:
    ss = False
elif args.screenshot == 1:
    ss = True
else:
    print("Invalid value for --screenshot argument. Exiting...")
    exit(1)

if args.keyword:
    print(f"{'Scraping' if not ss else 'Screenshoting'} images for {args.keyword}")
    s = Scraper(args.keyword, screenshot=ss)
    s.scrape()