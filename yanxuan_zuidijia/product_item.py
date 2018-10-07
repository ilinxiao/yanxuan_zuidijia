import scrapy

class ProductItem(scrapy.Item):
    id = scrapy.Field()
    category_id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    img_url = scrapy.Field()
    original_price = scrapy.Field()
    current_price = scrapy.Field()
    tag = scrapy.Field()    
    simple_desc = scrapy.Field()
    #ÏúÊÛ×´Ì¬
    empty = scrapy.Field()