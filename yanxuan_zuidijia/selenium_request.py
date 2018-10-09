"""
代码参考自https://github.com/clemfromspace/scrapy-selenium/
通过往请求中添加自定义参数，解决不同的地址等待不同的加载时间和等待条件
"""
from scrapy import Request


class SeleniumRequest(Request):
    """Scrapy ``Request`` subclass providing additional arguments"""

    def __init__(self, wait_time=None, wait_until=None, screenshot=False, *args, **kwargs):
        """Initialize a new selenium request
        Parameters
        ----------
        wait_time: int
            The number of seconds to wait.
        wait_until: method
            One of the "selenium.webdriver.support.expected_conditions". The response
            will be returned until the given condition is fulfilled.
        screenshot: bool
            If True, a screenshot of the page will be taken and the data of the screenshot
            will be returned in the response "meta" attribute.
        """
        self.wait_time = wait_time
        self.wait_until = wait_until
        self.screenshot = screenshot

        super().__init__(*args, **kwargs)