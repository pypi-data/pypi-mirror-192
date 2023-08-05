#!/share/nas2/genome/biosoft/Python//3.7.3/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/12/6 15:41
# @Author : jmzhang
# @Email : zhangjm@biomarker.com.cn
import logging

import spatial_tools
import argparse

app = spatial_tools.SpatialApp.run_dash(debug=False, return_app=True)

if __name__ == '__main__':
    desc = """
    Version: Version beta
    Contact: zhangjm <zhangjm@biomarker.com.cn>
    Program Date: 2022.10.25
    Description: spatial tools
    """

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--port', type=int, help='port', default=5070)
    parser.add_argument('--host', type=str, help='port', default='127.0.0.1')
    input_args = parser.parse_args()

    app.run_server(debug=False, mode='external', port=input_args.port, host=input_args.host)
