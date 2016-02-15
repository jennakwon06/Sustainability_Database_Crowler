from scrapy.http import Request
from scrapy.spiders import Spider
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from sust_reports.settings import FILES_STORE
import time
import csv
import os
import io

class sustSpider(Spider):
    name = "sust"
    start_urls = [
        "http://database.globalreporting.org/search",
    ]

    driver = webdriver.Chrome()

    def parse(self, response):
        with io.open("global_500_data.csv", encoding='utf8', errors='ignore') as f:
            for row in csv.DictReader(f):
                if row['GR_name'] != '':
                    self.driver.get(response.url)
                    company = row['GR_name']

                    # wait until companies button shows up
                    companies_button = self.driver.find_element_by_id("show-companies-toolbox")
                    if not companies_button.is_displayed():
                        for i in range(10):
                            if not companies_button.is_dislayed():
                                time.sleep(0.5)
                    companies_button.click()

                    # wait until search button shows up
                    searchfield = self.driver.find_element_by_id('search-field')
                    if not searchfield.is_displayed():
                        for i in range(10):
                            if not searchfield.is_displayed():
                                time.sleep(0.5)

                    # clear the button and send in the company name
                    searchfield.clear()
                    searchfield.send_keys(company)
                    self.driver.find_element_by_id('go-company-search').click()

                    time.sleep(3)
                    try:
                        list = self.driver.find_elements_by_xpath('//div[@class="company-name"]//a')
                        for link in list:
                            link = link.get_attribute('href')
                            yield Request(link, callback=self.parse_comp_link, meta={'company': company})
                    except StaleElementReferenceException:
                        print "exception happened"
                        continue

    def parse_comp_link(self, response):
        company = response.meta['company']
        self.driver.get(response.url)
        list = self.driver.find_elements_by_xpath('//a[contains(@href, "reports/view")]')
        for link in list:
            link = link.get_attribute('href')
            yield Request(link, callback=self.parse_report_link, meta={'company': company})

    def parse_report_link(self, response):
        company = response.meta['company']
        self.driver.get(response.url)
        for link in response.xpath('//a[@href]/@href').extract():
            if link.endswith('.pdf'):
                yield Request(link, callback=self.save_pdf, meta={'company': company})

    def save_pdf(self, response):
        path = os.path.join(FILES_STORE, response.meta['company'])
        if not os.path.exists(path):
            os.makedirs(path)
        pdfname = response.url.split('/')[-1]
        path = os.path.join(path, pdfname)
        with open(path, 'wb') as f:
            f.write(response.body)


