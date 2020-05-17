import os
import re

import pandas


class ModelReferences(object):
    def __init__(self, driver, urls):
        self.driver = driver
        self.urls = urls

    def parser(self):
        # self.get_links_cart_model()
        self.get_model_property()

    def get_links_cart_model(self):
        for url in self.urls:
            print(url[0])
            cart_list = []

            self.driver.get(url[0])
            td = self.driver.find_elements_by_xpath('//*[@id="listoftovar"]/table/tbody/tr/td/a')
            brand_name = self.driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td[2]/h5')
            brand_name = re.sub(r'\s/\s', '_', brand_name.text)
            print(brand_name)
            for tableData in td:
                cart_name = tableData.text
                cart_title = tableData.get_attribute('title')
                cart_link = tableData.get_attribute('href')
                if cart_list:
                    if cart_link != cart_list[-1][0]:
                        cart_list.append([cart_link, cart_title, cart_name])
                    else:
                        cart_list[-1].append(cart_name)
                else:
                    cart_list.append([cart_link, cart_title, cart_name])

            for cart in cart_list:
                print(cart)

            df = pandas.DataFrame(cart_list)
            df.to_csv(os.path.join('res', f'{brand_name}.csv'), index=False, mode='a', header=False, sep=";")

    def get_model_property(self):
        for url in self.urls:
            analog_list = []
            property_list = []
            property_data = []

            try:
                self.driver.get(url)
                brand_name = self.driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td[2]/h5[1]').text
                model_name = self.driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td[2]/h5[2]').text
                # model_name_en = self.driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td[2]/text()[2]')
                model_analog = self.driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td[2]/ul')
                property_table = self.driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td[2]/table[1]/tbody')

                print(model_name)
                ele = model_analog.find_elements_by_tag_name('li')
                for m in ele:
                    analog_list.append(m.text)

                for row in property_table.find_elements_by_tag_name('tr'):
                    property_list.append([td.text for td in row.find_elements_by_tag_name('td')])

                property_data.append([brand_name, model_name, analog_list, property_list])

                fn = re.sub(r'\s.*|/', '', model_name)
                df = pandas.DataFrame(property_data)
                df.to_csv(os.path.join('parse', f'{fn}.csv'), index=False, mode='a', header=False, sep=";")
            except:
                pass
