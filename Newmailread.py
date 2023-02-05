import os.path
import base64
import email
from pickle import TRUE
from email import message_from_binary_file
from selenium import webdriver
from selenium.webdriver.common.by import By
import speech_recognition as sr
import pyttsx3
import pywhatkit
# For Google APIs
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

### If modifying these scopes, delete the file token.json. ###
SCOPES = ['https://mail.google.com/']


class Newmailread:
    def __init__(self):
        """
        Authenticate the google api client and return the service object 
        to make further calls
        Args:
            None
        Returns:
            service api object from Gmail for making calls
        """
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.driver = webdriver.Chrome("chromedriver")
        self.driver.get("https://web.whatsapp.com/")
        listener=sr.Recognizer()
        engine=pyttsx3.init()
        voices=engine.getProperty('voices')
        engine.setProperty('voice',voices[1].id)
        # Call the Gmail API        
        self.service = build('gmail', 'v1', credentials=self.creds)
    def send_msgs(self):
        opt=input("To whom u would like to send\n1.Group\n2.contact\n")
        if opt=="1":
            group=input("__Enter the group name__")
            hour,minu=input("__Enter the time__").split(" ")
            msg=input("__Enter the Text Message__")
            pywhatkit.sendwhatmsg_to_group(group,msg,int(hour),int(minu))
        else:
            contact=input("....Enter the contact u would like to send....")
            hour,minu=input("...Enter the time...").split(" ")
            msg=input("...Enter the Text Message...")
            pywhatkit.sendwhatmsg(contact,msg,int(hour),int(minu))
    def msg(self):
        name=input("\n...Enter Group/User Name:...")
        f=open('bahubali.txt','r')
        message=f.read()
        count=int(input("...Enter the message count:..."))
        user=self.driver.find_element(By.XPATH,'//span[@title="{}"]'.format(name))
        user.click()
        text_box=self.driver.find_element(By.CLASS_NAME,"p3_M1")
        #send button
        for i in range(count):
            text_box.send_keys(message)
            send=self.driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')
            send.click()
        print("Do you want to send more msg to anyone")
        askUser=input("Press y for Yes and n for No")
        if askUser=='y':
            self.msg()
        else:
            print("...Thank you see u soon...")
    def play_vedio(self):
        vedio=input("___Enter the vedio___")
        pywhatkit.playonyt(vedio)
    def get_email(self):
        try:
            # Call the Gmail API
            service = build('gmail', 'v1', credentials=self.creds)
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            if not labels:
                print('No labels found.')
                return
            print('Labels:')
            for label in labels:
                print(label['name'])
            domain=input("enter the domain")
            #get messages
            result = self.service.users().messages().list(userId='me',labelIds=[domain]).execute()
            messages = result.get('messages', [])

            message_count=int(input('how many messages do u want to see from mail?'))
            if not messages:
                print("No messages found")
            else:
                print("Messages:")
                for message in messages[:message_count]:
                    msg=self.service.users().messages().get(userId="me", id=message['id']).execute()
                    print(msg['snippet'])
                    print("\n")
        except:
            pass
            # TODO(developer) - Handle errors from gmail API.
            

    def send_email(self):
        """Create and send an email message
        Print the sent message id
        Args:
            receiver: receiver email
            subject: email subject
            body: email body
        Returns:
            send_email: Message object, including message id
        """
        try:
            message = email.message.EmailMessage()

            # receiver and subject
            emails=input("Enter the email to send")
            subjects=input("enter the subject for send mail")
            message['To'] = emails
            message['Subject'] = subjects

            # message body
            body=input("enter the body for mail")
            message.set_content(body)

            # encoded message
            encoded_message = {
                'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()
            }
            
            send_email = (self.service.users().messages().send(userId="me", body=encoded_message).execute())

        except HttpError as error:
            print(f'An error occurred: {error}')
            send_email = None

        return send_email


    def search_email(self, keyword):
        """
        Search the inbox for emails using standard gmail search parameters
        and return a list of email IDs for each result
        Args:
            keyword: search operators you can use with Gmail
            (see https://support.google.com/mail/answer/7190?hl=en for a list)
        Returns:
            list_ids: list containing email IDs of search query
        """
        try:
            # initiate the list for returning
            #list_ids = []

            # get the id of all messages that are in the search string
            #search_ids = self.service.users().messages().list(userId='me', q=keyword).execute()
            
            # if there were no results, print warning and return empty string
            try:
                domain=input("enter the domain u want to search")
                result = self.service.users().messages().list(userId='me',labelIds=[domain],q=keyword).execute()
                messages = result.get('messages', [])
                message_count=int(input('how many messages do u want to see from mail?'))

                if not messages:
                    print("No messages found")
                else:
                    print("Messages:")
                    for message in messages[:message_count]:
                        msg=self.service.users().messages().get(userId="me", id=message['id']).execute()
                        print(msg['snippet'])
                        print("\n")
            except KeyError:
                print("WARNING: the search queried returned 0 results")
                print("returning an empty string")
                return ""

            # return list of message ids
#            if len(ids)>1:
#               for msg_id in ids:
#                   list_ids.append(msg_id['id'])
#               return(list_ids)
#           else:
#               list_ids = ids[0]['id']
#               return [list_ids]
            
        except HttpError as error:
            print(f'An error in search_email occurred: {error}')


if __name__ == '__main__':

    # service object from the Gmail API
    listener=sr.Recognizer()
    engine=pyttsx3.init()
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    engine.say("Welcome to Our Project")
    engine.runAndWait()
    service = Newmailread()
    while True:
        print("________WELCOME TO OUR PROJECT________")
        action=input("Enter the Action u want to perform\n1.\tSEND EMAIL\n2.\tSEARCH EMAIL\n3.\tGET EMAIL\n4.\tSEND WHATSAPP MSGS TIME\n5.\tSEND MULTIPLE MSGS\n6.\tPLAY VIDEO\n")
        engine.say("Choose your Option")
        engine.runAndWait()
        if action == "1":         # send email
            sent_email = service.send_email()
            print(f'Sent email: {sent_email}')
        elif action == "2":    # search emails
            engine.say("Enter the keyword")
            engine.runAndWait()
            keyword=input("Enter the keyword to search mail from gmail")
            emails_matched = service.search_email(keyword)
            if emails_matched:
                print("Number of emails with keyword '" + str(keyword) + "': " + str(len(emails_matched)))
                print("Email IDs: ", emails_matched)
        elif action=="3":
            engine.say("Frome which domain You want to get mail data")
            engine.runAndWait()
            service.get_email()
        elif action=="4":
            engine.say("now you can njoy with whatsapp")
            engine.runAndWait()
            service.send_msgs()
        elif action=="5":
            engine.say("lets play the funny game with whatsapp")
            engine.runAndWait()
            service.msg()
        elif action=="6":
            engine.say("Enter the vedio you want to play and njoy in youtube")
            engine.runAndWait()
            service.play_vedio()
        else:
            engine.say("Thank you for visiting our project")
            engine.runAndWait()
            print("sorry see you soon")
            break
        
    