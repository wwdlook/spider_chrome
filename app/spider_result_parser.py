# -*- coding: utf-8 -*-

import re
import os
import json
import pandas as pd


DATA_DIR = os.path.abspath('../data')


def common_parser1(data):
    """
    list of string
    :param data:
    :return:
    """
    data = '::\n'.join(data)
    data = re.sub('：', ':', data)
    data = re.sub('（', '(', data)
    data = re.sub('）', ')', data)
    data = re.sub('\-', '', data)
    data = re.sub('至', '', data)
    hanzi_num = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    hanzi_num = zip(hanzi_num, list(range(1, 11)))
    for i, j in hanzi_num:
        data = re.sub(i, str(j), data)
    data = re.sub('\([^\(\)]+\)', '', data)
    data = re.sub('\(|\)|\&', '', data)
    data = re.sub('[0-9a-zA-Z]+[^:]+', '', data)
    data = re.sub('[0-9a-zA-Z]', '', data)
    data = re.sub(' |；|、|，', ',', data)
    data = re.sub(',+[^:]+', '', data)
    data = re.sub(',+', '', data)
    data = re.sub('自编[^:]+', '', data)
    hanzi_post = ['商业', '住宅', '公建', '办公', '商业楼', '地下室', '办公楼工程', '社区服务中心', '商业住宅', '自编']
    for i in hanzi_post:
        data = re.sub(i+':', ':', data)
    district_post = ['市', '区', '乡', '县', '镇', '路', '道', '社区', '省']
    for i in district_post:
        print('[^:]{,3}'+i)
        data = re.sub('[^:]{,3}'+i, '', data)
    # d = re.sub(u'[^\u4e00-\u9fa5\n]+', ' ', d)

    data = data.split('::\n')
    return data


def common_parser2(data):
    data = [i.split('::') for i in data]
    project_set = set()
    for i in data:
        for j in i:
            j = j.strip()
            if len(j) <= 2:
                continue
            if j.startswith(':'):
                j = j[1:]
            if j.endswith('.'):
                j = j[:-1]
            if j.endswith('路'):
                continue
            project_set.add(j)
    project_set = list(project_set)
    return project_set


def common_parser3(data):
    data = '::\n'.join(data)
    data = re.sub('：', ':', data)
    data = re.sub('（', '(', data)
    data = re.sub('）', ')', data)
    data = re.sub('[0-9a-zA-Z\-]+(单元|地块|区域地块)', '', data)
    # data = re.sub('至', '', data)
    data = re.sub('\([^\(\)]+\)', '', data)
    data = data.split('::\n')
    return data


def parser(fp):
    data = pd.read_csv(os.path.join(DATA_DIR, fp))
    project_ls = data['project_names'].tolist()
    project_ls = common_parser1(project_ls)
    project_ls = [i.split('::') for i in project_ls]
    project_set = set()
    for i in project_ls:
        for j in i:
            if len(j) <= 2:
                continue
            if j.startswith(':'):
                j = j[1:]
            if j.endswith('.'):
                j = j[:-1]
            if j.endswith('路'):
                continue
            project_set.add(j)
    project_set = list(project_set)
    if '' in project_set:
        project_set.remove('')
    project_set = '\n'.join(project_set)
    with open(os.path.join(DATA_DIR, 'project_names.txt'), 'w') as f:
        # f.write(json.dumps(project_set, ensure_ascii=False, indent=4))
        f.write(project_set)
    pass


def parser2(fp=None):
    with open('/Users/wwd/PycharmProjects/shidai/project/data/org_names_parsed.json', 'r') as f:
        keywords = json.load(f)
    waiting_projects = keywords['LOC']
    waiting_projects = ['::'.join(waiting_projects)]
    waiting_projects = common_parser1(waiting_projects)
    waiting_projects = common_parser2(waiting_projects)
    waiting_projects = '\n'.join(waiting_projects)
    with open(os.path.join(DATA_DIR, 'project_names1.txt'), 'w') as f:
        # f.write(json.dumps(project_set, ensure_ascii=False, indent=4))
        f.write(waiting_projects)
    pass


def add_stop_words(fp, col):
    if fp.endswith('.csv'):
        col_df = pd.read_csv(fp, nrows=1)
    elif fp.endswith('.xlsx'):
        col_df = pd.read_excel(fp, nrows=1)
    assert col in col_df.columns
    if fp.endswith('.csv'):
        data = pd.read_csv(fp, use_cols=col)
    elif fp.endswith('.xlsx'):
        data = pd.read_excel(fp, use_cols=col)
    print(data.shape)
    data = list(data[col])
    res = {'stop_words': list(set(data))}

    json.dump(res,
        open(os.path.join(DATA_DIR, 'stop_words.json'), 'w'), ensure_ascii=False)


def json_parser(fp, key_names):
    if os.path.exists(os.path.join(DATA_DIR, 'stop_words.json')):
        pass
    else:
        add_stop_words('/Users/wwd/PycharmProjects/shidai/project/data/shidai201811.xlsx', '企业标签')
    with open(os.path.join(DATA_DIR, 'stop_words.json'), 'r') as f:
        stop_words = json.load(f)
    stop_words = stop_words['stop_words']
    with open(fp, 'r') as f:
        keywords = json.load(f)
    for keyname in key_names:
        if len(keywords.get(keyname, [])) > 0:
            res = common_parser3(keywords[keyname])
            res = '::'.join(res)
            res = res.split('::')
            project_set = set()
            for j in res:
                if len(j) <= 2:
                    continue
                if j.startswith(':'):
                    j = j[1:]
                if j.endswith('.'):
                    j = j[:-1]
                if j.endswith('路'):
                    continue
                project_set.add(j)
            res = project_set - set(stop_words)
            res = list(res)
            res = filter(lambda x: x != '', res)
            res = map(lambda x: x+'\n', res)
            # with open(os.path.join(DATA_DIR, 'gz_' + keyname+'.txt'), 'w') as f:
            #     f.writelines(res)
            with open(os.path.join(DATA_DIR, keyname+'.txt'), 'a') as f:
                f.writelines(res)


if __name__ == '__main__':
    # parser2('guangzhouzhufang.csv')
    # ret = common_parser1(['保利世界贸易中心（二期）::恒大山水城146-147号楼（C区）::广园东碧桂园凤凰城凤林苑二期住宅::锦绣御品名苑29-41栋、43-47栋、49-51栋::南沙碧桂园倚荔轩倚荔街7、8、9、10号::保利城花园::恒大山水城(D区)::祈福花园(花明径2、4、6、8、10、12号)::映翠苑::德福河畔花园::信业花园A区::嘉日雅居::新光城市花园二期一街至四街::映翠苑::锦绣半岛银湾西区商铺3'])
    json_parser('/Users/wwd/PycharmProjects/spider_chrome/data/loupan.json', ['loupan_ls'])
    pass
