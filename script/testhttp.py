# -*- coding: utf-8 -*-
# @Time : 2021/9/29 16:10
# @Author : Corn
# @File : testhttp.py
import re
import time
import unittest
import warnings
import json
import ddt

from WM.tool.getdata import GetData
from WM.tool.handle_testdata import HandleTestData
from WM.tool.http_request import HttpRequest
from WM.tool.log import MyLogger
from WM.tool.readExcel import ReadExcel
import json

mylog = MyLogger().get_log()
readex = ReadExcel("批量业务接口.xlsx")
before_data = readex.read_cases()
print("*****", before_data)


# readex = ReadExcel("批量业务接口.xlsx")
# after_data = HandleTestData().handlecasedata(readex.read_cases())
# print(after_data)


@ddt.ddt
class TestHttp(unittest.TestCase):
    @classmethod
    def setUp(cls):
        warnings.simplefilter('ignore', ResourceWarning)

    def tearDown(self):
        pass

    @ddt.data(*before_data)
    def test001(self, item):
        if item["bedepnedid"]:
            # 将被依赖的接口信息读取出来
            dependcase = readex.read_dependcase(item["sheetname"], item["bedepnedid"])
            mylog.info("依赖的接口信息%s"%dependcase)
            # 获取被依赖的键testfan-token
            dependkey = item["bedepnedkey"]
            # 获取依赖的值{'testfan-token': '029ce68381244657ac4df6a0584be880'}
            depend_value = HandleTestData().handledata(eval(dependcase[12]), dependkey)
            depend_parm = {item["depnedkey"]: depend_value}  # 构造依赖数据
            mylog.info("依赖数据%s"%depend_parm)
            # 将构造的依赖数据写回excel中
            readex.write_back_dependdata(item["sheetname"], int(item["case_id"].split("_")[1]) + 1,
                                         str(depend_parm))
            # 判断请求参数，将变量值替换成变量值
            req_data = eval(item["params"])
            if dependkey in req_data.keys():
                req_data[dependkey] = depend_value
            # 将替换后的参写回excel中
            readex.write_back_params(item["sheetname"], int(item["case_id"].split("_")[1]) + 1, str(req_data))
            # # 解决token关联
            if item["header"]=="Yes":
                setattr(GetData, "Token", depend_parm )
            item["params"] = readex.read_handleparam(item["sheetname"], int(item["case_id"].split("_")[1]) + 1)
            mylog.info("处理后的请求参数%s"%item["params"])
            res = HttpRequest().http_request(item["method"], item["url"], eval(item["params"]), GetData.Cookie,
                                             GetData.Token)
        else:
            res = HttpRequest().http_request(item["method"], item["url"], eval(item["params"]), GetData.Cookie,
                                             eval(item["header"]))
            # 将接口返回值写回excel
        readex.write_back(item["sheetname"], int(item["case_id"].split("_")[1]) + 1, 13,
                          str(res.json()))
        # 解决cookie关联
        if res.cookies:
            setattr(GetData, "Cookie", res.cookies)

        try:
            self.assertIn(item["expected"], dict(res.json()).values())
            result = "测试通过"
            color = "00FF00"  # 绿色
            mylog.info("断言成功")
        except Exception as e:
            result = "测试失败"
            color = "FF0000"  # 红色
        finally:

            # 将测试结果写回excel
            readex.write_back(item["sheetname"], int(item["case_id"].split("_")[1]) + 1, 14, result,
                              color)
        # print("****",res.json())
        # print("====",res.request.body)


