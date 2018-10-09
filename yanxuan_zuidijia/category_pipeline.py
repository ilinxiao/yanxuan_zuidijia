
class CategoryPipeline(object):
        
    def process_item(self, item, spider):
        print("spider methods and attributes:\n%s" % dir(spider))