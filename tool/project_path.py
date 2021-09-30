import os
'''
用于读取路径的值
'''
#os.path.split(project_path)将文件名和路径分开
#os.path.realpath(__file__)#获取当前文件的绝对路径
#获取项目路径E:\python-work\WM

project_path=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
#print(project_path)


#测试数据路径
test_data_path=os.path.join(project_path,"data")
#print("测试用例路径",test_case_path)
#测试报告路径
test_report_path=os.path.join(project_path,"report")
#print(test_report_parh)
#日志存储路径
log__file_path=os.path.join(project_path,"log")
#print(log__file_path)

#配置文件路径
case_config_path=os.path.join(project_path,"Config")


