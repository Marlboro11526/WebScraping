import scrapy

class LordandtaylorSpider(scrapy.Spider):
    name = 'lordandtaylor_spider'
    allowed_domains = ['lordandtaylor.com']
    start_urls = ['https://www.lordandtaylor.com/']

    def parse(self, response):
        categories = response.css('div.header-main-wrapper.fixed-header > div > div.header-sticky-wrapper > div > header > div:nth-child(1) > div.menu-layout.header-layout.header-layout--center-left > div > ul.site-nav.site-navigation.small--hide.active a::attr(href)').getall()
        print(categories)