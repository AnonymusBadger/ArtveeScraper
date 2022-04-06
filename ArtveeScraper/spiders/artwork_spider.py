import scrapy
from twisted.internet import reactor, task
from src.Terminal import terminal
from src.Text import decorate
from src.ProgessBar import ProgresBar
from ArtveeScraper.items import Artwork
from scrapy.crawler import CrawlerRunner
import app
import uuid

import logging

# logging.basicConfig(
#     filename="log.txt",
#     format="%(levelname)s: %(message)s",
#     level=logging.DEBUG,
# )


class ArtworksSpider(scrapy.Spider):
    name = "artworks"

    def __init__(self, query="", name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.query = query
        self.pagesProgress = ProgresBar("Pages")
        self.artworksProgress = ProgresBar("Artworks")
        self.imagesProgress = ProgresBar("Images")

    def parse(self, response):
        baseUrl = "https://artvee.com/s/page/num/?s=" + self.query
        pagination = response.xpath("//ul[@class='page-numbers']")

        totalPages = 1
        if pagination:
            totalPages = response.xpath(
                "//a[contains(@class, 'page-numbers') and not(contains(@class, 'next'))]/text()"
            ).getall()[-1]
            totalPages = int(totalPages)

        terminal.info(f"{decorate.bold('Found')}: {totalPages} pages")

        urls = [baseUrl.replace("num", str(n)) for n in range(1, totalPages + 1)]

        for url in urls:
            self.pagesProgress.addToTarget()

        yield from response.follow_all(urls, callback=self.parseSerachPage, errback=self.errback)

    def errback(self, respnse):
        terminal.warning(f"Failed to parse: {respnse.url}")

    def parseSerachPage(self, response):
        urls = response.xpath(
            "//a[contains(@class,'product-image-link')]/@href"
        ).getall()

        for url in urls:
            self.artworksProgress.addToTarget()

        self.pagesProgress.increment()

        yield from response.follow_all(urls, callback=self.parseArtworks, errback=self.errback)

    def parseArtworks(self, response):
        artworkRaw = response.xpath(
            '//h1[contains(@class,"entry-title")]//text()'
        ).getall()
        artistRaw = response.xpath('//div[contains(@class,"tartist")]')
        imageURL = response.xpath('//div[contains(@class,"w3eden dl_med")]//a/@href')[
            -1
        ].get()

        artworkData = self._parseArtwork(artworkRaw)
        artistData = self._parseArtist(artistRaw)

        data = {
            **artworkData,
            **artistData,
            "artwork_url": response.url,
            "image_url": imageURL,
            "image_file_name": uuid.uuid1()
        }

        self.artworksProgress.increment()
        self.logger.debug(Artwork(data))

        yield Artwork(data)

    def _parseArtwork(self, titleRaw):
        title = self._stripTextInList(titleRaw)
        title = " ".join(title)

        if title.count('(') > 1:
          year = title[title.find(")") + 1 : -1].strip("( )")
          title = title[0:title.find(")") + 1]

        elif title.find(")") != -1:
            year = title[title.find("(") + 1 : title.find(")")]
            title = title[0 : title.find("(")].strip()
        else:
            year = None
            title = title.strip()

        return {"artwork_title": title, "artwork_year": year}

    def _stripTextInList(self, _list):
        return list(map(lambda t: t.strip(), _list))

    def _parseArtist(self, artistRaw):
        lastItem = artistRaw[-1]
        lastItemText = lastItem.xpath(".//text()").getall()
        lastItemText = self._stripTextInList(lastItemText)

        if "About the Artist" in lastItemText:
            about = lastItem.xpath("./following-sibling::div//text()").getall()
            about = "\n".join(self._stripTextInList(about))
        else:
            about = None

        artist = artistRaw.xpath("./div/a/text()").get().strip()

        artistYearCountry = artistRaw.xpath("./div/text()").get()
        if artistYearCountry:
            yc = artistYearCountry.split(",")
            counrty = yc[0].strip("(), ")
            self.logger.debug(yc[1])
            year = yc[1].strip("(), ")
        else:
            counrty = None
            year = None

        return {
            "artist_name": artist,
            "artist_country": counrty,
            "artist_years": year,
            "artist_about": about,
        }


def run(url, query):
    # process = CrawlerProcess(
    newDir = app.scraperConfig.newDirPath
    settings = {
        "LOG_ENABLED": False,
        "LOG_FORMAT": "[%(name)s] %(levelname)s: %(message)s",
        "LOG_LEVEL": "WARNING",
        "BOT_NAME": "ArtveeScraper",
        "SPIDER_MODULES": ["ArtveeScraper.spiders"],
        "NEWSPIDER_MODULE": "ArtveeScraper.spiders",
        "IMAGES_STORE": f"{newDir}/artworks",
        "ROBOTSTXT_OBEY": True,
        "ITEM_PIPELINES": {
            "ArtveeScraper.pipelines.MyImagesPipeline": 300,
        },
        "IMAGES_URLS_FIELD": "image_url",
        "FEEDS": {
            f"{newDir}/data.csv": {
                "format": "csv",
                "encoding": "utf8",
                "fields": [
                    "artwork_title",
                    "artwork_year",
                    "artwork_url",
                    "artist_name",
                    "artist_country",
                    "artist_years",
                    "artist_about",
                    "image_file_name"
                ],
            }
        },
    }
    runner = CrawlerRunner(settings)
    runner.crawl(ArtworksSpider, start_urls=[url], query=query)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()  # the script will block here until all crawling jobs are finished
