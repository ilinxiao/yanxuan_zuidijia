import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from urllib.parse import urlparse, parse_qs, urlunparse
from scrapy.contrib.linkextractors import LinkExtractor

class ProductSpider(scrapy.Spider):

    name = 'category'
    allowed_domains = ['you.163.com']
    start_urls = [
        "http://you.163.com"
    ]
    
    def start_request(self):
        for url in start_urls:
            yield Request(url, self.parse)
    
    def parse(self, response):
    
        category = self.get_category(response)

        print('分类数目:%d' % len(category))

    def get_category(self, response):
        """
        获取商品分类
        筛选分类规则：看分类的链接地址中是否包含categoryId
        return: category_list: [
            {id:xxx, name:'name', url:'url'}
            ...
        ]
        """
        # //*[@id="j-yx-cp-m-top"]/div[2]/div/ul
        #j-yx-cp-m-top > div.yx-cp-m-funcTab.j-yx-cp-m-funcTab > div > ul
        category = response.css('.yx-cp-m-tabNav > li > a')
        category_list = []
        for a in category:
            # print('text:%s' % a.xpath('@title').extract()[0])
            text_list = a.xpath('text()').extract()
            href_list = a.xpath('@href').extract()
            text = ''
            href = ''
            if text_list:
                text = text_list[0]
                # print('text:%s' % text)
            if href_list:
                href = href_list[0]
                # print('href:%s' % href)
            
            cate_obj = {}
            if href:
                # print('目标分类.')
                url = urlparse(href)
                query = parse_qs(url.query)
                if 'categoryId' in query.keys():
                    if text:
                        cate_obj['name'] = text
                    id = parse_qs(url.query)['categoryId'][0]
                    q='categoryId={}'.format(id)
                    simple_url = urlunparse((url.scheme, url.netloc, url.path, url.params, q,''))
                    
                    cate_obj['id'] = id
                    cate_obj['url'] = str(simple_url)
                    category_list.append(cate_obj)
        
        return category_list