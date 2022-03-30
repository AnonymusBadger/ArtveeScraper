# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Artwork(Item):
    # define the fields for your item here like:
    artwork_title = Field()
    artwork_year = Field()
    artwork_url = Field()
    artist_name = Field()
    artist_country = Field()
    artist_years = Field()
    artist_about = Field()
    image_url = Field()
    image = Field()
