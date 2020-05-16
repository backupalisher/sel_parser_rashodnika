import os

import pandas
from selenium import webdriver

from model_references import ModelReferences


def get_link_cart_model():
    urls = pandas.read_csv(os.path.join('res', 'brand_links'), header=None).values.tolist()
    driver = webdriver.Chrome()
    parser = ModelReferences(driver, urls)
    parser.parser()


def get_model_property():
    url = [['http://rashodnika.net/HP-CF226A.html', 'Brother Ремень переноса', 'OP-1CL']]
    driver = webdriver.Chrome()
    parser = ModelReferences(driver, url)
    parser.parser()


def main():
    get_model_property()


if __name__ == '__main__':
    main()
