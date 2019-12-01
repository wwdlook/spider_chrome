# coding=utf-8

from Handlers.base_handler import BaseHandler
from tqdm import tqdm
import re


class Handler(BaseHandler):

    def set_params(self, project_name=None):
        if project_name is None:
            pass
        else:
            self.result.update({'project_name': project_name})

    def on_start(self, start_urls):
        for start_url in start_urls:
            self.get(start_url,  url_pattern=start_url+"all/p%d/", callback='index_page1')

    def index_page1(self, url_pattern):

        self.get(url_pattern % 1, callback='index_page2', time_interval=(5, 6))
        n_page = 29
        try:
            n_items = self.browser.find_element_by_css_selector(
                "#container > div.list-contents > div.list-results > div.list-page > span > em"
            )
        except:
            pass
        try:
            n_items = eval(n_items[0].text)
            n_page = n_items // 60 + min(1, n_items % 60)
        except:
            pass
        print("n_page: %d" % n_page)
        if n_page > 1:
            with tqdm(total=n_page) as pbar:
                for index in range(2, n_page + 1):
                    pbar.update(1)
                    self.get(url_pattern % index, callback='index_page2')
                pbar.update(1)

    def index_page2(self):
        loupan_ret = self.result.get('loupan_ls', [])
        eles = self.browser.find_elements_by_css_selector(
            "#container > div.list-contents > div.list-results > div.key-list.imglazyload > div > div > a.lp-name"
        )
        urls = [ele.get_attribute('href') for ele in eles]
        loupan_ids = []
        for ele in urls:
            try:
                loupan_ids.append(re.findall("[0-9]{6}", ele)[0])
            except:
                pass
        loupan_ret.extend(loupan_ids)
        self.result.update(
            {
                "loupan_ls": loupan_ret
            }
        )
        with tqdm(total=len(loupan_ids)) as pbar:
            for id in loupan_ids:
                dianping_url = "https://sh.fang.anjuke.com/loupan/dianping-%s.htmls/" % id
                self.get(dianping_url, callback='detail_page', time_interval=(1.5, 2))
                try:
                    n_items = self.browser.find_element_by_css_selector(
                        "#container > div.ugc-content.clearfix > div.ugc-mod > div.rev-pagination > div.pagi-title"
                    ).text
                except:
                    pass
                try:
                    n_items = re.findall("共有&nbsp;([0-9]{1,3})条", n_items)[0]
                    n_items = eval(n_items)
                    n_page = n_items // 30 + min(1, n_items % 30)
                except:
                    n_page = 1
                    if n_page > 1:
                        for index in range(2, n_page + 1):
                            self.get(dianping_url+'?p=%d' % index, callback='detail_page')
                pbar.update(1)
                self.save_result(fname='pinglun')

    def detail_page(self):
        pinglun_ret = self.result.get('pinglun', [])
        eles = self.browser.find_elements_by_css_selector(
            "#j-total-wrap > ul > li > div.clearfix > div.info-mod > h4.rev-subtit.part-text"
        )
        pinglun_ls = [ele.text for ele in eles]
        pinglun_ret.append('::'.join(pinglun_ls))
        self.result.update(
            {
                "pinglun": pinglun_ret
            }
        )

    def pipeline(self):
        self.save_result(fname='pinglun')

    def main(self):
        self.set_params(project_name='anjuke')
        self.on_start(['https://sh.fang.anjuke.com/loupan/'
                       ])
        # "https://sh.fang.anjuke.com/loupan/dianping-455873.htmls/?p=2"
        # "#container > div.ugc-content.clearfix > div.ugc-mod > div.rev-pagination > div.pagi-title"
        # "#j-total-wrap > ul > li:nth-child(30)"
        # "#j-total-wrap > ul > li:nth-child(1)"
        self.pipeline()
        self.browser.close()


if __name__ == '__main__':
    Hd = Handler()
    Hd.main()
    # Hd.get('http://news.hexun.com/2018-11-29/195364164.html')
    pass
