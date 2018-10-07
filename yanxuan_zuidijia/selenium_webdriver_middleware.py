from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
from selenium.webdriver.chrome.service import Service
import subprocess, os
from scrapy import signals

from urllib.parse import urlparse, parse_qs, urlunparse

class SeleniumMiddleware(object):
    
    # c_service = Service(webdriver_path)
    # c_service.command_line_args()
    # c_service.start()
    # global driver
    # driver = None
    def __init__(self, timeout=None, options=[], webdriver_path=''):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        

        chrome_options = Options()
        for option in options:
            chrome_options.add_argument(option)

        self.browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=webdriver_path)
        # driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=webdriver_path)
        # self.browser = driver
        # self.browser.set_window_size(1400, 700)
        # self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        pass
        # self.browser.close()
        # global driver
        # driver.quit()
        # self.c_service.stop()
        # 关闭webdriver进程
        # TODO: 改用selenium自己的关闭方式
        # kill_cmd = 'taskkill /F /IM chromedriver.exe'
        # os.system(kill_cmd)
        # status, output = subprocess.getstatusoutput(kill_cmd)
        # if status == 0:
            # self.logger.debug('chromedriver process had killed.')

    def process_request(self, request, spider):
        """
        用chromedriver --headless抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        self.logger.debug('Webdriver is Starting')
        # page = request.meta.get('page', 1)
        try:
            self.browser.get(request.url)
            # self.wait.until(EC.visibility_of_element_located(('css selector', '.m-content')))
            req_url = urlparse(request.url)
            query = parse_qs(req_url.query)
            if request.url == 'http://you.163.com':
                self.wait.until(EC.visibility_of_element_located(('css selector', '.yx-cp-m-tabNav')))
            elif 'categoryId' in query.keys() and 'subCategoryId' not in query.keys():
                self.wait.until(EC.visibility_of_element_located(('css selector', '.m-goodsArea')))
            
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)
        except TimeoutException:
            self.logger.debug('some error:%s' % request.url)
            return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                                    options=crawler.settings.get('CHROME_OPTIONS'),
                                    webdriver_path=crawler.settings.get('WEBDRIVER_PATH'))
                                    
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware
        
    def spider_closed(self):
        #退出webdriver
        self.browser.quit()