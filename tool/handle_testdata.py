# -*- coding: utf-8 -*- 
# @Time : 2021/10/15 16:50 
# @Author : Corn
# @File : handle_testdata.py
import re

from WM.tool.readExcel import ReadExcel

readex = ReadExcel("批量业务接口.xlsx")

class HandleTestData:
    '''
    用于处理测试用例数据
    '''
    def handledata(self, respdata, finalstr):
        '''
        用于提取接口返回值中的依赖的值，如果没有值默认是键名
        :param respdata:  接口的返回值
        :param finalstr: 依赖的键值
        :return:
        '''
        if isinstance(respdata, dict):
            if finalstr in respdata.keys():
                final_value = respdata[finalstr]
            else:
                for k in respdata.keys():
                    if isinstance(respdata[k], dict):
                        final_value = respdata[k].get(finalstr)
        elif respdata==None:
            final_value = finalstr
        return final_value
    def handlecasedata(self,after_data):
        for item in after_data:
            # 将被依赖的接口信息读取出来
            dependcase = readex.read_dependcase(item["sheetname"], item["bedepnedid"])
            # 获取被依赖的键testfan-token
            dependkey = item["bedepnedkey"]
            # 获取依赖的值{'testfan-token': '029ce68381244657ac4df6a0584be880'}
            depend_value = self.handledata(eval(dependcase[12]), dependkey)
            depend_parm = {item["depnedkey"]: depend_value}  # 构造依赖数据
            # 将构造的依赖数据写回excel中
            readex.write_back_dependdata(item["sheetname"], int(item["case_id"].split("_")[1]) + 1,
                                         str(depend_parm))
            # 判断请求参数，将变量值替换成变量值
            req_data = eval(item["params"])
            if dependkey in req_data.keys():
                req_data[dependkey] = depend_value
            # 将替换后的参写回excel中
            readex.write_back_params(item["sheetname"], int(item["case_id"].split("_")[1]) + 1, str(req_data))
            # print("***", item["params"])
            item["params"] = readex.read_handleparam(item["sheetname"], int(item["case_id"].split("_")[1]) + 1)
            # print("===", item["params"])

if __name__ == '__main__':
    after_data = readex.read_cases()
    print(HandleTestData().handlecasedata(after_data))

    # final_data = readex.read_cases()
    # print(final_data)
    # print(HandleTestData().handledata(a, mystr))
