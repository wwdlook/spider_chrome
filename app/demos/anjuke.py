# coding=utf-8

from app.Handlers.base_handler import BaseHandler


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

    def pipeline(self):
        self.save_result(fname='try')

    def main(self):
        self.set_params(project_name='loupan')
        self.on_start(['https://sz.fang.anjuke.com/loupan/',
                       'https://sh.fang.anjuke.com/loupan/',
                       'https://bj.fang.anjuke.com/loupan/'])
        self.pipeline()
        self.browser.close()


if __name__ == '__main__':
    Hd = Handler()
    Hd.main()
    pass
