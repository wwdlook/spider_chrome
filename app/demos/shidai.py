# coding=utf-8

import traceback
import pandas as pd
from tqdm import tqdm
# from app.Handlers.base_handler import BaseHandler
from app.processors.processors import load_processors


def parse(fp, out_fp):
    processors = load_processors()
    assert 'ProcessorGetDoc' in processors
    GetDoc = processors['ProcessorGetDoc']()
    data = pd.read_csv(fp)
    href_ls = data['urls'].tolist()
    doc_ls = data['docs'].tolist()
    for index, url in tqdm(enumerate(href_ls)):
        # html = requests.get(url).content
        # doc_ls[index] = newspaper_process.extract_content_from_html(html)
        if doc_ls[index] != 'None':  # and doc_ls[index] != 'ConnectionError':
            continue
        try:
            doc_ls[index] = GetDoc.process(url)
            # _ = 1
        except Exception as e:
            print('process error, continue, error info: {}'.format(str(e)))
            doc_ls[index] = str(e)
        # _ =1
        if index % 100 == 0:
            data_new = pd.DataFrame(zip(doc_ls, href_ls), columns=['docs', 'urls'])
            data_new.to_csv(out_fp, index=False)

    GetDoc.close()
    data_new = pd.DataFrame(zip(doc_ls, href_ls), columns=['docs', 'urls'])
    data_new.to_csv(out_fp, index=False)


if __name__ == '__main__':
    parse('/Users/wwd/PycharmProjects/shidai/project/data/shidai201811docs3.csv', '/Users/wwd/PycharmProjects/shidai/project/data/shidai201811docs3.csv')