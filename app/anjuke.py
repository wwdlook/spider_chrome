# coding=utf-8

import json
from tqdm import tqdm
from Handlers.base_handler import BaseHandler


class Handler(BaseHandler):

    def set_params(self, project_name=None):
        if project_name is None:
            pass
        else:
            self.result.update({'project_name': project_name})

    def on_start(self, start_urls):
        with tqdm(total=len(start_urls)) as pbar:
            for start_url in start_urls:
                self.get(start_url, url_pattern=start_url+"loupan/all/p%d/", callback='index_page')
                pbar.update(1)
                self.pipeline()

    def index_page(self, url_pattern, mode=1, **kwargs):
        if mode == 1:
            self.get(url_pattern % 1, callback='detail_page')
            n = 1
            n_page = 1
            while True:
                try:
                    n_items = self.browser.find_element_by_css_selector(
                        "#container > div.list-contents > div.list-results > div.list-page > span > em"
                    ).text
                    break
                except:
                    if n == 5:
                        break
                    self.get(url_pattern % 1, time_interval=(n, n+1))
                    n += 1
            try:
                n_items = eval(n_items)
                n_page = n_items // 60 + min(1, n_items % 60)
            except:
                pass
            if n_page > 1:
                with tqdm(total=n_page) as pbar:
                    for index in range(2, n_page+1):
                        pbar.update(1)
                        self.get(url_pattern % index, callback='detail_page')
                    pbar.update(1)

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
        self.save_result(fname='anjuke_new1')

    def main(self):
        self.set_params(project_name='loupan')
        with open("/Users/wwd/PycharmProjects/spider_chrome/data/anjuke_city.json", 'r') as f:
            city_dict = json.load(f)
        city_ls = city_dict["city_ls"]
        del city_dict
        with open("/Users/wwd/PycharmProjects/spider_chrome/data/loupan_anjuke_new.json", 'r') as f:
            res = json.load(f)
        self.result.update(res)
        del res
        self.on_start(city_ls[16:])
        self.pipeline()
        self.browser.close()


if __name__ == '__main__':
    Hd = Handler()
    Hd.main()
    # Hd.get('http://news.hexun.com/2018-11-29/195364164.html')
    pass
