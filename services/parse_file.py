import ast
import re

import pandas

from db_utils import *


async def parse(file):
    # try:
    file_list = pandas.read_csv(file, sep=';', header=None).values.tolist()[0]
    # for elem in file_list:
    #     print(elem)

    brand = re.sub(r'/.*', '', file_list[0]).strip()
    partcode = re.sub(r'(\s.+)', '', re.sub(rf'{brand}', '', file_list[2], flags=re.IGNORECASE).strip()).strip()
    if 'nan' in str(file_list[2]):
        name_ru = None
    else:
        name_ru = re.sub(f'{brand}', '', re.sub(f'{partcode}', '', str(file_list[2]), re.I), re.I).strip()

    if 'nan' in str(file_list[1]):
        name_en = None
    else:
        name_en = re.sub(r"'", '`', re.sub(r'^/|^-|\([^)]*\)', '', str(file_list[1]))).strip()

    model_analogs = ast.literal_eval(file_list[3])

    options = ast.literal_eval(file_list[4])
    # obj = {'brand': brand, 'partcode': partcode, 'name_en': name_en, 'name_ru': name_ru,
    #        'model_analogs': model_analogs, 'options': options}
    return {'brand': brand, 'partcode': partcode, 'name_en': name_en, 'name_ru': name_ru,
            'model_analogs': model_analogs, 'options': options}
    # except Exception as err:
    #     print(err, file)


async def set_option(options, code):
    print(code, options)
    pid = get_supplies_id(code)
    if pid:
        for opt in options:
            dic_caption_id = get_dict_partcode_option_id(opt[0])
            dic_option_id = get_dict_partcode_option_id(opt[1])
            if dic_caption_id and dic_option_id:
                option_id = get_option_id(dic_caption_id, dic_option_id)
                link_partcode_options(option_id, pid)
            else:
                print('nod ids for', opt)
    else:
        print('no id for', code)


async def set_model_analog(models, code, brand, brands):
    if brand == 'HP':
    # if brand == 'HP' and code == 'CE390A':
        print(models, code, brand, brands)
        # if brand == 'Konica Minolta':
        #     b_id = brands['Konica-Minolta']
        # else:
        #     b_id = brands[brand]
        # partcode_id = get_supplies_id(code)
        # if partcode_id:
        #     for model in models:
        #         model_id = get_model_id(b_id, model, model.replace('-', ' '))
        #         print(b_id, model, model_id, partcode_id)
                # link_partcode_analog(model_id, partcode_id)
