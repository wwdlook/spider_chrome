# coding=utf-8

import os
import sys
import json
import time
import random
from selenium import webdriver
# from app.common.utils import callback


class BaseHandler(object):
    def __init__(self, result_dir='../data'):
        assert os.path.exists(os.path.abspath(result_dir))
        self.browser = webdriver.Chrome()
        self.start_url = ''
        self.keyword ='验证码'
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
                break
            else:
                tmptime = time.time()
                if tmptime - stime > 10:
                    print('TIME OUT, PLEASE RETRY !')
                    break

    def get(self, url, **kwargs):
        """
        self.browser.get(url)
        :param url:
        :param kwargs: callback: give the next parser
        :return: the next parser
        """
        if kwargs.get('callback'):
            callback = kwargs['callback']
            if isinstance(callback, str) and hasattr(self, callback):
                func = getattr(self, callback)
            elif hasattr(callback, 'im_self') and callback.im_self is self:
                func = callback
            kwargs.pop('callback')
        else:
            self.browser.close()
            print('Please set the next parser function !')
            self.save_result('temp_result')
            sys.exit()

        if url != '':
            flag = True
            while flag:
                try:
                    self.browser.get(url)
                    assert url == self.browser.current_url
                    flag = False
                except:
                    self.manual_verification(url)
            time.sleep(random.uniform(0.5, 2))

        return func(**kwargs)

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
