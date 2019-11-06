import smtplib
import imapclient
import email
import re
import time
import random
def getEmailData(UIDs): # retrives the body of each email 
    body =[]
    for msgid, data in inbox.fetch(UIDs,'RFC822').items():
        email_message = email.message_from_bytes(data[b'RFC822']).as_string()
        email_string = email.message_from_string(email_message).as_string()
        #print(email_string)
        begin = email_string.find('Content-Type: text/plain; charset="UTF-8"')+41
        end = email_string.find('Content-Type: text/html; charset="UTF-8"')-31
        string = email_string[begin:end]
        string = string.strip().replace("\n"," ")
        body.append(string)
    return body


def getSender(UIDs): # retrieves the list of senders 
    senders = [] 
    email_parser = re.compile(r'From: (.*) <(.*)>')
    for msgid, data in inbox.fetch(UIDs,'RFC822').items():
        email_message = email.message_from_bytes(data[b'RFC822']).as_string()
        email_string = email.message_from_string(email_message).as_string()
        g = email_parser.search(email_string).group()
        start = str(g).find('<')+1
        end = str(g).find('>')
        g = g[start:end]
        senders.append(g)
    return senders


def login(username,password): #all necessary logins 
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(username,password)
    inbox = imapclient.IMAPClient('imap.gmail.com',ssl=True)
    inbox.login(username,password)
    return mail,inbox

def logout(mail,inbox):
    mail.quit()
    inbox.logout()
    


#mail.sendmail(username, username,"Message")

def getInbox(inbox):
    inbox.select_folder('INBOX',readonly=False)
    UIDs = inbox.search()
    return UIDs

def roll(UIDs,body,senders):
    count = 0
    for text in body:
        if('roll' in text):
            print("a roll occured")
            message ="You rolled a "+ str(random.randint(1,6))
            mail.sendmail(username,senders[count],"Subject: Dice Roll\n"+message)
            inbox.delete_messages(UIDs[count])
        count+=1


username = input("username:")
password = input("password:")
mail, inbox = login(username,password)

while True:
    UIDs = getInbox(inbox)
    body = getEmailData(UIDs)
    senders = getSender(UIDs)
    print('1',UIDs,"\n2",senders,"\n3",body)
    roll(UIDs,body,senders)
    time.sleep(int(15))
logout(mail,inbox)
