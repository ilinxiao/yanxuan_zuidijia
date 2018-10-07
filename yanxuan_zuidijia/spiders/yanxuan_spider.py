import scrapy
from scrapy import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from urllib.parse import urlunparse
from scrapy.contrib.linkextractors import LinkExtractor
from yanxuan_zuidijia.category_item import CategoryItem
from yanxuan_zuidijia.product_item import ProductItem

import yanxuan_zuidijia.tool
from yanxuan_zuidijia.tool import extract0, get_attribute_from_url, get_simple_url, rebuild_url_query
import json

class YanxuanSpider(CrawlSpider):

    name = 'yanxuan'
    allowed_domains = ['you.163.com']
    start_urls = [
        "http://you.163.com"
    ]
    # rules = [Rule(LinkExtractor(allow=['\?categoryId='], deny=['&subCategoryId=']), callback='parse_category')]
    
    def start_request(self):
        for url in start_urls:
            yield Request(url, self.parse)
    
    def parse(self, response):
        for category  in self.get_category(response):
            cate_item = CategoryItem()
            cate_item['category_id'] = category[0]
            cate_item['url'] = category[1]
            cate_item['name'] = category[2]
            cate_item['desc'] = category[2]
            cate_item['parent_id'] = 0

            #yield category item
            yield cate_item

            url = category[1]
            #yield category request
            yield Request(url, callback=self.parse_product)
        
        
    def parse_product(self, response):
        
        try:
            request_url = response.url
            parent_category_id = get_attribute_from_url(request_url, 'categoryId')
            sub_category = response.css('.m-content .m-Level2Category')
            for sub_div in sub_category:
                sub_category_id = extract0(sub_div.xpath('@id'))
                # sub_category_id = extract0(sub_div.css('id'))
                self.log('id:%s' % sub_category_id)
                sub_category_name = extract0(sub_div.css('.hd .title .name::text'))
                self.log('sub category name:%s' % sub_category_name)
                sub_category_desc = extract0(sub_div.css('.hd .desc::text'))
                self.log('sub category description:%s' % sub_category_desc)
                sub_category_url = rebuild_url_query(request_url, 
                    {'categoryId': parent_category_id, 'subCategoryId': sub_category_id})
                """
                子分类
                """
                sub_category = CategoryItem()
                sub_category['category_id'] = sub_category_id
                sub_category['url'] = sub_category_url
                sub_category['name'] = sub_category_name
                sub_category['desc'] = sub_category_desc
                sub_category['parent_id'] = parent_category_id
                yield sub_category

                item_list = sub_div.css('.m-itemList-level2Category .item')
                product_img_url = ''
                product_url = ''
                product_tag = ''        
                product_name = ''
                product_id = ''
                product_simple_desc = ''
                product_category_id = ''
                product_current_price = ''
                product_original_price = ''

                for item in item_list:
                    product_div = item.css('.m-product')
                    #img url
                    hd_div = product_div.css('.hd')
                    img = hd_div.css('img')
                    product_img_url = extract0(img.xpath('@src'))
                    
                    bd_div = product_div.css('.bd')
                    #name
                    link = bd_div.xpath('h4[@class="name"]/a')
                    # product_name = bd_div.xpath('h4[@class=\'name\']//text()')
                    product_name = extract0(link.xpath('@title'))
                    self.log('name:%s' % product_name)
                    #print(link.xpath('@href').extract())
                    data_yxstat = extract0(link.xpath('@data-yxstat'))
                    data= json.loads(data_yxstat)
                    # print(data['parameters']['itemId'])
                    #id 
                    product_id = data['parameters']['itemId']
                    #category
                    product_category_id = data['parameters']['categoryId']
                    #url
                    product_url = data['topage']

                    #current price
                    price_p = bd_div.xpath('p[@class="price"]/span')
                    product_current_price = extract0(price_p[0].xpath('span[2]//text()'))
                    #original price
                    ori_price = bd_div.xpath('p[@class="price"]/span[@class="counterPrice"]')
                    if ori_price:
                        product_original_price = extract0(ori_price.xpath('span[2]//text()'))
                    self.log('current price:%s\toriginal price:%s' % (product_current_price, product_original_price))
                    #simple desc
                    desc_p = bd_div.css('p.desc')
                    product_simple_desc = extract0(desc_p.css('::text'))
                    self.log('simple desc:%s' % product_simple_desc)

                    """
                    商品信息
                    """
                    product_item = ProductItem()
                    product_item['id'] = product_id
                    product_item['category_id'] = product_category_id 
                    product_item['url'] = product_url
                    product_item['original_price'] = product_original_price
                    product_item['current_price']  = product_current_price
                    product_item['tag'] = ''
                    product_item['simple_desc'] = product_simple_desc
                    product_item['img_url'] = product_img_url
                    yield product_item

        except Exception as e:
            self.log(e, loglevel=scrapy.log.ERROR)

    def get_category(self, response):
        """
        获取商品主分类
        筛选规则：链接地址中是否仅包含categoryId
        """
        try:
            category_links = response.css('.yx-cp-m-tabNav > li > a')
            category_list = []
            for a in category_links:
                name = extract0(a.xpath('text()'))
                href = extract0(a.xpath('@href'))
                if href and name:
                    category_id = get_attribute_from_url(href, 'categoryId')
                    sub_category_id = get_attribute_from_url(href, 'subCategoryId')
                    if category_id and sub_category_id is None:
                        simple_url = get_simple_url(href, 'categoryId')
                        yield category_id, simple_url, name
        except Exception as e:
            self.log(e, loglevel=scrapy.log.ERROR)