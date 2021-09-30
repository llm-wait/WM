import json

import requests
from requests import session

from WM.tool.getdata import GetData
from WM.tool.log import MyLogger
#实例化log日志对象
mylog=MyLogger().get_log()
class HttpRequest():
    def __init__(self):
        self.session=requests.Session()
    '''
    利用requests封装get/post请求
    url:请求的地址
    method：请求方式
    param:请求的参数，非必填参数，字典的格式传递
    header:请求头，非必填参数，字典的格式传递
    '''
    def http_request(self,method,url,param=None,cookie=None,header=None):
        try:
            if method.lower()=="get":
                resp=self.session.get(url,params=param,cookies=cookie,headers=header)
            elif method.lower() =="post":
                if header=={"Content-Type":"application/json"}:
                    resp=self.session.post(url,json=param, cookies=cookie,headers=header)
                else:
                    resp = self.session.post(url,data=param, cookies=cookie,headers=header)
            else:
                mylog.info("不支持的请求")
        except Exception as e:
            mylog.error("请求方式错误")
            raise e
        return resp
if __name__ == '__main__':
    login_url="http://192.168.199.4:8087/wm/sys/login/getLoginInfo"
    #login_data={"id":1}
    hp=HttpRequest()
    a=hp.http_request("get",login_url,)
    print(a.content)
