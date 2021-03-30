import os

import pandas
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from model_references import ModelReferences


options = Options()
options.add_argument("start-maximized")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--window-size=1366,768")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)


def get_link_cart_model():
    urls = pandas.read_csv(os.path.join('res', 'brand_links'), header=None).values.tolist()
    parser = ModelReferences(driver, urls)
    parser.parser()


def get_model_property():
    urls = load_urls()
    parser = ModelReferences(driver, urls)
    parser.parser()


def load_file_list():
    path = r'res'
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if 'brand_links' != file:
                file_list.append(os.path.join(root, file))
    return file_list


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