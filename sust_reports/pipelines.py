# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from sust_reports.settings import FILES_STORE


class SustReportsPipeline(FilesPipeline):

    def process_item(self, item, spider):
        # spider.logger.info('INSIDE PROCESS ITEMS' + item['file_urls'])
        path = os.path.join(FILES_STORE, item['name'])
        report = item['file_urls'].split('/')[-1]

        if not os.path.exists(path):
            os.makedirs(path)

        path = os.path.join(path, report)

        with open(path, 'wb') as f:
            f.write(path)
            return item

        # for file_url in item['file_urls']:
        #     spider.logger.info(item)
        #     spider.logger.info(file_url)
        #     path = file_url.split('/')[-1]
        #     with open(path, 'wb') as f:
        #         f.write(file_url)
        #         return item

                    #     with open(path, 'wb') as f:
    #         f.write(response.body)


    #         yield scrapy.Request(file_url)
    #
    #     spider.logger.info('Am I in the pipeline?')
    #     return item
    #
    # # def get_media_requests(self, item, info):
    #
    #
    # def item_completed(self, results, item, info):
    #     file_paths = [x['path'] for ok, x in results if ok]
    #     if not file_paths:
    #         raise DropItem("Item contains no files")
    #     item['file_paths'] = file_paths
    #     return item
