'''
Created on Sep 15, 2017

@author: duncan
'''
import smtplib

def send_mail(body_message,sender,to,subject=None):
        server = smtplib.SMTP('smtpserver:port')
        server.ehlo()
        server.starttls()
        server.login('username','password')
        msg = "\r\n".join([
          "From: %s",
          "To: %s",
          "Subject: %s",
          "",
          "%s"
          ] )%(sender,to,subject,body_message)
        server.sendmail(sender, to, msg)
        server.quit()


    

