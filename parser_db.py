import ast
import os
import re

from logzero import logger, logfile
import pandas

import db_utils


def load_file_list():
    path = r'parse'
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def parser():
    logfile('log_console.log')

    file_list = load_file_list()
    for file in file_list:
        dict_partcode_id = 0
        code_name_en = ''

        data_lists = pandas.read_csv(file, sep=';', header=None).values.tolist()
        brand_name = re.sub(r'/.*', '', data_lists[0][0]).strip()
        if brand_name == 'Konica Minolta':
            brand_id = db_utils.get_brand_id('Konica-Minolta')
        else:
            brand_id = db_utils.get_brand_id(brand_name)

        if brand_id < 1:
            print('Brand not found.', brand_id, brand_name)
            break
        # code_name_en = ''

        partcode = re.sub(rf'{brand_name}', '', data_lists[0][2], flags=re.IGNORECASE).strip()
        partcode = re.sub(r'(\s.+)', '', partcode).strip()
        code_name_ru = re.sub(rf'.*{partcode}|{brand_name}', '', data_lists[0][2], flags=re.IGNORECASE).strip()
        code_name_ru = re.sub(rf'^/|^-|\([^)]*\)', '', code_name_ru).strip()
        code_name_ru = re.sub(rf"'", '`', code_name_ru).strip()

        code_name_en = data_lists[0][1]
        dict_partcode_id = 0
        if code_name_en and str(code_name_en) != 'nan' and code_name_ru:
            code_name_en = re.sub(rf"'", '`', code_name_en).strip()
            dict_partcode_id = db_utils.get_dict_partcode_id(code_name_en)
            if dict_partcode_id:
                db_utils.update_dict_partcode(dict_partcode_id, code_name_ru)
            else:
                dict_partcode_id = db_utils.insert_dict_details(code_name_en, code_name_ru)
        elif code_name_ru:
            dict_partcode_id = db_utils.insert_dict_details('', code_name_ru)

        if partcode and dict_partcode_id and brand_id:
            partcode_id = db_utils.insert_partcodes(partcode, dict_partcode_id, brand_id)
        else:
            print(partcode, dict_partcode_id, brand_id)
            break

        """"For deleted"""
        # code_id = db_utils.get_code_id(partcode)
        # if not code_id:
        #     code_id = db_utils.insert_cartridge(brand_id, cart_code, cart_name_en, cart_name)
        #     #     db_utils.update_cartridge(brand_id, cartridge_id, cart_name_en, cart_name)
        #     # else:
        """end"""

        model_analogs = ast.literal_eval(data_lists[0][3])
        cart_ref = ast.literal_eval(data_lists[0][4])

        print(brand_name, partcode, code_name_en, code_name_ru)
        # print([i for i in cart_ref])
        # print([i for i in model_analogs])

        for model in model_analogs:
            supplies_analog_model_id = \
                db_utils.insert_cartridge_analog_model(brand_id, re.sub(r'\([^)]*\)', '', model).strip())
            if partcode_id and supplies_analog_model_id:
                db_utils.link_cartridge_model_analog(partcode_id, supplies_analog_model_id)

        for text in cart_ref:
            dict_partcode_opt_id_caption = db_utils.insert_spr_cartridge_options(str(text[0]).replace("'", "`").replace('"', '`'))
            dict_partcode_opt_id_option = db_utils.insert_spr_cartridge_options(str(text[1]).replace("'", "`").replace('"', '`'))
            if dict_partcode_id and dict_partcode_opt_id_caption and dict_partcode_opt_id_option:
                db_utils.link_cartridge_options(dict_partcode_opt_id_caption, dict_partcode_opt_id_option)

        for n in cart_ref:
            if n[0] == 'Part No.':
                carts = [x.strip() for x in n[1].split(',') if x]
                for cart in carts:

                    cart = re.sub(rf'{brand_name}|\n', ' ', cart).strip()
                    if partcode != cart:
                        # print(brand_name, cart)
                        cartridge_analog_id = db_utils.get_supplies_id(cart)
                        if cartridge_analog_id and partcode_id:
                            db_utils.link_cartdge_analog(partcode_id, cartridge_analog_id)
                        else:
                            log = str(partcode) + ' = ' + str(cart)
                            logger.error(log)
                            # partcode_id = db_utils.light_insert_cartridge(brand_id, cart, None, None)
                        # db_utils.update_cartridge_brand_id(brand_id, cart)
                        # if cartridge_analog_id and partcode_id:
                        #     db_utils.link_cartdge_analog(partcode_id, cartridge_analog_id)
