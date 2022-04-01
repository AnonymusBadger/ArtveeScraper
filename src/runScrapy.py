import app
import requests
from time import sleep
import subprocess
import sys
from src.Terminal import terminal
from src.Text import decorate
from bs4 import BeautifulSoup
from src.UserInput import userInput
from src.FileSystem import filesystem
from ArtveeScraper.spiders.artwork_spider import run as runSpider


class Run:
    def __init__(self):
        self.searchUrl = "https://artvee.com/s/?s="

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
                runSpider(targetUrl, query)

                sleep(1)
                terminal.info("Done")
                terminal.printDecorator(True)
                if app.config.osType == "Darwin":
                    CMD = '''
                    on run argv
  		      display notification (item 2 of argv) with title (item 1 of argv)
		    end run
	 	    '''
                    subprocess.call(['osascript', '-e', CMD, "Artvee scraper", "Scrapper finished!"])
                elif app.config.osType == "Linux":
                    subprocess.Popen(['notify-send', "Scrapper finished!"])
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
        terminal.clear()
        terminal.printDecorator()
        terminal.info("Checking if search has results", True)
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
