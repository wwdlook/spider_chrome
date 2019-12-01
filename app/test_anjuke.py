#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-10-28 10:28:08
# Project: anjuke_shidai_yulun

import re
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {

        'headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/77.0.3865.120 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive'
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        candi_url_lst = [
            'https://sh.fang.anjuke.com/loupan/'
        ]
        for candi_url in candi_url_lst:
            self.crawl(candi_url, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.search(r'https://[a-z]{2,12}\.fang\.anjuke\.com/loupan/\d{3,8}\.html', each.attr.href):
                m = re.search(
                    r'(?<=/loupan/)\d{3,8}(?=\.html)', each.attr.href)
                loupan_id = m.group(0)
                m = re.search(
                    r'(?<=https://)[a-z]{2,12}(?=\.fang\.anjuke\.com)', each.attr.href)
                province = m.group(0)
                comment_url = 'https://%s.fang.anjuke.com/loupan/dianping-%s.html' % (
                    province, loupan_id)
                print comment_url
                self.crawl(comment_url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):

        return {
            "url": response.url,
        }
