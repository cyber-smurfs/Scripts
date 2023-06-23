#!/usr/bin/python3
# Nick Alderete & Jeremy Patton
# Scan network for SSH and RDP connection 



import csv
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import socket

# List of known IP addresses
known_ip_addresses = ['10.0.0.126', '10.0.0.197', '10.0.0.123', '10.0.0.82', '10.0.0.74', '10.0.0.175', '10.0.0.100', '10.0.0.101', '10.0.0.102', '10.0.0.103', '10.0.0.6', '10.0.0.176']

# List of IP addresses to scan
ip_addresses = ['192.168.0.1', '192.168.0.2', '192.168.0.3']  # Add your IP addresses here

# Ports to check
rdp_port = 3389  # RDP port
ssh_port = 22  # SSH port

# CSV file name
csv_file = 'connections.csv'

# Email details
sender_email = 'hunter2user@gmail.com'
sender_password = 'htshnhgxtzxfcvan'
receiver_email = 'hunter2user@gmail.com'
subject = 'Detected Connections'

# Function to check if a port is open
def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

# Function to save connection details to CSV file
def save_to_csv(timestamp, known_ip, connection_type, port, unknown_ip):
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, known_ip, connection_type, port, unknown_ip])

# Function to send email with attachment
def send_email(filename):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the file
    with open(filename, 'r') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {filename}')

    message.attach(part)

    # Connect to the SMTP server and send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

# Scan IP addresses
for ip in ip_addresses:
    if check_port(ip, rdp_port):
        save_to_csv(datetime.datetime.now(), known_ip='Unknown', connection_type='RDP', port=rdp_port, unknown_ip=ip)

    if check_port(ip, ssh_port):
        save_to_csv(datetime.datetime.now(), known_ip='Unknown', connection_type='SSH', port=ssh_port, unknown_ip=ip)

# Check known IP addresses
for ip in known_ip_addresses:
    if check_port(ip, rdp_port):
        save_to_csv(datetime.datetime.now(), known_ip=ip, connection_type='RDP', port=rdp_port, unknown_ip='Unknown')

    if check_port(ip, ssh_port):
        save_to_csv(datetime.datetime.now(), known_ip=ip, connection_type='SSH', port=ssh_port, unknown_ip='Unknown')

# Send the CSV file via email
send_email(csv_file)
