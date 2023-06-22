#!/usr/bin/python3
# Nick Alderete & Jeremy Patton
# Automated network scan & Email notification



import csv
import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time


# IP addresses to monitor
ip_addresses = ['10.0.0.126', '10.0.0.197', '10.0.0.123', '10.0.0.82', '10.0.0.74', '10.0.0.175', '10.0.0.100',
                '10.0.0.101', '10.0.0.102', '10.0.0.103', '10.0.0.6', '10.0.0.176']
# Addresses: 
# .126 = Accounting 1 | .197 = Accounting 2 | .123 = Bobs Analytics server | 
# .82 = Metasploitable | .74 = Risk Analyst 1 | .175 = Web server | .100/101 = Hunter 1 | 
# 102/103 = Hunter 2 | .6 = Splunk/ SIEM | .176 = OpenVPN server


# Port numbers to check
port_numbers = [20, 21, 22, 23, 25, 53, 68, 80, 88, 110, 143, 161, 443]


# Path to save the CSV file
csv_file = 'traffic_data.csv'


# Email details
sender_email = 'hunter2user@gmail.com'
sender_password = 'fdhltktzgapxppskj'
receiver_email = 'hunter2user@gmail.com'
smtp_server = 'smtp.gmail.com'
smtp_port = 587


def check_external_traffic(ip_address):
    external_traffic = False
    for port in port_numbers:
        try:
            # Create a socket connection to the IP address on the specified port
            sock = socket.create_connection((ip_address, port), timeout=5)
            external_traffic = True
            sock.close()
            break
        except (socket.timeout, ConnectionRefusedError):
            pass
    return external_traffic


def save_traffic_data(ip_address, port_number):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, ip_address, port_number, 'External Traffic'])


def send_email_alert(csv_file):
    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Network Traffic Alert'

    # Attach the CSV file
    with open(csv_file, 'r') as file:
        attachment = MIMEText(file.read(), 'csv')
        attachment.add_header('Content-Disposition', 'attachment', filename=csv_file)
        message.attach(attachment)

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)


if __name__ == '__main__':
    while True:
        # Check for external traffic and save data to CSV
        for ip_address in ip_addresses:
            for port_number in port_numbers:
                if check_external_traffic(ip_address, port_number):
                    save_traffic_data(ip_address, port_number)


        # Send email alert with the CSV file attached
        send_email_alert(csv_file)


        # Wait for a specific interval before running the loop again (e.g., every 5 minutes)
        time.sleep(300)  # 300 seconds = 5 minutes
