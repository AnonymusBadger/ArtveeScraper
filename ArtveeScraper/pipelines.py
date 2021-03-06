# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from PIL import Image
import re

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


def sanitizeFileName(string):
    query = r"^[ .]|[/<>:\"\\|?*]+|[ .]$"

    illegal_char = re.findall(query, string)

    if len(illegal_char) == 0:
        return string
    else:
        return re.sub(query, "_", string)


class ArtveescraperPipeline:
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    Image.MAX_IMAGE_PIXELS = None

    def process_item(self, item, spider):
        return super().process_item(item, spider)

    def get_media_requests(self, item, info):
        yield Request(
            item["image_url"],
            meta={"file_name": item["image_file_name"]},
        )

    def file_path(self, request, response=None, info=None, *, item=None):
        return f"{request.meta.get('file_name')}.jpg"
