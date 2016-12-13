# -*- coding: utf-8 -*-
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import sys

from distutils.dir_util import copy_tree

SENDER = ''
SENDER_PWD = ''
RECEIVERS = ''
TARGET_URL = ''

DISTINATION_FOLDER_A = '/var/www/html/starcity'
DISTINATION_FOLDER_B = '/var/www/html/sweetheart'
BnBPath_A_FOLDER_R = '/var/www/html/bitbucket/bootstrap-official-website-for-sweetheart-and-starcity/war/starcity'
BnBPath_A_FOLDER_U = '/var/www/html/bitbucket_title/bootstrap-official-website-for-sweetheart-and-starcity/war/starcity'
BnBPath_B_FOLDER_R = '/var/www/html/bitbucket/bootstrap-official-website-for-sweetheart-and-starcity/war/sweetheart'
BnBPath_B_FOLDER_U = '/var/www/html/bitbucket_title/bootstrap-official-website-for-sweetheart-and-starcity/war/sweetheart'


def url_success(url):
    r = requests.head(url)
    return r.status_code == 200

def send_gmail(sender, receivers, subject, message):
    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server_ssl.ehlo() # optional, called by login()
    server_ssl.login(SENDER, SENDER_PWD)  
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receivers
    msg['Subject'] = subject
    content = MIMEText(message, 'html')
    msg.attach(content)
    
    # ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
    server_ssl.sendmail(sender, receivers, msg.as_string())
    #server_ssl.quit()
    server_ssl.close()
    
def update_bnb_official_title():
    result_A = copyDirectory(BnBPath_A_FOLDER_U, DISTINATION_FOLDER_A)
    result_B = copyDirectory(BnBPath_B_FOLDER_U, DISTINATION_FOLDER_B)
    if result_A and result_B:
        sender = SENDER
        receivers = RECEIVERS
        subject = '[正向更新]心適軒の川月星城官方網站標題修改通知[週期：每五分鐘](確認時間:'+ datetime.datetime.now().__str__() + ')'
        message = """\
            <html>
            <head></head>
            <body>
            <p>管理者 您好, <br>
                自動定期更新官方網站標題,測試是否可以提昇Google搜尋尋排行順序.<br>
                心適軒の川月星城 官方網站： https://www.icountry.com.tw/starcity/
            </p>
            </body>
            </html>
        """
        send_gmail(sender, receivers, subject, message) 
       
    
def reverse_update_bnb_official_title():
    result_A = copyDirectory(BnBPath_A_FOLDER_R, DISTINATION_FOLDER_A)
    result_B = copyDirectory(BnBPath_B_FOLDER_R, DISTINATION_FOLDER_B)
    if result_A and result_B:
        sender = SENDER
        receivers = RECEIVERS
        subject = '[反向更新]心適軒の川月星城官方網站標題修改通知[週期：每五分鐘](確認時間:'+ datetime.datetime.now().__str__() + ')'
        message = """\
            <html>
            <head></head>
            <body>
            <p>管理者 您好, <br>
                自動定期更新官方網站標題,測試是否可以提昇Google搜尋尋排行順序.<br>
                心適軒の川月星城 官方網站： https://www.icountry.com.tw/starcity/
            </p>
            </body>
            </html>
        """
        send_gmail(sender, receivers, subject, message)   
    
def fail_update_bnb_official_title():
    sender = SENDER
    receivers = RECEIVERS
    subject = '[更新失敗通知]心適軒の川月星城官方網站標題修改通知[週期：每五分鐘](確認時間:'+ datetime.datetime.now().__str__() + ')'
    message = """\
        <html>
        <head></head>
        <body>
        <p>管理者 您好, <br>
            官方網站標題自動定期更新失敗.<br>
            心適軒の川月星城-官方網站： https://www.icountry.com.tw/starcity/<br>
            心適軒-官方網站： https://www.icountry.com.tw/sweetheart/<br>
        </p>
        </body>
        </html>
    """
    send_gmail(sender, receivers, subject, message)  
    
def copyDirectory(src, dest):
    try:
        copy_tree(src, dest)
        return True
    # Directories are the same
    except :
        print('Directory not copied. Error.')
        fail_update_bnb_official_title()
        return False


def main():
    print(sys.argv[1:][0])
    if sys.argv[1:][0] == 'update':
        update_bnb_official_title()
    elif sys.argv[1:][0] == 'reverse':
        reverse_update_bnb_official_title()
        
if __name__ == "__main__":
    # execute only if run as a script
    main()