# import parser_http as ph
import asyncio

import parser_db as pd
import re


def main():
    # ph.get_link_cart_model()
    # ph.get_model_property()
    # pd.parser()
    asyncio.run(pd.init_parse())


if __name__ == '__main__':
    main()
