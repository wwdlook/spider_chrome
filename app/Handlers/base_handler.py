# coding=utf-8

import os
import sys
import json
import time
import random
import traceback
import newspaper as npp
from selenium import webdriver
# from app.common.utils import callback


class BaseHandler(object):
    def __init__(self, result_dir='../data'):
        print(os.path.abspath(result_dir))
        assert os.path.exists(os.path.abspath(result_dir))
        self.browser = webdriver.Chrome('C:\\Users\\wwdor\\webdriver\\chromedriver.exe')
        self.browser.minimize_window()
        self.start_url = ''
        self.keyword = '验证码'
        self.result_dir = os.path.abspath(result_dir)
        self.result = dict({'project_name': 'DEMO'})
        self.set_params()

    def set_params(self, **kwargs):
        pass

    def manual_verification(self, start_url):
        """
        人工验证功能， 由于仅开启当前一个ChromeDriver暂时无需保存Cookie
        :param start_url: 原请求url
        :return: None
        """
        stime = time.time()
        self.browser.get(start_url)
        time.sleep(1)
        last_page = self.browser.page_source
        last_url = self.browser.current_url
        while self.keyword in last_page:
            time.sleep(1)
            tmp_url = self.browser.current_url
            if tmp_url != last_url:
                print('Verification DONE')
                return True
            else:
                tmptime = time.time()
                if tmptime - stime > 10:
                    print('Verification TIME OUT, PLEASE RETRY !')
                    return False
        return True

    def get(self, url, **kwargs):
        """
        self.browser.get(url)
        :param url:
        :param kwargs: callback: give the next parser
        :return: the next parser
        """
        if "time_interval" in kwargs:
            time_interval = kwargs["time_interval"]
            kwargs.pop("time_interval")
        else:
            time_interval = (0.5, 2.0)

        assert type(time_interval) is tuple
        try:
            time_wait = random.uniform(time_interval[0], time_interval[1])
        except:
            time_wait = random.uniform(0.5, 2)
        if kwargs.get('callback'):
            callback = kwargs['callback']
            if isinstance(callback, str) and hasattr(self, callback):
                func = getattr(self, callback)
            elif hasattr(callback, 'im_self') and callback.im_self is self:
                func = callback
            kwargs.pop('callback')
        else:
            self.browser.get(url)
            time.sleep(time_wait)
            return None
            # sys.exit()

        if url != '':
            flag = True
            while flag:
                try:
                    self.browser.get(url)
                    assert url == self.browser.current_url
                    flag = False
                except:
                    if self.manual_verification(url):
                        break
            time.sleep(time_wait)

        func(**kwargs)

    def get_doc(self, url, time_out=5):
        """
        request url by GET method and then get doc content
        if page's loading time exceeds `time_out`(default=5) seconds then return 'TIME OUT, url: url'
        :param url:
        :param time_out: int(default=5)
        :return: str
        """
        self.get(url)
        last_page = self.browser.page_source
        time.sleep(0.1)
        time0 = time.time()
        while self.browser.page_source != last_page:
            if time.time() - time0 > time_out:
                return 'TIME OUT, url: %s' % url
            time.sleep(0.5)
            last_page = self.browser.page_source

        a = npp.Article(self.browser.current_url, language='zh')
        a.download(input_html=self.browser.page_source)
        a.parse()
        return a.text

    def save_result(self, fname='default_result'):
        """
        to save json_file in data directory
        :param fname: save_file_name
        :return: None
        """
        pre_name = self.result['project_name']
        if len(fname) > 0:
            pre_name += '_'
        json.dump(self.result,
                  open(os.path.join(self.result_dir, pre_name+fname+'.json'), 'w'), ensure_ascii=False)
        return None


if __name__ == '__main__':
    pass
