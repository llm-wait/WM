import smtplib
import time
#邮件发送的用户名和密码，第三方授权码
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

_username="1617542130@qq.com"
_pwd="vmutzcyvrzltdgjh"
now=time.strftime("%Y-%m-%d_%H_%M_%S")
class SendEmail():
    def send_email(self,email_to,filepath):
        """
        email_to:收件方
        filepath:发送的附件地址
        :return:
        """
        msg=MIMEMultipart()#生成邮件对象
        msg["subject"]=now+"业务管理系统测试报告"   #设置邮件主题
        msg["From"]=_username    #设置发件人
        msg["To"]=email_to           #设置收件人
        #设置正文
        part=MIMEText("这是自动化测试结果请查收")
        msg.attach(part)
        #设置附件部分内容
        part=MIMEApplication(open(filepath,'rb').read())
        part.add_header("Content-Disposition","attachment",filename=filepath)
        msg.attach(part)
        s=smtplib.SMTP_SSL("smtp.qq.com",timeout=30)#连接smtp服务器，超时时间默认是25s
        s.login(_username,_pwd)#登录服务器
        s.sendmail(_username,email_to,msg.as_string())#发送邮件
        s.close()
if __name__ == '__main__':
    filepath=r"E:\python-work\Postman\report\result_2020-11-26_16_12_55.html"
    SendEmail().send_email("1617542130@qq.com",filepath)





