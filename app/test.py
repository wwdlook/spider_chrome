# coding=utf-8

import pandas as pd
from selenium import webdriver
import time


def count_line(fp):
    d = pd.read_csv(fp)
    print(d.shape)


def test():
    driver = webdriver.Chrome()
    driver.get("https://bj.fang.anjuke.com/loupan/")
    time.sleep(1)
    ele = driver.find_element_by_css_selector(
        "#container > div.list-contents > div.list-results > div.list-page > span > em"
    )
    _ = 1


if __name__ == '__main__':
    test()
    # #container > div.list-contents > div.list-results > div.key-list.imglazyload > div:nth-child(1) > div > a.lp-name > h3 > span
    # container > div.list-contents > div.list-results > div.key-list.imglazyload > div:nth-child(60) > div > a.lp-name > h3 > span
    pass
