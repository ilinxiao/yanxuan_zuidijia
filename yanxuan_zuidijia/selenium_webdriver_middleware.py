from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
from logging import getLogger
from selenium.webdriver.chrome.service import Service
import subprocess, os

from scrapy.exceptions import NotConfigured
from scrapy import signals

from urllib.parse import urlparse, parse_qs, urlunparse
from yanxuan_zuidijia.selenium_request import SeleniumRequest
from importlib import import_module

class SeleniumMiddleware(object):
    
    def __init__(self, driver_name, driver_excutable_path, driver_arguments):
        """初始化selenium webdriver
        参数：
        --------
        driver_name : str
            哪个selenium webdriver被使用
        driver_excutable_path: str
            webdriver执行路径
        driver_arguments: list
            初始化webdriver的参数列表
        """
        self.logger = getLogger(__name__)
        
        #根据driver_name加载不同的selenium模块
        selenium_base_class_name = 'selenium.webdriver.{}'.format(driver_name)
        
        #WebDriver实例类
        driver_module = import_module('{}.webdriver'.format(selenium_base_class_name))
        driver_class = getattr(driver_module, 'WebDriver')
        
        #Options实例类
        driver_options_module = import_module('{}.options'.format(selenium_base_class_name))
        driver_options_class = getattr(driver_options_module, 'Options')
        
        #添加选项
        driver_options = driver_options_class()
        for option in driver_arguments:
            driver_options.add_argument(option)
        
        driver_args = {
            'executable_path': driver_excutable_path,
            '{}_options'.format(driver_name): driver_options
        }
        self.browser = driver_class(**driver_args)

    def process_request(self, request, spider):
        """
        用chromedriver --headless抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        self.logger.debug(type(spider))
        self.logger.debug('Request Url:%s' % request.url)
        self.logger.debug('Webdriver is Starting')
        # self.logger.debug('Request type:%s' % type(request))
        if not isinstance(request, SeleniumRequest):
            self.logger.error('NOT SELENIUM REQUEST.')
            return None
            
        # page = request.meta.get('page', 1)
        try:
            self.browser.get(request.url)
            
            if request.wait_time:
                wait = WebDriverWait(self.browser, request.wait_time)
                if request.wait_until:
                    wait.until(request.wait_until)
            
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)
        except TimeoutException:
            self.logger.debug('some error:%s' % request.url)
            return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        """ Initialize the middleware with the crawler settings """
        
        driver_name = crawler.settings.get('SELENIUM_DRIVER_NAME')
        driver_excutable_path = crawler.settings.get('SELENIUM_DRIVER_EXCUTABLE_PATH')
        driver_arguments = crawler.settings.get('SELENIUM_DRIVER_ARGUMENTS')
        
        if not driver_name or not driver_excutable_path:
            raise NotConfigured(
                'SELENIUM_DRIVER_NAME和SELENIUM_DRIVER_EXCUTABLE_PATH必须配置。'
            )
            
        middleware = cls(
            driver_name=driver_name,
            driver_excutable_path=driver_excutable_path,
            driver_arguments=driver_arguments
        )
                                    
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware
        
    def spider_closed(self):
        #退出webdriver
        self.browser.quit()