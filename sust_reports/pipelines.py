# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy
from scrapy.pipelines.files import FilesPipeline
from sust_reports.settings import FILES_STORE


class SustReportsPipeline(FilesPipeline):

    def process_item(self, item, spider):
        path = os.path.join(FILES_STORE, item['name'])
        report = item['file_urls'].split('/')[-1]

        if not os.path.exists(path):
            os.makedirs(path)

        path = os.path.join(path, report)

        with open(path, 'wb') as f:
            f.write(item['content'].body)
            return item

