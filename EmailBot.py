import smtplib
import imapclient
import email
import re
import time
import random
import threading

def getEmailData(UIDs): # retrives the body of each email 
    body =[]
    string = ''
    for msgid, data in inbox.fetch(UIDs,'RFC822').items():
        email_message = email.message_from_bytes(data[b'RFC822'])
        email_string = email.message_from_string(email_message.as_string()).as_string()
        maintype = email_message.get_content_maintype()
        if maintype == 'multipart':
             for part in email_message.get_payload():
                if part.get_content_type() == 'text/plain':
                    string = part.get_payload()
        elif maintype == 'text/plain':
            string=  email_message.get_payload()
        if string is not '':
            string = string.replace('\n','')
            string = string.replace('\r','')
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

def check(UIDs,body,senders):
    count = 0
    for text in body:
        text = text.lower()
        if('roll a'in text):
            string = text.replace('roll a ','')
            string = string.replace('sided die','')
            string = string.strip()
            message ="You rolled a "+ str(random.randint(1,int(string)))
            mail.sendmail(username,senders[count],"Subject: Dice Roll\n"+message)
        elif('roll' in text):
            print("a roll occured")
            message ="You rolled a "+ str(random.randint(1,6))
            mail.sendmail(username,senders[count],"Subject: Dice Roll\n"+message)
        elif('remind me' in text):
            match = re.search('remind me in (.*) about (.*)',text)
            event = match.group(2)
            number = int(re.search(r'\d',match.group(1)).group())
            if('days' in match.group(1)):
                number*=3600
            elif('hours' in match.group(1)):
                number*=60
            x = threading.Thread(target=Event, args=(event,number,senders[count],))
            print("reminder from "+ senders[count])
            Threads.append(x)
            x.start()
        inbox.delete_messages(UIDs[count])
        count+=1

def Event(name,waittime,sendee):
    time.sleep(int(waittime*60))
    mail.sendmail(username,sendee,"Subject: Autamated Reminder\nThis is a reminder about"+name)
    
        
        
username = input("username")
password = input("password")
mail, inbox = login(username,password)

Threads = []
while True:
    UIDs = getInbox(inbox)
    body = getEmailData(UIDs)
    senders = getSender(UIDs)
    print('1',UIDs,"\n2",senders,"\n3",body)
    check(UIDs,body,senders)
    time.sleep(int(10))
logout(mail,inbox)
