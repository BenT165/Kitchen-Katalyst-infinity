from pathlib import Path
import smtplib
import ssl
from django.core.management import BaseCommand
from home.models import User, Grocery
from datetime import date, timedelta
from django.db.models import Prefetch
import inflect

# Create an inflect engine instance
p = inflect.engine()

#make everything grammatically correct
def pluralize(noun, quantity):
    # Pluralize the noun based on the quantity
    plural_noun = p.plural(noun, quantity)

    # Construct the output string
    output = f"{quantity} {plural_noun}"

    return output

#classify and return lists of items for each user
def process_groceries(user, today, reminder_threshold, receiver_email):
    expired_list = []
    twenty_four_hours_list = []
    custom_list = []

    expired_list.append("Expired")
    twenty_four_hours_list.append("Expiring within 1 day")
    custom_list.append(f"Expiring within {pluralize('day', user.date_reminder)}")

    # Loop through all groceries for the current user
    for grocery in user.groceries.all():


        # Check if grocery expiration date has already passed and grocery is not already expired
        if grocery.expiration_date == today and not grocery.is_expired:
            formatted_entry = f"\t{pluralize(grocery.name, grocery.quantity)}"
            expired_list.append(formatted_entry)
            grocery.is_expired = True  # TODO: Mark as expired
            grocery.day_before = True
            grocery.custom_reminder = True
            grocery.save()  # TODO: Save changes

        # Check if current time is within 24 hours before the expiration date
        elif grocery.expiration_date - today <= timedelta(days=1) and not grocery.day_before:
            formatted_entry = f"\t{pluralize(grocery.name, grocery.quantity)}"
            twenty_four_hours_list.append(formatted_entry)
            grocery.day_before = True
            grocery.custom_reminder = True
            grocery.save()  # TODO: Save changes

        # Check if current time is within the custom reminder threshold
        elif grocery.expiration_date - today <= reminder_threshold and not grocery.custom_reminder:
            formatted_entry = f"\t{pluralize(grocery.name, grocery.quantity)}"
            custom_list.append(formatted_entry)
            grocery.custom_reminder = True
            grocery.save()  # TODO: Save changes

   

        

    return (format_grocery_entries(expired_list), format_grocery_entries(twenty_four_hours_list), format_grocery_entries(custom_list))


#bundles components into formatted array
def format_grocery_entries(groceries):

    if len(groceries) == 1:
        groceries.append("\tNothing yet")
    groceries.append("\n")

    return '\n'.join(groceries)



#main class
class Command(BaseCommand):

    help = 'Sends email using information from User and Grocery models'

    #def add_arguments(self, parser):
     #   return super().add_arguments(parser)


    def handle(self, *args, **options):

        # Get the directory 3 levels above the current directory
        target_dir = Path(__file__).resolve().parent.parent.parent.parent

        # Path to stuff.txt in the parent directory
        stuff_txt_path = target_dir / 'stuff.txt'

        # Open stuff.txt and retrieve email credentials for sender
        with open(stuff_txt_path, 'r') as file:
            lines = file.readlines()
            email = lines[0].strip()
            password = lines[2].strip()
            


        # Get today's date
        today = date.today()
   
        # Fetch all users with related groceries and prefetch related objects
        users_with_groceries = User.objects.prefetch_related(
            Prefetch('groceries', queryset=Grocery.objects.filter(is_expired=False))
        )


        # Loop through all users
        for user in users_with_groceries:

            # Get email for current user
            receiver_email = user.email

            # Get window for custom reminders
            reminder_threshold = timedelta(days=user.date_reminder)


            #query DB and join components into a templated message            
            subject = f"Kitchen Update {today}"

            intro = f"Hello {user.first_name},\n\n\nHere's the rundown on your current kitchuation:\n\n"
            components = process_groceries(user, today, reminder_threshold, receiver_email)

            # Check if user should get an email or not
            dont_send = components[0] == "Expired\n\tNothing yet\n\n" and components[1] == "Expiring within 1 day\n\tNothing yet\n\n" and components[2] == f"Expiring within {pluralize('day', user.date_reminder)}\n\tNothing yet\n\n"


            # If should_send is False, print the receiver's email
            if dont_send:
                print("not sending to " + receiver_email)
                continue


            farewell = "You rock,\n\n\nKitchen Katalyst"  
            message = '\n'.join([intro, components[0], components[1], components[2], farewell])
            text= f"Subject: {subject}\n\n{message}"

            #print(text)


            #TODO uncomment and test
            #establish connection on port 587
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            server.login(email, password)
            server.sendmail(email, receiver_email, text)

            print("email sent to " + receiver_email)

            #TODO sleep for 1 minute

        