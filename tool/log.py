import logging.handlers
import os

import time

from WM.tool.project_path import log__file_path

class MyLogger():
    def get_log(self):
        self.logger = logging.getLogger()
        # 判断logger.handlers是否为空，为空则添加，不为空则直接写日志
        if not self.logger.handlers:
            # 给日志器设置总的级别,级别是封装在logging里面的
            # 我要设置错误级别,完全大写
            self.logger.setLevel(logging.INFO)
            # 2.获取格式器
            # 2.1这个只是要输出的样式
            fmt = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d] - %(message)s"
            # 2.2 获取格式器 参数  具体要输出什么样的样式
            fm = logging.Formatter(fmt)
            # 3.获取处理器  按时间切割的文件处理器工作中用midnight  ,backupCount=3  除了原件，只保存最新的三个
            cur_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

            log_path = os.path.join(log__file_path,  cur_date+".log")
            self.tf = logging.handlers.TimedRotatingFileHandler(filename=log_path,
                                                                when='H',
                                                                interval=1,
                                                                backupCount=3,
                                                                encoding='utf-8')

            # 在处理器中添加格式器
            self.tf.setFormatter(fm)
            # 在日志器中添加处理器
            self.logger.addHandler(self.tf)
        return self.logger

if __name__ == '__main__':
    logger= MyLogger().get_log()
    logger.info("aaa")