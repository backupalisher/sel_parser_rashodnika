import os

import pandas
from selenium import webdriver

from model_references import ModelReferences


def get_link_cart_model():
    urls = pandas.read_csv(os.path.join('res', 'brand_links'), header=None).values.tolist()
    driver = webdriver.Chrome()
    parser = ModelReferences(driver, urls)
    parser.parser()


def get_model_property(urls):
    for url in urls:
        driver = webdriver.Chrome()
        parser = ModelReferences(driver, url)
        parser.parser()


def load_file_list():
    path = r'res'
    d = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if 'brand_links' != file:
                d.append(os.path.join(root, file))
    return d


def load_urls():
    urls = []
    files = load_file_list()
    for file in files:
        print(file)
        try:
            data = pandas.read_csv(file, sep=';', header=None).values.tolist()
            for d in data:
                urls.append(d[0])
        except:
            pass
    return urls


def main():
    # get_link_cart_model()
    urls = load_urls()
    get_model_property(urls)


if __name__ == '__main__':
    main()
