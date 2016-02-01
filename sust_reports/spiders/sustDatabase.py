import urlparse

from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from sust_reports.items import ReportItem


class sustSpider(Spider):
    name = "sust"
    # allowed_domains = ["database.globalreporting.org"] not specifying will allow all domains
    start_urls = [
        "http://database.globalreporting.org/reports/view/34452",
    ]

    for company in open("companies", 'r').readlines():
        company = company.split(' ', 1)[0]
    #     search company in the website & click go
    #     for each result, click and parse



    # response.css("#go-report-search")
    # response.xpath('//input[@class="search-field"]')
    # parse the response data and extract the scraped data
    def parse(self, response):
        for a in response.xpath('//a[@href]/@href'):
            item = ReportItem()
            link = a.extract()
            if link.endswith('.pdf'):
                self.logger.info(link)
                item['name'] = 'myComp'
                item['file_urls'] = link
                return item
    #             yield Request(link, callback=self.save_pdf)
    #
    # def save_pdf(self, response):
    #     path = response.url.split('/')[-1]
    #     with open(path, 'wb') as f:
    #         f.write(response.body)


