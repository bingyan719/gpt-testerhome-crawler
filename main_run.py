#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Icy Li
# @Date  : 2023/12/27

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from testergpt.spiders.tester_home_topics import TesterHomeTopicsSpider


def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(TesterHomeTopicsSpider)
    process.start()

if __name__ == "__main__":
    run_spider()
