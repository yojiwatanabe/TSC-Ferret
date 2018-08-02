#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
email_results.py

This module works to email the results of the plugin output query. It relies on a SMTP server to email the information
to the recipients. Sends information about the query as the email body and attaches the results table (in either a CSV
or HTML file, depending on what the user specified. Uses MIME formatting.
"""

import process_dump
from pandas import datetime
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

SMTP_HOST = ''
SMTP_PORT = 0
RECIPIENTS = ['']
SUBJECT_PREFIX = 'TSC Ferret Results @ '
PLUGIN_PREFIX = 'Plugin ID: '
HOST_PREFIX = 'Scanned Hosts: '
REPO_PREFIX = 'Scanned Repositories: '
IP_RANGE_PREFIX = 'Scanned IP Range (CIDR): '
SEARCH_PREFIX = 'Search Queries: '
DUPLICATE_MESSAGE = 'Allowing duplicates'
SENDER_ADDRESS = 'tsc_ferret_notifier@tufts.edu'
BODY_POSTFIX = '\n\n==================================================\nTHIS IS AN AUTOMATED MESSAGE, DO NOT RESPOND'


#       craft_and_send_message()
#
# Driver for the email_results.py module. Calls on helpers to craft each section of the email before sending the email
# individually to each recipient.
# Input  - plugin_id: string with plugin ID that was queried
#          hosts: string with hosts that were queried (if any)
#          repos: string with repost that were queried (if any)
#          ip_range: string of the IP range (CIDR format) that was queried (if any)
#          duplicates: boolean of whether or not duplicates are allowed
#          csv: boolean of whether or not output is in csv format
#          search_list:
# Output - none
def craft_and_send_message(plugin_id, hosts, repos, ip_range, search_list, duplicates, output_type):
    filename = process_dump.OUTPUT_FILENAME + output_type

    encoded_attachment = get_attachment_content(filename)
    subject_line = get_subject_line()
    email_body = craft_body(plugin_id, hosts, repos, ip_range, search_list, duplicates)

    for recipient in RECIPIENTS:
        send_message(encoded_attachment, subject_line, email_body, recipient, filename)

    return


#       get_subject_line()
#
# Function to craft the subject line of the email. Depends on the date and  time at which the email is being crafted
# Input  - none
# Output - string with the subject line to be added to email
def get_subject_line():
    date = datetime.now()
    formatted_date = str(date.month) + '/' + str(date.day) + '/' + str(date.year)
    formatted_time = str(date.hour) + ':' + str(date.minute) + ':' + str(date.second)

    formatted_datetime = ' - '.join([formatted_date, formatted_time])

    return ''.join([SUBJECT_PREFIX, formatted_datetime])


#       craft_body()
#
# Function that crafts the body of the email. Information in the body is descriptive of what kind of queries were run in
# the instance of TSC Ferret whose results are being emailed. Adds all information that may be useful.
# Input  - plugin_id: string with plugin ID that was queried
#          hosts: string with hosts that were queried (if any)
#          repos: string with repos that were queried (if any)
#          ip_range: string with CIDR-formatted IP range queried (if any)
#          search_list: string list with text that was queried (if any)
#          duplicates: boolean value of if duplicates were allowed
# Output - string containing query information to be used in email body
def craft_body(plugin_id, hosts, repos, ip_range, search_list, duplicates):
    info = PLUGIN_PREFIX + plugin_id

    # Add information to body about the configuration of the TSC Ferret instance
    if hosts:
        host_strings = process_dump.read_input(hosts)
        info = info + '\n' + HOST_PREFIX + ', '.join(host_strings)
    if repos:
        repo_strings = process_dump.read_input(repos)
        info = info + '\n' + REPO_PREFIX + ', '.join(repo_strings)
    if ip_range:
        info = info + '\n' + IP_RANGE_PREFIX + ip_range
    if search_list:
        search_strings = process_dump.read_input(search_list)
        info = info + '\n' + SEARCH_PREFIX + ', '.join(search_strings)
    if duplicates:
        info = info + '\n' + DUPLICATE_MESSAGE

    return info + BODY_POSTFIX


#       get_attachment_content()
#
# Gets the contents of a file to be attached to the email.
# Input  - string of the file to be attached to the email/whose contents will be retrieved
# Output - string with the contents of the given file
def get_attachment_content(filename):
    file_stream = open(filename, 'rb')
    file_content = file_stream.read()

    return file_content


#       send_message()
#
# Function to craft email in MIME format. Takes in all information about the email to be sent, crafts the email
# including sender, recipient, attachments, body, and then sends it to the recipients through the designated SMTP server
# in the global variables.
# Input  - attachment: string with the contents of the file to be attached to the email
#          subject_line: string with the subject line of the email
#          body: string with the body of the email
#          recipient: string with a single address to receive the email
#          filename: string with the name of the attachment file
# Output - None
def send_message(attachment, subject_line, body, recipient, filename):
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = recipient
    msg['Subject'] = subject_line

    msg.attach(MIMEText(body))
    attached_file = MIMEApplication(attachment)
    attached_file.add_header('content-disposition', 'attachment', filename=filename)
    msg.attach(attached_file)

    smtp_server = SMTP(SMTP_HOST, SMTP_PORT)
    smtp_server.sendmail(SENDER_ADDRESS, recipient, msg.as_string())
    smtp_server.close()

    return
