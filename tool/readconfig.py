import configparser
from WM.tool.project_path import case_config_path

class ReadConfig:
    def __init__(self,filename):
        self.cf=configparser.ConfigParser()
        self.filenam=filename
        self.cf.read(case_config_path+"/"+filename,encoding='utf-8')
    def read_config(self,section,option):
        result=self.cf.get(section,option)
        return result
    def write_config(self,section,option,data):
        result = self.cf.set(section,option,data)
        self.cf.write(open(case_config_path+"/"+filename,"w",encoding='utf-8'))
        return result
if __name__ == '__main__':
    filename="wmcase.conf"
    res=eval(ReadConfig(filename).read_config("MODE",'mode'))
    print(res)
    for i in res.keys():
        print(i)
    # login_token="112sdff23rfd5"
    # rw=ReadConfig(filename).write_config("Token","token",login_token)
    # res1 = ReadConfig(filename).read_config("Token","token")
    # print(type(res1))