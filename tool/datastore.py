import re
import unittest
import ddt

from WM.tool.getdata import GetData
from WM.tool.http_request import HttpRequest
from WM.tool.log import MyLogger
from WM.tool.project_path import case_config_path
from WM.tool.readExcel import ReadExcel
# 导入字体、边框、颜色以及对齐方式相关库
from openpyxl.styles import PatternFill

#实例化log日志对象
from WM.tool.readconfig import ReadConfig
mylog=MyLogger().get_log()

readex=ReadExcel("业务.xlsx")
test_data=readex.read_cases()
print(test_data)

@ddt.ddt
class TestOne(unittest.TestCase):
    def setUp(self):
       pass
    def tearDown(self):
        pass
    @ddt.data(*test_data)
    def test_api(self,item):
        try:
            #判断是否存在接口依赖，存在获取依赖值，构造依赖参数，将依赖参数写回excel
            if item["casedepnedname"]:
               depend_case=readex.read_depend_case(item["sheetname"],item["casedepnedname"])
               depend_value=re.findall("'data': '(.+?)'}",depend_case[8])
               print(depend_value[0])
               #case_depend=depend_case[]
               # 将被依赖的接口返回值写回excel
               readex.write_back(item["sheetname"], item["case_id"]+1, 12,str(depend_value[0]))
               #将被依赖的字段写回excel
               readex.write_back(item["sheetname"], item["case_id"]+1, 14, str({item["casedepnedkey"]:depend_value[0]}))
               #发起请求
               res = HttpRequest().http_request(item["method"], item["url"], eval(item["params"]),GetData.Cookie,{"testfan-token":depend_value[0]})
            else:
                res = HttpRequest().http_request(item["method"], item["url"], eval(item["params"]), GetData.Cookie, eval(item["header"]))
            mylog.info("正在执行第%s条用例\n测试用例:%s\n请求地址:%s\n请求方式:%s\n请求参数:%s\n请求头%s\n响应值:%s\n响应头:%s"%(item["case_id"],item['title'],item['url'],item['method'],item['params'],res.request.headers,res.json(),res.headers))
        except Exception as e:
            result = "测试失败"
            color = "FF0000"  # 红色
            readex.write_back(item["sheetname"], item["case_id"] + 1, 10, result, color)
            readex.write_back(item["sheetname"], item["case_id"] + 1, 9, str(e))
            mylog.error(e)

        if res.cookies :
            setattr(GetData,"Cookie",res.cookies)
        if res.json()["data"]:
            setattr(GetData, "Token",res.json()["data"])
        try:
            self.assertEqual(item["expected"], res.json()["code"])
            result = "测试通过"
            color="00FF00"  # 绿色
            mylog.info("断言成功")
        except Exception as e:
            result="测试失败"
            color = "FF0000"#红色
            mylog.error(e)
            raise e
        finally:
            readex.write_back(item["sheetname"],item["case_id"]+1,9,str(res.json()))#将接口返回值写回excel
            readex.write_back(item["sheetname"],item["case_id"]+1,10, result,color)#将测试结果写回excel
        print(item["title"],res.json())

