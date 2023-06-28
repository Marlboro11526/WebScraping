import scrapy

class MacysSpider(scrapy.Spider):
    name = 'macys_spider'
    allowed_domains = ['macys.com']
    start_urls = ['https://www.macys.com/']


    def parse(self, response):
        navigationFobs =response.css('#mainNavigation #mainNavigationFobs a::attr(href)').getall()
        print(navigationFobs)
        for navigationFob in navigationFobs:
            print("navigationFob", navigationFob)
            yield scrapy.Request(response.urljoin("https://www.macys.com/" + navigationFob), callback=self.parse_nabigationFob)
        
    def parse_nabigationFob(self, response):
        categories = response.css('.categoryHeader .accordion-category-tree a::attr(href)').getall()
        print(categories)
        for category in categories:
            print("catagory", category)
            yield scrapy.Request(response.urljoin(category), callback=self.parse_category)
    

    def parse_category(self, response):
        items = response.css('.productThumbnail')
        for item in items:
            product_id = item.attrib["id"]
            product_brand = item.css('.productBrand::text').get().strip().replace('\t', '').replace('\n', '').replace('\r', '').replace('  ', '')
            product_title = item.css('div.productDescription a::attr(title)').get()
            product_link = "https://www.macys.com" + item.css("a::attr(href)").extract()[0]
            regular = item.css('.prices > div:nth-child(1) > span:nth-child(1)::text').getall()
            clean_regular = [d.strip() for d in regular if d.strip()]
            product_regular_price = clean_regular[0]
            discount = item.css('.prices > div:nth-child(2) > span:nth-child(1)::text').getall()
            if len(discount) == 2:
                product_discount_price = discount[1].strip()
            else:
                product_discount_price = "none"
            yield {
                "product_id": product_id,
                "product_brand" : product_brand,
                "product_title" : product_title,
                "product_link" : product_link,
                "product_regular_price" : product_regular_price,
                "product_discount_price" : product_discount_price
            }

        # Follow links to the next page
        next_page_url = response.css('.pagination .pagination-next a::attr(href)').get()
        print(next_page_url)
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
