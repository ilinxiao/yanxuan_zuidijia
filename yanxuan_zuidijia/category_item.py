import scrapy

class CategoryItem(scrapy.Item):
    category_id = scrapy.Field()
    category_name = scrapy.Field()
    category_url = scrapy.Field()