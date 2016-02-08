from scrapy.http import Request
from scrapy.spiders import Spider
from selenium import webdriver
from sust_reports.settings import FILES_STORE
import time
import os

class sustSpider(Spider):
    name = "sust"
    # allowed_domains = ["database.globalreporting.org"] not specifying will allow all domains
    start_urls = [
        "http://database.globalreporting.org/search",
    ]

    driver = webdriver.Chrome()

    # def start_requests(self):
    #     with open("companies", 'r') as f:
    #         for line in f:
                # company = line.rstrip().partition(' ')[0]
                # yield Request("http://database.globalreporting.org/search", callback=self.parse, meta={'company': company})

    def parse(self, response):
        self.driver.get(response.url)
        searchfield = self.driver.find_element_by_id('search-field')
        # if searchfield.is_displayed():
        #     searchfield.clear()
        with open("companies", 'r') as f:
            for line in f:
                company = line.rstrip().partition(' ')[0]
                self.driver.find_element_by_id("show-companies-toolbox").click()
                if not searchfield.is_displayed():
                    for i in range(10):
                        if not searchfield.is_displayed():
                            time.sleep(0.5)
                searchfield.clear()
                searchfield.send_keys(company)
                self.driver.find_element_by_id('go-company-search').click()
                time.sleep(1)
#                  all the relevant links will pop up?
    #             listoflinks = self.driver.find_elements_by_xpath('//div[@class="company-name"]//a/@href')
    #             response.selector.remove_namespaces()
                # listoflinks = response.xpath('//div[@class="company-name"]//a/@href').extract()
                list = self.driver.find_elements_by_xpath('//div[@class="company-name"]//a')
                for link in list:
                    link = link.get_attribute('href')
                    # self.logger.info("inside parse", link)
                    yield Request(link, callback=self.parse_comp_link, meta={'company': company})

    def parse_comp_link(self, response):
        company = response.meta['company']
        self.driver.get(response.url)
        list = self.driver.find_elements_by_xpath('//a[contains(@href, "reports/view")]')
        for link in list:
            link = link.get_attribute('href')
            # self.logger.info("inside parse_comp_link", link)
            yield Request(link, callback=self.parse_report_link, meta={'company': company})

    def parse_report_link(self, response):
        company = response.meta['company']
        self.driver.get(response.url)
        for link in response.xpath('//a[@href]/@href').extract():
            if link.endswith('.pdf'):
                # self.logger.info("inside parse_report_link", a)
                # item = ReportItem()
                # item['name'] = response.meta['company']
                # item['file_urls'] = a
                # item['content'] = response
                # self.logger.info(a)
                # return item
                yield Request(link, callback=self.save_pdf, meta={'company': company})

    def save_pdf(self, response):
        path = os.path.join(FILES_STORE, response.meta['company'])

        if not os.path.exists(path):
            os.makedirs(path)

        pdfname = response.url.split('/')[-1]

        path = os.path.join(path, pdfname)

        with open(path, 'wb') as f:
            f.write(response.body)


