from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def extract0(selector):
    """
    从选择器中提取第一个元素
    """
    if selector and len(selector)>=1:
        if type(selector) == type([]):
            return selector[0]
        else:
            from scrapy.selector.unified import SelectorList
            if isinstance(selector, SelectorList):
                return extract0(selector.extract())
    return ''

def get_attribute_from_url(url, attri_name):
    """
    从url中获取对应的参数值
    """
    url_obj = urlparse(url)
    query = parse_qs(url_obj.query)
    # print(query)
    if attri_name in query.keys():
        value = query[attri_name]
        if type(value) == type([]) and len(value) == 1:
            return value[0]
        return value
    return None

def get_simple_url(url, attris):
    """
    将url中不存在于attris中的参数过滤掉，返回新的url
    """
    url_obj = urlparse(url)
    query = parse_qs(url_obj.query)
    if type(attris) == type(''):
        attris = [attris]
    # for attri_name in query.keys():
    tmp_keys = list(query.keys())
    for i in range(len(query)):
        attri_name = tmp_keys[i]
        if attri_name not in attris:
            query.pop(attri_name)
    query = urlencode(query, doseq=True)
    # print(query)
    simple_url = str(urlunparse((url_obj.scheme, url_obj.netloc, url_obj.path, url_obj.params, query, url_obj.fragment)))
    return simple_url

def rebuild_url_query(url, query):
    """
    从新构建url的查询字符串,query以字典形式提供
    """
    query_str = urlencode(query)
    url_obj = urlparse(url)
    new_url = urlunparse((url_obj.scheme, url_obj.netloc, url_obj.path, url_obj.params, query_str, url_obj.fragment))
    return new_url
