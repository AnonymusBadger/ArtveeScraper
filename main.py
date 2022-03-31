import os
import sys
import app
import scrapy
import ArtveeScraper
import ArtveeScraper.pipelines
import ArtveeScraper.items
import scrapy.spiderloader
import scrapy.statscollectors
from src.Ui import Ui

if __name__ == "__main__":
    app.init()
    Ui()
