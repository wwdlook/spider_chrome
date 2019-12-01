# coding=utf-8

import json
from Handlers.base_handler import BaseHandler


class Handler(BaseHandler):

    def set_params(self, project_name=None):
        if project_name is None:
            pass
        else:
            self.result.update({'project_name': project_name})

    def on_start(self, start_urls):
        for start_url in start_urls:
            self.get(start_url, url_pattern=start_url+"all/p%d/", callback='index_page')

    def index_page(self, url_pattern, mode=1, **kwargs):
        if mode == 1:
            for index in range(1, 26):
                if index == 1:
                    self.get('', callback='detail_page')
                else:
                    self.get(url_pattern % index, callback='detail_page')

    def detail_page(self):
        try:
            loupan_ret = self.result.get('loupan_ls', [])
            eles = self.browser.find_elements_by_css_selector(
                    '#container > div.list-contents > div.list-results > div.key-list.imglazyload > div > div > a.lp-name > h3 > span')
            loupan_ls = [ele.text for ele in eles]
            loupan_ret.append('::'.join(loupan_ls))
            self.result.update(
                {
                    "loupan_ls": loupan_ret
                }
            )
        except Exception as e:
            print(str(e))
            error_ret = self.result.get('error_ls', [])
            error_ret.append(str(e)+'\nurl: {}\n'.format(self.browser.current_url))

    def pipeline(self):
        self.save_result(fname='anjuke_new')

    def main(self):
        self.set_params(project_name='loupan')
        with open("/Users/wwd/PycharmProjects/spider_chrome/data/anjuke_city.json", 'r') as f:
            city_dict = json.load(f)
        city_ls = city_dict["city_ls"]
        del city_dict
        self.on_start(city_ls)
        self.pipeline()
        self.browser.close()


if __name__ == '__main__':
    Hd = Handler()
    # Hd.get('http://news.hexun.com/2018-11-29/195364164.html')
    pass
