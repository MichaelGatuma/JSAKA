'''
Created on Sep 15, 2017

@author: duncan
'''
import smtplib

def send_mail(body_message,sender,to,subject=None):
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login('duncanndiithi@gmail.com','elizabeth@wairimu26')
        msg = "\r\n".join([
          "From: %s",
          "To: %s",
          "Subject: %s",
          "",
          "%s"
          ] )%(sender,to,subject,body_message)
        server.sendmail(sender, to, msg.encode('utf-8').strip())
        server.quit()


    

