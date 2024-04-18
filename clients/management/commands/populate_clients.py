import pandas as pd
from django.core.management.base import BaseCommand
from users.models import User
from clients.models import Client


class Command(BaseCommand):
    help = "Populate the databse with clients"

    def add_arguments(self, parser):
        parser.add_argument('user-email', help='email ID of the user')
        parser.add_argument('csv-file', help='path to the csv file')

    def handle(self, *args, **options):
        
        #get the user from the email
        user_email = options['user-email']
        user = User.objects.get(email=user_email)
        print(f"User {user.email} found")
        csv_file = options['csv-file']
        df = pd.read_csv(csv_file)
        #populate the clients
        for index, row in df.iterrows():
            description = row['description']
            if pd.isnull(description):  # Check if description is empty
                description = ''
            ethernet_ip = row['ethernet_ip']
            client_port = row['client_port']
            client_username = row['client_username']
            client_password = row['client_password']
            client_lab = row['client_lab']
            interface_name = row['interface']

            # Create Client object
            try:
                client = Client.objects.create(
                    user=user,
                    description=description,
                    ethernet_ip=ethernet_ip,
                    client_port=client_port,
                    client_username=client_username,
                    client_password=client_password,
                    client_lab=client_lab,
                    interface_name=interface_name
                )
                print(f"Client {client.description} created for user {user.email}")
            except Exception as e:
                print(f"Error creating client {description} for user {user.email}")
                print(e)
                continue

