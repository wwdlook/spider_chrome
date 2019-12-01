# coding=utf-8

from Handlers.base_handler import BaseHandler


class Handler(BaseHandler):

    def set_params(self, project_name=None):
        if project_name is None:
            pass
        else:
            self.result.update({'project_name': project_name})

    def on_start(self, start_urls):
        for start_url in start_urls:
            self.get(start_url, callback='index_page')

    def index_page(self):
        eles = self.browser.find_elements_by_css_selector(
                "body > div.content > div > div.letter_city > ul > li > div.city_list > a"
        )
        urls = [ele.get_attribute('href') for ele in eles]
        for url in urls:
            self.get(url, callback='detail_page')

    def detail_page(self):
        city_ret = self.result.get('city_ls', [])
        eles = self.browser.find_elements_by_css_selector(
                "#glbNavigation > div > ul > li:nth-child(2) > a"
        )
        city_ls = [ele.get_attribute('href') for ele in eles]
        city_ret.extend(city_ls)
        self.result.update(
            {
                "city_ls": city_ret
            }
        )

    def pipeline(self):
        self.save_result(fname='city')

    def main(self):
        self.set_params(project_name='anjuke')
        self.on_start(['https://www.anjuke.com/sy-city.html'
                       ])
        self.pipeline()
        self.browser.close()


if __name__ == '__main__':
    Hd = Handler()
    Hd.main()
    # Hd.get('http://news.hexun.com/2018-11-29/195364164.html')
    pass
