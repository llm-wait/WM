# -*- coding: utf-8 -*- 
# @Time : 2021/9/30 9:33 
# @Author : Corn
# @File : aa.py
import json
import re
resp_data={
  "code": 200,
  "data": [
    {
      "id": "0e1e9407e52d435980de18a5994afe62",
      "login_name": "zghqzts",
      "login_pwd": "123456",
      "dept_id": "f18602be7ff14c918121d0fe7775fd51",
      "dept_name": "null",
      "remark": "作业室主任",
      "roleFlag": "null"
    },
{
      "id": "c3029c6279384800bb093463d4507337",
      "login_name": "zkzz",
      "login_pwd": "123456",
      "dept_id": "",
      "dept_name": "null",
      "remark": "质控组长",
      "roleFlag": "null"
    },
  ],
  "message": "success",
}
data={'code': '0', 'message': 'success', 'data': '029ce68381244657ac4df6a0584be880',}

#print(re.findall("'code': '(.+?)'",str(data)))  成功匹配单层数据
a="dept_id"
print(re.findall("'%s': '(.+?)'"%a,str(resp_data)))