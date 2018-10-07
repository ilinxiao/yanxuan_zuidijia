import scrapy

class CategoryItem(scrapy.Item):
    category_id = scrapy.Field()
    parent_id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()

# class SubCategoryItem(CategoryItem):