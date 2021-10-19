import unittest
import time

from WM.script.testhttp import TestHttp
from WM.tool.htmlTestRunner import HTMLTestRunner
from WM.tool.project_path import test_report_path


suit=unittest.TestSuite()
load=unittest.TestLoader()
suit.addTest(load.loadTestsFromTestCase(TestHttp))

#执行
report_now=time.strftime('%Y-%m-%d_%H_%M_%S')
with open(test_report_path+"/result_"+report_now+".html",'wb')as f:
    runner=HTMLTestRunner(stream=f, title='系统接口',description='系统接口测试',tester="test")
    runner.run(suit)
