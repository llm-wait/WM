# -*- coding: utf-8 -*- 
# @Time : 2021/10/9 13:47 
# @Author : Corn
# @File : handle_excel.py
import re
from typing import Dict, Any

from WM.tool.readExcel import ReadExcel

readex = ReadExcel("批量业务接口.xlsx")
test_data = readex.read_cases()
class HandleExcelData():
    def handledata(self,test_data):
        final_data=[]
        for item in test_data:
            # 判断是否存在依赖
            if item["bedepnedid"]:
                # 将被依赖的接口信息读取出来
                dependcase = readex.read_dependcase(item["sheetname"], item["bedepnedid"])
                # 获取被依赖的键testfan-token
                dependkey = item["bedepnedkey"]
                # 获取依赖的值{'testfan-token': '029ce68381244657ac4df6a0584be880'}
                depend_value = re.findall("'%s': '(.*?)'," % dependkey, str(dependcase[12]))
                #print(depend_value)
                depend_parm = {item["depnedkey"]: depend_value[0]}  # 构造依赖数据
                # print("*********",depend_parm)
                # 将构造的依赖数据写回excel中
                readex.write_back_dependdata(item["sheetname"], int(item["case_id"].split("_")[1]) + 1,
                                             str(depend_parm))
                # 判断是是否存在请求参数，存在则将请求参数值替换为依赖值
                # 判断依赖的键是否存在请求参数中，存在则将请求参数值替换为依赖值
                req_data = eval(item["params"])
                if dependkey in req_data.keys():
                    req_data[dependkey] = depend_value[0]
                # 将替换后的参写回excel中
                readex.write_back_params(item["sheetname"], int(item["case_id"].split("_")[1]) + 1, str(req_data))
            final_data.append(item)
        return  final_data

if __name__ == '__main__':
    print(HandleExcelData().handledata(test_data))