import db


def get_brand_id(brand_name):
    # SELECT * FROM models WHERE regexp_replace(name,'-','','g') ~* 'Brother HL1030';
    q = db.i_request(f"SELECT id FROM brands WHERE LOWER(name) = LOWER('{brand_name}')")
    if q:
        return q[0][0]
    else:
        return 0


# def insert_cartridge(brand_id, code, name_en, name_ru):
#     q = db.i_request(f"WITH s as (SELECT id FROM cartridge "
#                      f"WHERE brand_id = {brand_id} AND code = '{code}'), "
#                      f"i as (INSERT INTO cartridge (brand_id, code, name, name_ru) "
#                      f"SELECT {brand_id}, '{code}', '{name_en}', '{name_ru}' "
#                      f'WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s')
#     if q:
#         return q[0][0]
#     else:
#         return 0
#
#
# def light_insert_cartridge(brand_id, code, name, name_ru):
#     q = db.i_request(f'WITH s as (SELECT id FROM cartridge '
#                      f'WHERE code = \'{code}\'), '
#                      f'i as (INSERT INTO cartridge (brand_id, code, name, name_ru) '
#                      f'SELECT {brand_id}, \'{code}\', NULL, NULL '
#                      f'WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s')
#     if q:
#         return q[0][0]
#     else:
#         return 0


def insert_supplies_analog_model(brand_id, model):
    q = db.i_request(f'WITH s as (SELECT id FROM supplies_analog_model '
                     f'WHERE brand_id = {brand_id} AND model = \'{model}\'), '
                     f'i as (INSERT INTO supplies_analog_model (brand_id, model) '
                     f'SELECT {brand_id}, \'{model}\' WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) '
                     f'SELECT id FROM i UNION ALL SELECT id FROM s')
    if q:
        return q[0][0]
    else:
        return 0


def link_supplies_model_analog(partcode_id, supplies_analog_model_id):
    db.i_request(f'INSERT INTO link_supplies_model_analog (partcode_id, supplies_analog_model_id) '
                 f'VALUES({partcode_id}, {supplies_analog_model_id})')


def insert_dictionary_partcode_options(text):
    q = db.i_request(f'WITH s as (SELECT id FROM dictionary_partcode_options '
                     f'WHERE text_ru = \'{text}\'), i as (INSERT INTO dictionary_partcode_options (text_ru) '
                     f'SELECT \'{text}\' WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) '
                     f'SELECT id FROM i UNION ALL SELECT id FROM s')
    if q:
        return q[0][0]
    else:
        return 0


def link_cartridge_options(dictionary_partcode_caption_id, dictionary_partcode_option_id):
    q = db.i_request(f'WITH s as (SELECT id FROM link_dictionary_partcode_options '
                     f'WHERE dictionary_partcode_caption_id = {dictionary_partcode_caption_id} AND '
                     f'dictionary_partcode_option_id = {dictionary_partcode_option_id}), '
                     f'i as (INSERT INTO link_dictionary_partcode_options (dictionary_partcode_caption_id, dictionary_partcode_option_id) '
                     f'SELECT {dictionary_partcode_caption_id}, {dictionary_partcode_option_id} WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) '
                     f'SELECT id FROM i UNION ALL SELECT id FROM s')
    if q:
        return q[0][0]
    else:
        return 0


def insert_partcodes(code, pn_id, brand_id):
    q = db.i_request(f"WITH s as (SELECT id FROM partcodes "
                     f"WHERE LOWER(code) = LOWER('{code}')), i as "
                     f"(INSERT INTO partcodes (code, manufacturer, dictionary_partcode_id, supplies) "
                     f"SELECT '{code}', {brand_id}, {pn_id}, TRUE "
                     f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    return q[0][0]


def link_supplies_analog(supplies_id, supplies_analog_id):
    db.i_request(f'INSERT INTO link_supplies_analog (supplies_id, supplies_analog_id) '
                 f'VALUES({supplies_id}, {supplies_analog_id})')


def insert_dict_partcode(code_name_en, code_name_ru):
    if code_name_en:
        q = db.i_request(f"WITH s as (SELECT id FROM dictionary_partcode "
                         f"WHERE LOWER(name_en) = LOWER('{code_name_en}')), i as "
                         f"(INSERT INTO dictionary_partcode (name_en, name_ru) SELECT '{code_name_en}', '{code_name_ru}' "
                         f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    else:
        q = db.i_request(f"WITH s as (SELECT id FROM dictionary_partcode "
                         f"WHERE LOWER(name_ru) = LOWER('{code_name_ru}')), i as "
                         f"(INSERT INTO dictionary_partcode (name_ru) SELECT '{code_name_ru}' "
                         f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    return q[0][0]


def get_supplies_id(cart):
    q = db.i_request(f"SELECT id FROM partcodes WHERE code = '{cart}'")
    if q:
        return q[0][0]


def get_dict_partcode_id(code_name_en):
    q = db.i_request(f"SELECT id FROM dictionary_partcode WHERE name_en = '{code_name_en}'")
    if q:
        return q[0][0]


def update_dict_partcode(dict_partcode_id, code_name_ru):
    db.i_request(f"UPDATE dictionary_partcode SET name_ru = '{code_name_ru}' "
                 f"WHERE id = {dict_partcode_id}")


def link_partcode_options(partcode_id, link_id):
    db.i_request(f"INSERT INTO link_partcode_options (partcode_option_id, partcode_dictionary_id) VALUES ({link_id}, {partcode_id})")