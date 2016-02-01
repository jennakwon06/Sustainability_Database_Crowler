# # This package will contain the spiders of your Scrapy project
# #
# # Please refer to the documentation for information on how to create and manage
# # your spiders.
#
# from scrapy.spider import Spider
# from scrapy.selector import Selector
# from scrapy.spider import BaseSpider
# from scrapy.selector import HtmlXPathSelector
# from scrapy.http import FormRequest
# from scrapy.http import Request
# import json
#
# class sustSpider1(scrapy.Spider):
#     name = "wnd"
#     allowed_domains = ['google.com']
#     url_prefix = []
#
#     start_urls = []
#     for company in open("companies", 'r').readlines():
#
#
# def parse(self, response):
#     sel = Selector(response)
#
# class SustSpider(BaseSpider):
#     name = "dmoz"
#     max_pages = 100
#     allowed_domains = ["http://database.globalreporting.org/search"]
#     start_urls = ["http://database.globalreporting.org/search"]
#
# # Search on the website, currently I have just put in a static search term here, but I would like to loop over a list of companies.
#
#     def list_iterator(self):
#         for i in range(self.max_pages):
#             yield Request('https://projects.propublica.org/docdollars/search?page=d' % i, callback=self.parse)
#
#     def parse(self, response):
#         for sel in response.xpath('//*[@id="payments_list"]/tbody'):
#             item = PropubItem()
#             item['payee'] = sel.xpath('tr[1]/td[1]/a[2]/text()').extract()
#             item['link'] = sel.xpath('tr[1]/td[1]/a[1]/@href').extract()
#             item['city'] = sel.xpath('tr[1]/td[2]/text()').extract()
#             item['state'] = sel.xpath('tr[1]/td[3]/text()').extract()
#             item['company'] = sel.xpath('tr[1]/td[4]').extract()
#             item['amount'] =  sel.xpath('tr[1]/td[7]/span/text()').extract()
#             yield item
#
#     def parse(self, response):
#         return FormRequest.from_response(response, formdata={'q': rebtel},callback=self.search_result)
#
# # I fetch the url from the search result and convert it to correct Financial-url where the information is located.
#
#     def search_result(self,response):
#         sel = HtmlXPathSelector(response)
#         link = sel.xpath('//ul[@class="company-list two-columns"]/li/a/@href').extract()
#         finance_url=str(link[0]).replace("/foretag","http://www.proff.se/nyckeltal")
#         return Request(finance_url,callback=self.parse_finance)
#
# # I Scraped the information of this particular company, this is hardcoded and will not
# # work for other responses. I had some issues with the encoding characters
# # initially since they were Swedish. I also tried to target the Json element direct by
# # revenue = sel.xpath('#//*[@id="accountTable1"]/tbody/tr[3]/@data-chart').extract()
# # but was not able to parse it (error - expected string or buffer - tried to convert it
# # to a string by str() with no luck, something off with the formatting, which is messing the the data types.
#
#     def parse_finance(self, response):
#         sel = HtmlXPathSelector(response)
#         datachart = sel.xpath('//tr/@data-chart').extract()
#         employees=json.loads(datachart[36])
#         revenue = json.loads(datachart[0])
#         items = []
#         item = DmozItem()
#         item['company']=response.url.split("/")[-5]
#         item['market']=response.url.split("/")[-3]
#         item['employees']=employees
#         item['revenue']=revenue
#         items.append(item)
#         return item