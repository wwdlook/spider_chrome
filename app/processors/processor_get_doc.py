# coding=utf-8

import traceback
import time
import newspaper as npp
from selenium import webdriver
from processors.processors import ProcessorBase


class ProcessorGetDoc(ProcessorBase):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def process(self, url, time_out=5):
        """
        request url by GET method and then get doc content,
        if find 404 Client Error then return '404 Client Error'
        if page' loading time exceed 10 seconds then return 'TIME OUT, url: url'
        :param url:
        :param time_out: int(default=5)
        :return: str
        """
        assert type(url) is str
        a = npp.Article(url, language='zh')
        a.download()
        try:
            a.parse()
        except Exception as e:
            if '404 Client Error' in str(e):
                return str(e)
            self.driver.get(url)
            time.sleep(0.01)
            last_page = self.driver.page_source
            time.sleep(0.1)
            time0 = time.time()
            while self.driver.page_source != last_page:
                if time.time() - time0 > time_out:
                    return 'TIME OUT, url: %s' % url
                time.sleep(0.5)
                last_page = self.driver.page_source

            a = npp.Article(self.driver.current_url, language='zh')
            a.download(input_html=self.driver.page_source)
            a.parse()
        return a.text

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    # P = ProcessorGetDoc()
    # a = P.process("http://stock.10jqka.com.cn/20181126/c608352490.shtml")
    # print(a)
    pass
