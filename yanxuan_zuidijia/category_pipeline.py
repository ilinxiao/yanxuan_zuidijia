
class CategoryPipeline(object):
        
    def process_item(self, item, spider):
        """ 根据item的类别 动态启用spider.settings设置ITEM_PIPEPINES """
        print("spider methods and attributes:\n%s" % dir(spider))