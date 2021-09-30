# -*- coding: utf-8 -*- 
# @Time : 2021/9/29 16:10 
# @Author : Corn
# @File : testhttp.py
import re
import unittest

import ddt

from WM.tool.getdata import GetData
from WM.tool.http_request import HttpRequest
from WM.tool.log import MyLogger
from WM.tool.readExcel import ReadExcel
import  json

mylog = MyLogger().get_log()
readex = ReadExcel("批量业务接口.xlsx")
test_data = readex.read_cases("登录")
print("*****", test_data)


@ddt.ddt
class TestHttp(unittest.TestCase):
    def setup(self):
        pass

    def teardown(self):
        pass

    @ddt.data(*test_data)
    def test001(self, item):
        if item["depnedid"] != None:  # 判断是否存在接口关联
            # 将被依赖的接口信息读取出来
            # dependcase=readex.read_dependcase("登录", "case_001")
            dependcase = readex.read_dependcase(item["sheetname"], item["depnedid"])

            # 获取被依赖的键{'testfan-token': '029ce68381244657ac4df6a0584be880'}—>testfan-token
            dependkey = item["depnedkey"]
            # 构造依赖数据{'testfan-token': '029ce68381244657ac4df6a0584be880'}
            depend_value = re.findall(re.findall("'%s': '(.+?)'"%dependkey, dependcase[11]))
            depend_parm={dependkey:depend_value}
            print(depend_parm)


            try:
                resp = HttpRequest().http_request(item["method"], item["url"], eval(item["params"]),
                                                  GetData().Cookie, item["header"])
                print(resp.text)
            except Exception as e:
                mylog.error(e)
