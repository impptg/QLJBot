from selenium import webdriver
from time import sleep
import string
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import schedule
import config

login_url = 'http://gba.bjtu.edu.cn/login?redirect=%2Factivity%2Flist'

# 正文
msg = MIMEText('害嗨嗨，有新的会议咯，快抢', 'plain', 'utf-8')
msg['From'] = Header('QLJBot')
msg['To'] = Header('21125166')
msg['Subject'] = Header('新会议', 'utf-8')

cntPre = 0


def sendMail():
    try:
        # 连接
        smtpobj = smtplib.SMTP_SSL(config.mail_server, config.mail_port)
        # 登录
        smtpobj.login(config.mail_from, config.mail_pswd)
        # 发送
        smtpobj.sendmail(config.mail_from, config.mail_to, msg.as_string())
        print("邮件发送成功")

    except smtplib.SMTPException:
        print("无法发送邮件")

    finally:
        # 关闭
        smtpobj.quit()


def refreshCount():
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    option.add_argument('--headless')

    browser = webdriver.Chrome(chrome_options=option)
    browser.get(login_url)

    # 账号密码
    userInfo = browser.find_elements_by_class_name('el-input__inner')
    sleep(1)
    userInfo[0].send_keys(config.login_user)

    sleep(1)
    userInfo[1].send_keys(config.login_pswd)

    # 登陆
    sleep(1)
    loginBtn = browser.find_element_by_class_name("el-button--primary")
    loginBtn.click()

    # 最新活动数
    sleep(2)
    countInfo = browser.find_element_by_class_name('el-pagination__total').text
    countNum = int(''.join(x for x in countInfo if x.isdigit()))
    return countNum


def refreshJob():
    print("refreshJob")
    cntNow = refreshCount()
    cntPre = cntNow
    if cntNow > cntPre:
        sendMail()


def liveJob():
    sendMail()
    print("liveJob")


if __name__ == '__main__':
    # 获取初始 Cnt
    cntPre = refreshCount()

    # 2 小时刷新一次
    schedule.every(1).hours.do(refreshJob)
    # 每天 12 点判断服务是不是挂了
    schedule.every().day.at("12:00").do(liveJob)
    while True:
        schedule.run_pending()
