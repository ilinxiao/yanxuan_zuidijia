import scrapy

class ProductItem(scrapy.Item):
    category_id = scrapy.Field()
    category_name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()