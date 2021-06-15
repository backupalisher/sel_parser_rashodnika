import ast
import os
import re

from logzero import logger, logfile
import pandas

import db_utils


def load_log():
    pars_file_list = []
    with open("log_console.log", "r") as file:
        for line in file:
            pars_file_list.append(re.sub('.*] parse/', '', line).strip().replace('\\', ''))
    return pars_file_list


def load_file_list():
    path = r'parse'
    file_list = []
    pars_file_list = load_log()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file in pars_file_list:
                print(file, '- parsed')
            else:
                file_list.append(os.path.join(root, file))
    return file_list


def parser():
    logfile('log_console.log')

    file_list = load_file_list()
    for file in file_list:
        data_lists = pandas.read_csv(file, sep=';', header=None).values.tolist()
        brand_name = re.sub(r'/.*', '', data_lists[0][0]).strip()
        if brand_name == 'Konica Minolta':
            brand_id = db_utils.get_brand_id('Konica-Minolta')
        else:
            brand_id = db_utils.get_brand_id(brand_name)

        if brand_id < 1:
            print('Brand not found.', brand_id, brand_name)
            break

        partcode = re.sub(rf'{brand_name}', '', data_lists[0][2], flags=re.IGNORECASE).strip()
        partcode = re.sub(r'(\s.+)', '', partcode).strip()
        code_name_ru = re.sub(rf'.*{partcode}|{brand_name}', '', data_lists[0][2], flags=re.IGNORECASE).strip()
        code_name_ru = re.sub(rf'^/|^-|\([^)]*\)', '', code_name_ru).strip()
        code_name_ru = re.sub(rf"'", '`', code_name_ru).strip()

        code_name_en = data_lists[0][1]

        code_name_en = re.sub(rf"nan", '', str(code_name_en)).strip()
        code_name_en = re.sub(rf"\n|\r|\n\r", '', code_name_en).strip()
        code_name_en = re.sub(rf"'", '`', code_name_en).strip()
        dict_partcode_id = None

        if code_name_en and code_name_ru:
            dict_partcode_id = db_utils.get_dict_partcode_id(code_name_en)
            if dict_partcode_id:
                db_utils.update_dict_partcode(dict_partcode_id, code_name_ru)
            else:
                dict_partcode_id = db_utils.insert_dict_partcode(code_name_en, code_name_ru)
        elif code_name_en:
            dict_partcode_id = db_utils.insert_dict_partcode(code_name_en, None)
        elif code_name_ru:
            dict_partcode_id = db_utils.insert_dict_partcode(None, code_name_ru)

        if partcode and dict_partcode_id and brand_id:
            partcode_id = db_utils.insert_partcodes(partcode, dict_partcode_id, brand_id)
        else:
            print(partcode, dict_partcode_id, brand_id)
            break

        model_analogs = ast.literal_eval(data_lists[0][3])
        # cart_ref = ast.literal_eval(data_lists[0][4])

        for model in model_analogs:
            model_id = db_utils.get_model_id(brand_id, brand_name + ' ' + re.sub(r'\([^)]*\)', '', model).strip())
            if model_id:
                print('Linked: ', model_id, brand_name + ' ' + re.sub(r'\([^)]*\)', '', model).strip())
                db_utils.link_model_supplies(model_id, partcode_id)
            else:
                model_id = db_utils.get_model_id(brand_id, re.sub(r'\([^)]*\)', '', model).strip())
                if model_id:
                    print('Linked: ', model_id, re.sub(r'\([^)]*\)', '', model).strip())
                    db_utils.link_model_supplies(model_id, partcode_id)
                else:
                    model_id = db_utils.get_model_id(brand_id, brand_name + ' ' + re.sub(r'\([^)]*\)', '', model.replace('-', ' ')))
                    if model_id:
                        print('Linked: ', model_id, re.sub(r'\([^)]*\)', '', model.replace('-', ' ')))
                        db_utils.link_model_supplies(model_id, partcode_id)



        # for model in model_analogs:
        #     supplies_analog_model_id = \
        #         db_utils.insert_supplies_analog_model(brand_id, re.sub(r'\([^)]*\)', '', model).strip())
        #     if partcode_id and supplies_analog_model_id:
        #         db_utils.link_supplies_model_analog(partcode_id, supplies_analog_model_id)
        #
        # for text in cart_ref:
        #     dict_partcode_opt_id_caption = db_utils.insert_dictionary_partcode_options(str(text[0]).replace("'", "`").replace('"', '`'))
        #     dict_partcode_opt_id_option = db_utils.insert_dictionary_partcode_options(str(text[1]).replace("'", "`").replace('"', '`'))
        #     if dict_partcode_id and dict_partcode_opt_id_caption and dict_partcode_opt_id_option:
        #         link_id = db_utils.link_cartridge_options(dict_partcode_opt_id_caption, dict_partcode_opt_id_option)
        #         if link_id:
        #             db_utils.link_partcode_options(partcode_id, link_id)
        #
        # for n in cart_ref:
        #     if n[0] == 'Part No.':
        #         carts = [x.strip() for x in n[1].split(',') if x]
        #         for cart in carts:
        #
        #             cart = re.sub(rf'{brand_name}|\n', ' ', cart).strip()
        #             if partcode != cart:
        #                 cartridge_analog_id = db_utils.get_supplies_id(cart)
        #                 if cartridge_analog_id and partcode_id:
        #                     db_utils.link_supplies_analog(partcode_id, cartridge_analog_id)
        logger.info(file)
