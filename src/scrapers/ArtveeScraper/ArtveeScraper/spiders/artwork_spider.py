import scrapy
from src.Terminal import terminal
from src.Text import decorate
from src.ProgessBar import ProgresBar
from src.scrapers.ArtveeScraper.ArtveeScraper.items import Artwork

import logging

logging.basicConfig(
    filename="log.txt",
    format="%(levelname)s: %(message)s",
    level=logging.DEBUG,
)


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

        yield from response.follow_all(urls, callback=self.parseSerachPage)

    def parseSerachPage(self, response):
        urls = response.xpath(
            "//a[contains(@class,'product-image-link')]/@href"
        ).getall()

        for url in urls:
            self.artworksProgress.addToTarget()

        self.pagesProgress.increment()

        yield from response.follow_all(urls, callback=self.parseArtworks)

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
        }

        self.artworksProgress.increment()

        self.logger.debug(Artwork(data))

        yield Artwork(data)

    def _parseArtwork(self, titleRaw):
        title = self._stripTextInList(titleRaw)
        title = " ".join(title)

        if title.find(")") != -1:
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

        artistYearCountry = artistRaw.xpath("./div/text()").get().split(",")
        if artistYearCountry:
            counrty = artistYearCountry[0].strip("(), ")
            self.logger.debug(artistYearCountry[1])
            year = artistYearCountry[1].strip("(), ")
        else:
            counrty = None
            year = None

        return {
            "artist_name": artist,
            "artist_country": counrty,
            "artist_years": year,
            "artist_about": about,
        }
