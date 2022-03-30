from twisted.internet import reactor, task
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from src.scrapers.ArtveeScraper.ArtveeScraper.spiders.artwork_spider import (
    ArtworksSpider,
)
from src.scrapers.ArtveeScraper.ArtveeScraper.pipelines import MyImagesPipeline
import app
import requests
import sys
from src.Terminal import terminal
from src.Text import decorate
from bs4 import BeautifulSoup
from src.UserInput import userInput
from src.FileSystem import filesystem


class Run:
    def __init__(self):
        self.searchUrl = "https://artvee.com/s/?s="

    def runSpider(self, url, query):
        settings = get_project_settings()
        settings.set(
            "FEEDS",
            {
                f"{app.scraperConfig.newDirPath}/data.csv": {
                    "format": "csv",
                    "encoding": "utf8",
                }
            },
        )
        settings.set("IMAGES_STORAGE", f"{app.scraperConfig.newDirPath}/artworks")
        settings.set("LOG_ENABLED", False)
        settings.set("IMAGES_URLS_FIELD", "image_url")
        # settings.set("SPIDER_MODULES", ["src.scrapers.ArtveeScraper.ArtveeScraper.spiders"])
        # settings.set("NEWSPIDER_MODULE", "src.scrapers.ArtveeScraper.ArtveeScraper.spiders.",)
        settings.set(
            "ITEM_PIPELINES",
            {
                "src.scrapers.ArtveeScraper.ArtveeScraper.pipelines.MyImagesPipeline": 1,
            },
        )
        runner = CrawlerRunner(settings)
        runner.crawl(ArtworksSpider, start_urls=[url], query=query)
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())

        reactor.run()  # the script will block here until all crawling jobs are finished

    def run(self):
        terminal.printDecorator(True)
        query = app.scraperConfig.serializeQuery()
        targetUrl = self.searchUrl + query
        found = self.checkIfResults(targetUrl)
        if not found:
            raise ValueError
        else:
            if not userInput.query_yes_no("Continue?"):
                raise ValueError
            else:
                terminal.clear()
                terminal.printDecorator()

                self.setupDirs()

                terminal.info("Starting scraping")
                self.runSpider(targetUrl, query)

                terminal.info("Done")
                terminal.printDecorator(True)
                print()
                input("Press any key to exit ")
                sys.exit()

    def setupDirs(self):
        terminal.info("Creating save directory", True)
        path = app.scraperConfig.newDirPath
        imagesPath = f"{path}/artworks"
        filesystem.mkdir(path, True)
        filesystem.mkdir(imagesPath)
        terminal.info("Done")

    def checkIfResults(self, url):
        terminal.info("Checking if search has results")
        page = requests.get(url)

        if page.status_code != 200:
            terminal.warning("Cound not connect to the website. Retrying")
            return self.checkIfResults(url)
        else:
            soup = BeautifulSoup(page.text, "html.parser")
            count = soup.find("p", class_="woocommerce-result-count")
            if not count:
                terminal.warning("No results found!")
                return False
            count = count.get_text().strip()
            count = [int(s) for s in count.split() if s.isdigit()][0]
            terminal.info(f"{decorate.bold('Found')}: {count} artworks")
            terminal.info(f"{decorate.bold('Check on')}: {url}")
            return True


crawler = Run()
