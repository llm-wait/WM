import os
import re

import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import Font, colors
from openpyxl.styles import PatternFill
from openpyxl.styles.colors import ColorList

from WM.tool.project_path import test_data_path
from WM.tool.readconfig import ReadConfig


class ReadExcel():
    '''
    从配置文件case.conf中读取[MODE]->mode值,(测试的工作表和执行的模式)
    mode控制是否执行所有的用例，mode值只能是all或列表，默认值all表示执行所有的用例，
    列表表示执行指定的用例
    '''

    def __init__(self, filename):
        self.filename = filename
        self.wb = openpyxl.load_workbook(test_data_path + "/" + filename)
        self.confile = "wmcase.conf"

    def read_cases(self, sheetname):
        sheet = self.wb[sheetname]
        test_data = []
        for i in range(2, sheet.max_row + 1):
            row_data = {}  # 单行测试用例
            row_data["case_id"] = sheet.cell(i, 1).value
            row_data["module"] = sheet.cell(i, 2).value
            row_data["url"] = sheet.cell(i, 3).value
            row_data["method"] = sheet.cell(i, 4).value
            row_data["title"] = sheet.cell(i, 5).value
            row_data["params"] = sheet.cell(i, 6).value
            row_data["header"] = sheet.cell(i, 7).value
            # 依赖的接口case_id
            row_data["depnedid"] = sheet.cell(i, 8).value
            # 被依赖的接口返回值
            row_data["depnedkey"] = sheet.cell(i, 9).value
            # 依赖的字段
            row_data["depneddata"] = sheet.cell(i, 10).value
            row_data["expected"] = sheet.cell(i, 11).value
            # 测试用例中添加sheetname字典，用于测试结果写回时之指定excel
            row_data["sheetname"] = sheetname
            test_data.append(row_data)
        return test_data

    def write_back(self, sheet_name, i, j, value, back_color=None):
        '''
        用于写回测试结果
        '''
        sheet = self.wb[sheet_name]
        sheet.cell(i, j).value = value
        # 设置写回单元格填充颜色,默认是白色
        if back_color == None:
            sheet.cell(i, j).fill = PatternFill("solid", fgColor="FFFFFF")
        else:
            sheet.cell(i, j).fill = PatternFill("solid", fgColor=back_color)
        self.wb.save(test_data_path + "/" + self.filename)

    def read_dependcase(self, sheetname, case_id):
        '''
        用于读取接口依赖测试数据
        根据传递的参数case_id,找到对应行的数据
        :param sheetname:被依赖的接口所在工作表
        :param  case_id:被依赖的接口，是个int
        :return:
        '''
        sheet = self.wb[sheetname]
        depandcase = []
        for i in range(1, sheet.max_column + 1):
            depandcase.append(sheet.cell(int(case_id.split("_")[1]) + 1, i).value)
        return depandcase

    def read_dependcase1(self, sheetname, case_id):
        '''
        用于读取接口依赖测试数据
        根据传递的参数case_id,找到对应行的数据
        :param sheetname:被依赖的接口所在工作表
        :param  case_id:被依赖的接口，是个int
        :return:
        '''
        sheet = self.wb[sheetname]
        depandcase = {}
        for i in range(1, sheet.max_column + 1):

            depandcase["case_id"] = sheet.cell(int(case_id.split("_")[1]) + 1,1).value
            depandcase["url"] = sheet.cell(int(case_id.split("_")[1]) + 1, 3).value
            depandcase["method"] = sheet.cell(int(case_id.split("_")[1]) + 1, 4).value
            depandcase["params"] = sheet.cell(int(case_id.split("_")[1]) + 1, 6).value
            depandcase["header"] = sheet.cell(int(case_id.split("_")[1]) + 1, 7).value
            # 被依赖的接口返回值
            depandcase["respdata"] = sheet.cell(int(case_id.split("_")[1]) + 1, 12).value
            # 测试用例中添加sheetname字典，用于测试结果写回时之指定excel
            depandcase["sheetname"] = sheetname
            # depandcase.append(sheet.cell(int(case_id.split("_")[1]) + 1, i).value)
        return depandcase


if __name__ == '__main__':
    filename = "批量业务接口.xlsx"
    read = ReadExcel(filename)
    print(read.read_cases("登录"))
    dependcase = read.read_dependcase1("登录", "case_003")
    a=eval(dependcase["respdata"])
    print(a)
    print(a["data"])



