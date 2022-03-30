# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ArtveescraperPipeline:
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
    #     return super().process_item(item, spider)

    def get_media_requests(self, item, info):
        print("Hello")
        print(info)
        print(item)
        yield Request(item["image_url"], meta={"title": item["artwork_title"]})

    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = request.meta.get("title")
        return f"{file_name}.jpg"
