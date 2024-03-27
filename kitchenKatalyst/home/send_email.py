from pathlib import Path
import smtplib
import ssl
from models import Grocery, User
from datetime import datetime

#hello

# Get the parent directory
parent_dir = Path(__file__).resolve().parent.parent

# Path to stuff.txt in the parent directory
stuff_txt_path = parent_dir / 'stuff.txt'

# Open stuff.txt and retrieve email credentials for sender
with open(stuff_txt_path, 'r') as file:
    lines = file.readlines()
    email = lines[0].strip()
    password = lines[2].strip()



#TODO while True

    #TODO sleep for 1 minute

    #DB query for current user to see if they have any groceries they need to be reminded about (with 24 hours of expiring)

    #if yes,
        #declare subject (Expires Soon Reminder  - today's date)
        #make body list of groceries for each item in table that meets criteria (expires in less than or equal to 24 hours and grocery.default_reminder1==False)
        #set grocery.default_reminder1 to true for each grocery that meets criteria


     #DB query for current user to see if they have any groceries they need to be reminded about (expired)

    #if yes,
        #declare subject (something like Expired Reminder - today's date)
        #make body list of groceries for each item in table that meets criteria (expired and grocery.default_reminder2==True)
        #set grocery.default_reminder2 to true for each grocery that meets criteria

    #DB query for current user to see if they have any groceries they need to be reminded about (current datetime + user.custom_reminder (number of days)) >= grocery.expiration_date

    #if yes,
        #declare subject (something like Custom-Reminder - today's date)
        #make body list of groceries for each item in table that meets criteria (expired and grocery.default_reminder2==True)
        #set grocery.custom_reminder to true for each grocery that meets criteria

#TODO 
# 
# helper functions(grocery, ndays)


# TODO TODO TODO (Gerson, update the email value on line to test it out: should send an email to)
# Define recipient email (TODO make this vary based on user)
receiver_email = "bentate165@gmail.com"  # Enter receiver address

# Email content
subject = "Hello"
message = "Hi Ninayyy goose"
text= f"Subject: {subject}\n\n{message}"


#establish connection on port 587
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(email, password)
server.sendmail(email, receiver_email, text)

print("email sent to " + receiver_email)