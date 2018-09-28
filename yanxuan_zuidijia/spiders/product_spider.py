import scrapy
from scrapy_splash import SplashRequest

class ProductSpider(scrapy.Spider):

    name = 'product'
    allowed_domains = ['you.163.com']
    start_urls = [
        "http://you.163.com/item/list?categoryId=1008000"
    ]
    
    def start_request(self):
        splash_args = {
            'wait':0.9,
        }
        for url in start_urls:
            yield SplashRequest(url, self.parse_result, endpoint='render.html', args=splash_args)
    
    def parse_result(self, response):
        goods_area = response.css('#j-goodsAreaWrap').extract()
        print(goods_area)
        m_content = response.css('.m-content')
        print('内容数量:%d' % len(m_content))