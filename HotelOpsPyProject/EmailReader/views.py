from django.shortcuts import render,redirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.contrib import messages
from pathlib import Path
import datetime
import re
import win32com.client
from django.shortcuts import render, redirect
from .models import Resume,Designation,EmailMessage

import PyPDF2
import docx2txt
import os
import PyPDF2
import pytesseract
from PIL import Image
import re
import fitz
from .azure import upload_file_to_blob,download_blob
from django.http import HttpResponse,Http404
import mimetypes
import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import uuid
import random
import string
from datetime import date
def TestEmail(request):
    # Define your email credentials
    # #username = "resumes@nilehospitality.com"
    username = "nileresumes@outlook.com"
    password = "Vishal@7990"
    # Define the IMAP server and port
    imap_server = "outlook.office365.com"  # Update with your email provider's IMAP server
    imap_port = 993

    # Connect to the IMAP server using SSL
    imap = imaplib.IMAP4_SSL(imap_server, imap_port)

    # Log in to your email account
    imap.login(username, password)

    # Select the mailbox you want to retrieve emails from
    mailbox = "INBOX"  # You can change this to the desired mailbox
    imap.select(mailbox)

    # Define the target date (e.g., today)
    target_date = datetime.datetime.today().date()

    # Directory to save email attachments
    output_dir = r"C:\Emails"

    # Clear the output directory
    for root, dirs, files in os.walk(output_dir, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))

    # Search for email messages based on criteria (e.g., all emails received today)
    status, data = imap.search(None, f'(SINCE "{target_date.strftime("%d-%b-%Y")}")')

    if status == "OK":
        message_numbers = data[0].split()
        print(message_numbers)
        for num in message_numbers:
            # Fetch the email message
            status, msg_data = imap.fetch(num, "(RFC822)")
            
            if status == "OK":
                msg = email.message_from_bytes(msg_data[0][1])
                
                # Extract sender information
                From, encoding = decode_header(msg.get("From"))[0]
                if From is not None:
                    From = From
                else:
                    From = "Unknown Sender"
                
                # Process the email message as needed
                # For example, save attachments or perform other operations

                # Print sender and subject for demonstration
                print("Sender:", From)
                print("Subject:", msg.get("Subject"))

    # Logout and close the connection
    imap.logout()
    # # account credentials
    # #username = "resumes@nilehospitality.com"
    # username = "nileresumes@outlook.com"
    # password = "Vishal@7990"
    # # use your email provider's IMAP server, you can look for your provider's IMAP server on Google
    # # or check this page: https://www.systoolsgroup.com/imap/
    # # for office 365, it's this:
    # # imap_server = "outlook.office365.com"


    # def clean(text):
    #     # clean text for creating a folder
    #     return "".join(c if c.isalnum() else "_" for c in text)

    # # number of top emails to fetch
    # N = 3

    # # create an IMAP4 class with SSL, use your email provider's IMAP server
    # #imap = imaplib.IMAP4_SSL(imap_server)
    # # imap = imaplib.IMAP4_SSL(imap_server)
    # imap_server = 'outlook.office365.com'
    # imap_port = 993

    # # Create an IMAP4_SSL instance with TLS encryption
    # imap = imaplib.IMAP4_SSL(imap_server, imap_port)
    # # authenticate
    # imap.login(username, password)

    # # select a mailbox (in this case, the inbox mailbox)
    # # use imap.list() to get the list of mailboxes
    # response, mailbox_list = imap.list()
    # if response == 'OK':
    #     for mailbox in mailbox_list:
    #         # Parse the mailbox name
    #         mailbox_name = mailbox.decode('utf-8').split(' "/" ')[1]
    #         print("Mailbox Name:", mailbox_name)
    #         status, messages = imap.select(mailbox_name)

    #         # total number of emails
    #         messages = int(messages[0])
    #         print("messages Count")
    #         print(messages)
    #         messages=10
    #         #for i in range(messages, messages-N, -1):
    #         for i in range(messages, messages-N, -1):
    #             # fetch the email message by ID
    #             res, msg = imap.fetch(str(i), "(RFC822)")
    #             for response in msg:
                    
    #                 if isinstance(response, tuple):
    #                     # parse a bytes email into a message object
    #                     msg = email.message_from_bytes(response[1])
    #                     # decode the email subject
    #                     subject, encoding = decode_header(msg["Subject"])[0]
    #                     if isinstance(subject, bytes):
    #                         # if it's a bytes, decode to str
    #                         subject = subject.decode(encoding)
    #                     # decode email sender
    #                     From, encoding = decode_header(msg.get("From"))[0]
    #                     if isinstance(From, bytes):
    #                         From = From.decode(encoding)
    #                     print("Subject:", subject)
    #                     print("From:", From)
    #                     # if the email message is multipart
    #                     if msg.is_multipart():
    #                         # iterate over email parts
    #                         for part in msg.walk():
    #                             # extract content type of email
    #                             content_type = part.get_content_type()
    #                             content_disposition = str(part.get("Content-Disposition"))
    #                             try:
    #                                 # get the email body
    #                                 body = part.get_payload(decode=True).decode()
    #                             except:
    #                                 pass
    #                             if content_type == "text/plain" and "attachment" not in content_disposition:
    #                                 # print text/plain emails and skip attachments
    #                                 print(body)
    #                             elif "attachment" in content_disposition:
    #                                 # download attachment
    #                                 filename = part.get_filename()
    #                                 if filename:
    #                                     folder_name = clean(subject)
    #                                     if not os.path.isdir(folder_name):
    #                                         # make a folder for this email (named after the subject)
    #                                         os.mkdir(folder_name)
    #                                     filepath = os.path.join(folder_name, filename)
    #                                     # download attachment and save it
    #                                     open(filepath, "wb").write(part.get_payload(decode=True))
    #                     else:
    #                         # extract content type of email
    #                         content_type = msg.get_content_type()
    #                         # get the email body
    #                         body = msg.get_payload(decode=True).decode()
    #                         if content_type == "text/plain":
    #                             # print only text email parts
    #                             print(body)
    #                     if content_type == "text/html":
    #                         # if it's HTML, create a new HTML file and open it in browser
    #                         folder_name = clean(subject)
    #                         if not os.path.isdir(folder_name):
    #                             # make a folder for this email (named after the subject)
    #                             os.mkdir(folder_name)
    #                         filename = "index.html"
    #                         filepath = os.path.join(folder_name, filename)
    #                         # write the file
    #                         open(filepath, "w").write(body)
    #                         # open in the default browser
    #                         webbrowser.open(filepath)
    #                     print("="*100)
    #     # close the connection and logout
    # imap.close()
    # imap.logout()
    context= {'resume_lists':[]}
    return render(request,"emailtemp/TestEmail.html",context)
def generate_unique_id():
    # Define the characters to use for the ID
    characters = string.ascii_letters + string.digits  # You can include other characters if needed

    # Generate a random string
    length = 6  # Change the length as needed
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    # Get the current date in YYYYMMDD format
    current_date = date.today().strftime("%Y%m%d")

    # Concatenate the random string and date to create a unique ID
    unique_id = f"{current_date}-{random_string}"

    # You can check the uniqueness of this ID in your database before using it
    # Ensure it doesn't clash with existing IDs if uniqueness is critical

    # You can check the uniqueness of this ID in your database before using it
    # Ensure it doesn't clash with existing IDs if uniqueness is critical

    return unique_id

import pythoncom
def download_email_data_new(request):
    target_date = datetime.datetime.today()
    output_dir = r"C:\Emails"
    data_found = False
    for root, dirs, files in os.walk(output_dir, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
 
    try:
        # Initialize COM using CoInitializeEx
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
 
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
 
        inbox = outlook.GetDefaultFolder(6)
        email_messages = inbox.Items
        for email_message in email_messages:
            print("emailMessage")
            print(email_message)
            

            received_date = email_message.ReceivedTime
            recipients = email_message.Recipients
 
            if received_date.date() == target_date.date():
                data_found = True
                attachments = email_message.Attachments
                recipients = email_message.Recipients
                for recipient in recipients:
                    recipient_email_address = recipient.Address
                    print(recipient_email_address)
 
                for attachment in attachments:
                    original_filename = attachment.FileName
 
                    sanitized_filename = re.sub(r'[\\/:"*?<>|]+', '', original_filename)
                    output_path = os.path.join(output_dir, sanitized_filename)
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    attachment.SaveAsFile(output_path)
 
        if not data_found:
            messages.error(request, "No data found for the previous date.")
        else:
            messages.success(request, "Emails Downloaded Successfully")
    except Exception as e:
        # Handle exceptions appropriately
        print(f"Error: {e}")
        messages.error(request, f"Error: {e}")
    finally:
        # Uninitialize COM using CoUninitialize
        pythoncom.CoUninitialize()
 
    return redirect('resume_list')

from pywintypes import com_error
import shutil

import pythoncom
import win32com.client
import os
import re
import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from pythoncom import com_error
import keyboard

# def downloadEmails():
#     try:
#         folder_path = r"C:\Emails"
#         if os.path.exists(folder_path):
#             shutil.rmtree(folder_path)
        
#         os.makedirs(folder_path, exist_ok=True)
#         pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
#         target_date = datetime.datetime.today()
#         selected_account_name = ["darpan.anjanay@nilehospitality.com"]
#         #selected_account_name = [ "career.giftcityclub@radissonindividuals.com","career.upn@radissonindividuals.com","rajshree.ranawat@hyatt.com"]
#         for emailAccount in selected_account_name:
#             output_dir = r"C:\Emails"
#             data_found = False

#             # Remove all files in the output directory
#             # for root, dirs, files in os.walk(output_dir, topdown=False):
#             #     for file in files:
#             #         os.remove(os.path.join(root, file))

#             outlook = win32com.client.Dispatch("Outlook.Application")
#             namespace = outlook.GetNamespace("MAPI")

#             try:
#                 selected_account = namespace.Folders(emailAccount)
#             except com_error as e:
#                 print(f"Error accessing folder '{emailAccount}': {e}")

#             for folder in selected_account.Folders:
#                 print("Mailbox:", folder)
#                 email_messages = folder.Items
#                 keyboard.press_and_release('down')
#                 for email_message in email_messages:
#                     try:
#                         keyboard.press_and_release('down')
#                         received_date = email_message.ReceivedTime
#                         if received_date.date()  >= target_date.date():#>= datetime.date(2022, 12, 1):
#                             print("Processing email_message")
#                             print(email_message.EntryID)

#                             recipients_to = email_message.To
#                             Subject = email_message.Subject
#                             Sender = email_message.Sender
#                             ReceivedTime = email_message.ReceivedTime

#                             if recipients_to:
#                                 for recipient in recipients_to.split(";"):
#                                     recipient_email_address = recipient.strip()
#                                     print("Recipient in 'To' field:", recipient_email_address)

#                             objEmailMessage = EmailMessage(MessageID=email_message.EntryID, To=recipients_to,
#                                                           Subject=Subject, Sender=Sender, ReceivedTime=ReceivedTime)
#                             objEmailMessage.save()
#                             data_found = True

#                             attachments = email_message.Attachments

#                             for attachment in attachments:
#                                 original_filename = attachment.FileName
#                                 new_output_path = os.path.join(output_dir, email_message.EntryID)
#                                 sanitized_filename = re.sub(r'[\\/:"*?<>|]+', '', original_filename)
#                                 new_output_path = os.path.join(new_output_path, sanitized_filename)
#                                 os.makedirs(os.path.dirname(new_output_path), exist_ok=True)
#                                 attachment.SaveAsFile(new_output_path)

#                     except Exception as e:
#                         print(f"Error processing email_message: {e}")
#                         # continue

#             if not data_found:
#                 print("No data found for today.")
#             else:
#                 print( "Emails Downloaded Successfully")

#     except Exception as e:
#         print(f"Unexpected error: {e}")

#     finally:
#         # Uninitialize COM using CoUninitialize
#         pythoncom.CoUninitialize()


from datetime import datetime, timedelta
# import os
# import shutil
# import pythoncom
# import win32com.client
# import re
# class EmailMessage:
#     def __init__(self, MessageID, To, Subject, Sender, ReceivedTime):
#         self.MessageID = MessageID
#         self.To = To
#         self.Subject = Subject
#         self.Sender = Sender
#         self.ReceivedTime = ReceivedTime

#     def save(self):
        
#         print("Saving email message:", self.MessageID)


# def downloadEmails():
#     try:
#         folder_path = r"C:\Emails"
#         if os.path.exists(folder_path):
#             shutil.rmtree(folder_path)
        
#         os.makedirs(folder_path, exist_ok=True)
#         pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
#         target_date = datetime.today()
#         selected_account_name = ["darpan.anjanay@nilehospitality.com"]
#         # selected_account_name = ["careers@nilehospitality.com", "career.giftcityclub@radissonindividuals.com","career.upn@radissonindividuals.com","rajshree.ranawat@hyatt.com"]
#         #selected_account_name = [ "career.giftcityclub@radissonindividuals.com","career.upn@radissonindividuals.com","rajshree.ranawat@hyatt.com"]
#         for emailAccount in selected_account_name:
#             output_dir = r"C:\Emails"
#             data_found = False

#             outlook = win32com.client.Dispatch("Outlook.Application")
#             namespace = outlook.GetNamespace("MAPI")

#             try:
#                 selected_account = namespace.Folders(emailAccount)
#             except Exception as e:
#                 print(f"Error accessing folder '{emailAccount}': {e}")

#             for folder in selected_account.Folders:
#                 # Skip non-mail folders
#                 if folder.DefaultItemType != 0:  # 0 indicates mail items
#                     continue

#                 print("Mailbox:", folder)
              
#                 filter_str = f"[ReceivedTime] >= '{target_date.strftime('%m/%d/%Y')}' AND [ReceivedTime] < '{(target_date + timedelta(days=1)).strftime('%m/%d/%Y')}'"
#                 email_messages = folder.Items.Restrict(filter_str)
                
#                 for email_message in email_messages:
#                     try:
#                         received_date = email_message.ReceivedTime
#                         if received_date.date() == target_date.date():
#                             print("Processing email_message")
#                             print(email_message.EntryID)

#                             recipients_to = email_message.To
#                             Subject = email_message.Subject
#                             Sender = email_message.Sender
#                             ReceivedTime = email_message.ReceivedTime

#                             if recipients_to:
#                                 for recipient in recipients_to.split(";"):
#                                     recipient_email_address = recipient.strip()
#                                     print("Recipient in 'To' field:", recipient_email_address)

#                             objEmailMessage = EmailMessage(MessageID=email_message.EntryID, To=recipients_to,
#                                                           Subject=Subject, Sender=Sender, ReceivedTime=ReceivedTime)
#                             objEmailMessage.save()
#                             data_found = True

#                             attachments = email_message.Attachments

#                             for attachment in attachments:
#                                 original_filename = attachment.FileName
#                                 new_output_path = os.path.join(output_dir, email_message.EntryID)
#                                 sanitized_filename = re.sub(r'[\\/:"*?<>|]+', '', original_filename)
#                                 new_output_path = os.path.join(new_output_path, sanitized_filename)
#                                 os.makedirs(os.path.dirname(new_output_path), exist_ok=True)
#                                 attachment.SaveAsFile(new_output_path)

#                     except Exception as e:
#                         print(f"Error processing email_message: {e}")

#             if not data_found:
#                 print("No data found for today.")
#             else:
#                 print("Emails Downloaded Successfully")

#     except Exception as e:
#         print(f"Unexpected error: {e}")

#     finally:
#         # Uninitialize COM using CoUninitialize
#         pythoncom.CoUninitialize()




# def downloadEmails(start_date, end_date):
#     try:
#         folder_path = r"C:\Emails"
#         if os.path.exists(folder_path):
#             shutil.rmtree(folder_path)
        
#         os.makedirs(folder_path, exist_ok=True)
#         pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        
#         # Make start_date and end_date naive
#         start_date = start_date.replace(tzinfo=None)
#         end_date = end_date.replace(tzinfo=None)
        
#         selected_account_name = ['darpan.anjanay@nilehospitality.com']
#         for emailAccount in selected_account_name:
#             output_dir = r"C:\Emails"
#             data_found = False
            
#             outlook = win32com.client.Dispatch("Outlook.Application")
#             namespace = outlook.GetNamespace("MAPI")

#             try:
#                 selected_account = namespace.Folders(emailAccount)
#             except com_error as e:
#                 print(f"Error accessing folder '{emailAccount}': {e}")

#             for folder in selected_account.Folders:
#                 print("Mailbox:", folder)
#                 email_messages = folder.Items
#                 keyboard.press_and_release('down')
#                 for email_message in email_messages:
#                     try:
#                         keyboard.press_and_release('down')
#                         received_date = email_message.ReceivedTime
#                         received_date = received_date.replace(tzinfo=None)  # Make received_date naive
#                         if start_date <= received_date <= end_date:
#                             print("Processing email_message")
#                             print(email_message.EntryID)

#                             recipients_to = email_message.To
#                             Subject = email_message.Subject
#                             Sender = email_message.Sender
#                             ReceivedTime = email_message.ReceivedTime

#                             if recipients_to:
#                                 for recipient in recipients_to.split(";"):
#                                     recipient_email_address = recipient.strip()
#                                     print("Recipient in 'To' field:", recipient_email_address)

#                             objEmailMessage = EmailMessage(MessageID=email_message.EntryID, To=recipients_to,
#                                                           Subject=Subject, Sender=Sender, ReceivedTime=ReceivedTime)
#                             objEmailMessage.save()
#                             data_found = True

#                             attachments = email_message.Attachments

#                             for attachment in attachments:
#                                 original_filename = attachment.FileName
#                                 new_output_path = os.path.join(output_dir, email_message.EntryID)
#                                 sanitized_filename = re.sub(r'[\\/:"*?<>|]+', '', original_filename)
#                                 new_output_path = os.path.join(new_output_path, sanitized_filename)
#                                 os.makedirs(os.path.dirname(new_output_path), exist_ok=True)
#                                 attachment.SaveAsFile(new_output_path)

#                     except Exception as e:
#                         print(f"Error processing email_message: {e}")
#                         # continue

#             if not data_found:
#                 print("No data found for the specified date range.")
#             else:
#                 print("Emails Downloaded Successfully")

#     except Exception as e:
#         print(f"Unexpected error: {e}")

#     finally:
#         # Uninitialize COM using CoUninitialize
#         pythoncom.CoUninitialize()




# class EmailMessage:
#     def __init__(self, MessageID, To, Subject, Sender, ReceivedTime):
#         self.MessageID = MessageID
#         self.To = To
#         self.Subject = Subject
#         self.Sender = Sender
#         self.ReceivedTime = ReceivedTime

#     def save(self):
#         print("Saving email message:", self.MessageID)


def downloadEmails(start_date=None, end_date=None):
    try:
        folder_path = r"C:\Emails"
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        os.makedirs(folder_path, exist_ok=True)
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)

        selected_account_name = ["darpan.anjanay@nilehospitality.com"]
        # selected_account_name = ["careers@nilehospitality.com", "career.giftcityclub@radissonindividuals.com","career.upn@radissonindividuals.com","rajshree.ranawat@hyatt.com"]
        #selected_account_name = [ "career.giftcityclub@radissonindividuals.com","career.upn@radissonindividuals.com","rajshree.ranawat@hyatt.com"]
        for emailAccount in selected_account_name:
            output_dir = r"C:\Emails"
            data_found = False

            outlook = win32com.client.Dispatch("Outlook.Application")
            namespace = outlook.GetNamespace("MAPI")

            try:
                selected_account = namespace.Folders(emailAccount)
            except Exception as e:
                print(f"Error accessing folder '{emailAccount}': {e}")

            for folder in selected_account.Folders:
                # Skip non-mail folders
                if folder.DefaultItemType != 0:  # 0 indicates mail items
                    continue

                print("Mailbox:", folder)
              
                filter_str = f"[ReceivedTime] >= '{start_date.date().strftime('%m/%d/%Y')}' AND [ReceivedTime] < '{(end_date.date() + timedelta(days=1)).strftime('%m/%d/%Y')}'"
                email_messages = folder.Items.Restrict(filter_str)
                
                for email_message in email_messages:
                    try:
                        received_date = email_message.ReceivedTime
                        if start_date.date() <= received_date.date() <= end_date.date():
                            print("Processing email_message")
                            print(email_message.EntryID)

                            recipients_to = email_message.To
                            Subject = email_message.Subject
                            Sender = email_message.Sender
                            ReceivedTime = email_message.ReceivedTime

                            if recipients_to:
                                for recipient in recipients_to.split(";"):
                                    recipient_email_address = recipient.strip()
                                    print("Recipient in 'To' field:", recipient_email_address)

                            objEmailMessage = EmailMessage(MessageID=email_message.EntryID, To=recipients_to,
                                                          Subject=Subject, Sender=Sender, ReceivedTime=ReceivedTime)
                            objEmailMessage.save()
                            data_found = True

                            attachments = email_message.Attachments

                            for attachment in attachments:
                                original_filename = attachment.FileName
                                new_output_path = os.path.join(output_dir, email_message.EntryID)
                                sanitized_filename = re.sub(r'[\\/:"*?<>|]+', '', original_filename)
                                new_output_path = os.path.join(new_output_path, sanitized_filename)
                                os.makedirs(os.path.dirname(new_output_path), exist_ok=True)
                                attachment.SaveAsFile(new_output_path)

                    except Exception as e:
                        print(f"Error processing email_message: {e}")

            if not data_found:
                print("No data found within the specified date range.")
            else:
                print("Emails Downloaded Successfully")

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        # Uninitialize COM using CoUninitialize
        pythoncom.CoUninitialize()


def upload_EmailData():
    
    output_dir = r"C:\Emails"
    if os.path.exists(output_dir) and os.path.isdir(output_dir):
        files = os.listdir(output_dir)
        for folder in files:
            folderPath=os.path.join(output_dir, folder)
            foldersfiles = os.listdir(folderPath)
            for file in foldersfiles:
                try:
                    file_path = os.path.join(folderPath, file)
                    #file_path = os.path.join(folderPath, file)
                    if os.path.isfile(file_path) and any(file_path.lower().endswith(ext) for ext in SUPPORTED_FORMATS):
                            print(file_path)
                            try:
                                text, images = process_file(file_path)
                                emails, phone_numbers = extract_emails_and_phone_numbers(text)
                                    
                                original_filename, _ = os.path.splitext(file)
                                name = original_filename.replace("_", " ")
                                file_name = file
                                # Create a new Resume entry
                                resume = Resume(MessageID=folder,name=name, file_name=file_name, email=emails[0] if emails else '', phone_number=phone_numbers[0] if phone_numbers else '')
                                resume.save()
                                resume.designation.add(*extract_designation(text))
                                with open(file_path, 'rb') as file:    
                                    id = resume.id
                                    new_file = upload_file_to_blob(file,id)
                            
                            except:
                                    print("Error")
                except:
                                    print("Error")

       

    # return redirect('resume_list')



def download_email_data():

    for root, dirs, files in os.walk("C:\Emails", topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)

# Remove all directories
    shutil.rmtree("C:\Emails")
    try:
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        target_date = datetime.today()
        selected_account_name = ["careers@nilehospitality.com","career.giftcityclub@radissonindividuals.com","career.upn@radissonindividuals.com","rajshree.ranawat@hyatt.com"]
        #selected_account_name = ["rajshree.ranawat@hyatt.com"]
        # selected_account_name = ["careers@nilehospitality.com"]
        for emailAccount in selected_account_name:
            output_dir = r"C:\Emails"
            data_found = False
            # for root, dirs, files in os.walk(output_dir, topdown=False):
            #         for file in files:
            #             os.remove(os.path.join(root, file))
            # outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
            
            # inbox = outlook.GetDefaultFolder(6)

            outlook = win32com.client.Dispatch("Outlook.Application")

            # Get the MAPI namespace
            namespace = outlook.GetNamespace("MAPI")

            # Find the email account based on the specified account name or email address
            selected_account = None
            # for account in namespace.Accounts:
            #     if account.SmtpAddress.lower() == selected_account_name.lower():
            #         selected_account = account
            try:
                try:
                    print(str(emailAccount))
                    selected_account = namespace.Folders(str(emailAccount))
                    print("Access")
                except com_error as e:
                     print(f"Error accessing folder '{emailAccount}': {e}")
                # inbox = selected_account.DeliveryStore.GetDefaultFolder(6)  # 6 corresponds to the Inbox folder
                # email_messages = inbox.Items
                # # email_messages = inbox.Items
                for folder in selected_account.Folders:
                    print("Mailbox:", folder)
                        
                    email_messages = folder.Items
                    for email_message in email_messages:
                        # received_date = email_message.ReceivedTime
                    
                        try:
                            received_date = email_message.ReceivedTime
                            # Continue processing the email message
                        
                        # if received_date.date() == target_date.date():
                            
                            if received_date.date() >=target_date.date():
                                recipients_to = email_message.To
                                Subject=email_message.Subject
                                Sender=email_message.Sender
                                ReceivedTime=email_message.ReceivedTime
                                if recipients_to:
                                    for recipient in recipients_to.split(";"):
                                        # Access the full email address of the recipient
                                        recipient_email_address = recipient.strip()
                                # mesid=email_message.EntryID+"__"+
                                mesid = generate_unique_id()
                                objEmailMessage = EmailMessage(MessageID=mesid, To=recipients_to, Subject=Subject, Sender=Sender,ReceivedTime=ReceivedTime)
                                # objEmailMessage = EmailMessage(MessageID=mesid, To=recipients_to, Subject=Subject, Sender=Sender,ReceivedTime=ReceivedTime)
                                objEmailMessage.save()
                                data_found = True
                                attachments = email_message.Attachments

                                for attachment in attachments:
                                    original_filename = attachment.FileName
                                    new_output_path = os.path.join(output_dir,mesid)
                                    sanitized_filename = re.sub(r'[\\/:"*?<>|]+', '', original_filename)
                                    newOUtoutput_path = os.path.join(new_output_path, sanitized_filename)             
                                    os.makedirs(os.path.dirname(newOUtoutput_path), exist_ok=True)
                                    attachment.SaveAsFile(newOUtoutput_path)
                            
                        except AttributeError as e:
                                    print(f"Error accessing ReceivedTime: {e}")
                                    # Handle the error gracefully, e.g., by skipping this email message
                                    continue
            finally:
                print("error")                    
    finally:
        # Uninitialize COM using CoUninitialize
        pythoncom.CoUninitialize()
    
    return redirect('resume_list')

def process_file(file_path):
    text = ""
    images = []

    if file_path.lower().endswith('.pdf'):
        pdf_document = fitz.open(file_path)
        for page in pdf_document:
            text += page.get_text()
            images.extend(page.get_images(full=True))
        pdf_document.close()
    elif file_path.lower().endswith('.docx'):
        text = docx2txt.process(file_path)
    elif file_path.lower().endswith('.doc'):
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(file_path)
        text = doc.Content.Text
        doc.Close()
        word.Quit()
    else:
        text = pytesseract.image_to_string(Image.open(file_path))

    return text, images

def extract_emails_and_phone_numbers(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b'
    phone_pattern = r'(?:(?:\+?(\d{1,3}))?[-.\s]?)?(\d{10})'  

    emails = re.findall(email_pattern, text)
    phone_numbers = []


    for match in re.finditer(phone_pattern, text):
        country_code, phone = match.groups()
        if phone:
            phone_numbers.append(f'{country_code}-{phone}')

    return emails, phone_numbers



def extract_designation(text):
    designations = Designation.objects.all()
    matching_designations = []

    for designation in designations:
        if designation.keyword.lower() in text.lower():
            matching_designations.append(designation)

    return matching_designations

SUPPORTED_FORMATS = ('.pdf', '.docx', '.doc')

def upload_resume():
    
    try:
        attachments = download_email_data()
    except:
         print("Error- download_email_data")
    output_dir = r"C:\Emails"
    if os.path.exists(output_dir) and os.path.isdir(output_dir):
        files = os.listdir(output_dir)
        for folder in files:
            folderPath=os.path.join(output_dir, folder)
            foldersfiles = os.listdir(folderPath)
            for file in foldersfiles:
                file_path = os.path.join(folderPath, file)
                #file_path = os.path.join(folderPath, file)
                if os.path.isfile(file_path) and any(file_path.lower().endswith(ext) for ext in SUPPORTED_FORMATS):
                        try:
                            text, images = process_file(file_path)
                            emails, phone_numbers = extract_emails_and_phone_numbers(text)
                                
                            original_filename, _ = os.path.splitext(file)
                            name = original_filename.replace("_", " ")
                            file_name = file
                            # Create a new Resume entry
                            resume = Resume(MessageID=folder,name=name, file_name=file_name, email=emails[0] if emails else '', phone_number=phone_numbers[0] if phone_numbers else '')
                            resume.save()
                            resume.designation.add(*extract_designation(text))
                            with open(file_path, 'rb') as file:    
                                id = resume.id
                                new_file = upload_file_to_blob(file,id)
                         
                        except:
                                print("Error")

       

    # return redirect('resume_list')



def download_resume(request, id):
    file = Resume.objects.get(pk=id)
    file_id = file.file_id
    file_name = file.file_name
    
    file_type, _ = mimetypes.guess_type(file_id)
    
    
    blob_name = file_id
    blob_content = download_blob(blob_name)
    
    if blob_content:
        response = HttpResponse(blob_content.readall(), content_type=file_type)
        response['Content-Disposition'] = f'attachment; filename={file_name}'
      
        return response
    return Http404

def resume_list(request):
    # if 'OrganizationID' not in request.session:
    #     return redirect(MasterAttribute.Host)
    # else:
    #     print("Show Page Session")


    # OrganizationID =request.session["OrganizationID"]
    # UserID =str(request.session["UserID"])
    resume_lists = Resume.objects.filter(IsDelete=False)
    

    context= {'resume_lists':resume_lists}
    return render(request,"emailtemp/resumelist.html",context)




