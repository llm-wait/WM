# -*- coding: utf-8 -*- 
# @Time : 2021/9/29 16:10 
# @Author : Corn
# @File : testhttp.py
import re
import time
import unittest
import warnings

import ddt

from WM.tool.getdata import GetData
from WM.tool.handle_excel import HandleExcelData
from WM.tool.handle_testdata import HandleTestData
from WM.tool.http_request import HttpRequest
from WM.tool.log import MyLogger
from WM.tool.readExcel import ReadExcel
import json

mylog = MyLogger().get_log()
readex = ReadExcel("批量业务接口.xlsx")
before_data = readex.read_cases()
print(before_data)
@ddt.ddt
class TestHttp(unittest.TestCase):
    @classmethod
    def setUp(cls):
        warnings.simplefilter('ignore', ResourceWarning)
    def tearDown(self):
        pass

    @ddt.data(*before_data)
    def test001(self, item):
        # {'case_id': 'case_005', 'module': '修改登录账户', 'url': 'http://192.168.199.4:8087/wm/sys/login/updateSysLogin',
        #  'method': 'post', 'title': '正向修改',
        #  'params': "{'id': '25fb120e22074116b85d6d9ed5938e7c', 'login_name': 'test', 'login_pwd': '123456', 'remark': 'test', 'roleIDs': '8888'}",
        #  'header': 'None', 'bedepnedid': 'case_004', 'bedepnedkey': 'id', 'depnedkey': 'id',
        #  'depneddata': "{'id': '25fb120e22074116b85d6d9ed5938e7c'}", 'expected': '修改成功！', 'sheetname': '登录（已调整）'}
        # 判断是否存在依赖
        if item["bedepnedid"]:
            # 将被依赖的接口信息读取出来
            dependcase = readex.read_dependcase(item["sheetname"], item["bedepnedid"])
            print("***",dependcase)
            # 获取被依赖的键testfan-token
            dependkey = item["bedepnedkey"]
            # 获取依赖的值{'testfan-token': '029ce68381244657ac4df6a0584be880'}
            depend_value=HandleTestData().handledata(eval(dependcase[12]),dependkey)
            # print("*****", type(depend_value))
            depend_parm = {item["depnedkey"]: depend_value}  # 构造依赖数据
            # print("*********",depend_parm)
            # 将构造的依赖数据写回excel中
            readex.write_back_dependdata(item["sheetname"], int(item["case_id"].split("_")[1]) + 1,
                                         str(depend_parm))
            # 判断是是否存在请求参数，存在则将请求参数值替换为依赖值
            # 判断依赖的键是否存在请求参数中，存在则将请求参数值替换为依赖值
            req_data = eval(item["params"])
            if dependkey in req_data.keys():
                req_data[dependkey] = depend_value
            # 将替换后的参写回excel中
            readex.write_back_params(item["sheetname"], int(item["case_id"].split("_")[1]) + 1, str(req_data))
            res = HttpRequest().http_request(item["method"], item["url"], eval(item["params"]), GetData.Cookie,
                                             GetData.Token)
        else:
            res = HttpRequest().http_request(item["method"], item["url"], eval(item["params"]), GetData.Cookie,
                                             eval(item["header"]))

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
            # 将接口返回值写回excel
            readex.write_back(item["sheetname"], int(item["case_id"].split("_")[1]) + 1, 13,
                              str(res.json()))
            # 将测试结果写回excel
            readex.write_back(item["sheetname"], int(item["case_id"].split("_")[1]) + 1, 14, result,
                              color)

        print(res.json())
        print(res.request.body)
        # print(item["params"])
