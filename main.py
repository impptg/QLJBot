from selenium import webdriver
from time import sleep
import string
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import schedule

login_url = 'http://gba.bjtu.edu.cn/login?redirect=%2Factivity%2Flist'

mail_server = 'smtp.qq.com'
mail_from = '1493173244@qq.com'
mail_pswd = ''
mail_to = '21125166@bjtu.edu.cn'

# 正文
msg = MIMEText('害嗨嗨，有新的会议咯，快抢', 'plain', 'utf-8')
msg['From'] = Header('QLJBot')
msg['To'] = Header('21125166')
msg['Subject'] = Header('新会议', 'utf-8')

cntPre = 0


def sendMail():
    try:
        # 连接
        smtpobj = smtplib.SMTP_SSL(mail_server)
        smtpobj.connect(mail_server, 465)

        # 登录
        smtpobj.login(mail_from, mail_pswd)

        # 发送
        smtpobj.sendmail(mail_from, mail_to, msg.as_string())
        print("邮件发送成功")

    except smtplib.SMTPException:
        print()
        print("无法发送邮件")

    finally:
        # 关闭
        smtpobj.quit()


def refreshCount():
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')

    browser = webdriver.Chrome(chrome_options=option)
    browser.get(login_url)

    userInfo = browser.find_elements_by_class_name('el-input__inner')
    sleep(1)
    userInfo[0].send_keys("21125166")

    sleep(1)
    userInfo[1].send_keys("")

    sleep(1)
    loginBtn = browser.find_element_by_class_name("el-button--primary")
    loginBtn.click()

    sleep(2)
    countInfo = browser.find_element_by_class_name('el-pagination__total').text
    countNum = string.atoi(''.join(x for x in countInfo if x.isdigit()))
    return countNum


def job():
    cntNow = refreshCount()
    if cntNow > cntPre:
        sendMail()


if __name__ == '__main__':
    # 获取初始 Cnt
    cntPre = refreshCount()

    # 定义循环任务
    schedule.every(5).seconds.do(job)
    while True:
        schedule.run_pending()
