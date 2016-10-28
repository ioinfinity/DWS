# -*- coding: utf-8 -*-
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import sys

SENDER = 'example@gmail.com'
SENDER_PWD = 'example_password'
RECEIVERS_A = 'example_receiver_a1@gmail.com;example_receiver_a2@gmail.com'
RECEIVERS_B = 'example_receiver_b2@gmail.com;example_receiver_b2@gmail.com'
TARGET_URL = 'https://www.icountry.com.tw'

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
    
def detect_success():
    if url_success(TARGET_URL):
        sender = SENDER
        receivers = RECEIVERS_A
        subject = '心適軒の川月星城官方網站正常運作通知 [週期：每一小時](確認時間:'+ datetime.datetime.now().__str__() + ')'
        message = """\
        <html>
          <head></head>
          <body>
            <p>管理者 您好, <br>
               官方網站正常運作中.<br>
               心適軒の川月星城 官方網站： https://www.icountry.com.tw/starcity/
            </p>
          </body>
        </html>
        """
        send_gmail(sender, receivers, subject, message)
    else:
        detect_failure()
         
def detect_failure(): 
    if not url_success(TARGET_URL):
        sender = SENDER
        receivers = RECEIVERS_B
        subject = '心適軒の川月星城無法登入請技術人員儘快確認 [週期：十分鐘一次](偵測問題時間:'+ datetime.datetime.now().__str__() + ')'
        message = """\
        <html>
          <head></head>
          <body>
            <p>管理者 您好, <br>
               本系統發現官方網站無法正常運作, 請進快聯絡系統負責人協助處理.<br>
               心適軒の川月星城 官方網站： https://www.icountry.com.tw/starcity/
            </p>
          </body>
        </html>
        """
        send_gmail(sender, receivers, subject, message)


def main():
    print(sys.argv[1:][0])
    if sys.argv[1:][0] == 'success':
        detect_success()
    elif sys.argv[1:][0] == 'failure':
        detect_failure()
    else:
        detect_success()
        
    
if __name__ == "__main__":
    # execute only if run as a script
    main()