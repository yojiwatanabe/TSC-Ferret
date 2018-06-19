#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
email_results.py

This module works to email the results of the plugin output query. It is able to read the recipients list from a file
as well as read in from the command line. It uses a SMTP server to craft_message out each message attached with the results
table created from the last query.
"""

from process_dump import read_input
from pandas import datetime
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


SMTP_HOST = 'your.smtp.server'
SMTP_PORT = 0
RECIPIENTS = ['you@example.com']
FILENAME = 'results'
CSV_EXTENSION = '.csv'
HTML_EXTENSION = '.html'
SUBJECT_PREFIX = 'TSC Search Results @ '
PLUGIN_PREFIX = 'Plugin ID: '
HOST_PREFIX = 'Scanned Hosts: '
REPO_PREFIX = 'Scanned Repositories: '
IP_RANGE_PREFIX = 'Scanned IP Range (CIDR): '
SEARCH_PREFIX = 'Search Queries: '
DUPLICATE_MESSAGE = 'Allowing duplicates'
SENDER_ADDRESS = 'tsc_search_notifier@tufts.edu'
BODY_POSTFIX = '\n\n==================================================\nTHIS IS AN AUTOMATED MESSAGE, DO NOT RESPOND'


def craft_and_send_message(plugin_id, repos, hosts, ip_range, duplicates, csv, search_list):
    if csv:
        filename = ''.join((FILENAME, CSV_EXTENSION))
    else:
        filename = ''.join((FILENAME, HTML_EXTENSION))

    encoded_attachment = get_attachment(filename)
    subject_line = get_subject_line()
    email_body = get_information(plugin_id, hosts, repos, ip_range, search_list, duplicates)

    for recipient in RECIPIENTS:
        send_message(encoded_attachment, subject_line, email_body, recipient, filename)

    return True


def get_subject_line():
    date = datetime.now()
    formatted_date = str(date.month) + '/' + str(date.day) + '/' + str(date.year)
    formatted_time = str(date.hour) + ':' + str(date.minute) + ':' + str(date.second)

    formatted_datetime = ' - '.join([formatted_date, formatted_time])

    return ''.join([SUBJECT_PREFIX, formatted_datetime])


def get_information(plugin_id, hosts, repos, ip_range, search_list, duplicates):
    info = PLUGIN_PREFIX + plugin_id

    # Add information to body about the configuration of the TSC Search instance
    if hosts:
        host_strings = read_input(hosts)
        info = info + '\n' + HOST_PREFIX + ', '.join(host_strings)
    if repos:
        repo_strings = read_input(repos)
        info = info + '\n' + REPO_PREFIX + ', '.join(repo_strings)
    if ip_range:
        info = info + '\n' + IP_RANGE_PREFIX + ip_range
    if search_list:
        search_strings = read_input(search_list)
        info = info + '\n' + SEARCH_PREFIX + ', '.join(search_strings)
    if duplicates:
        info = info + '\n' + DUPLICATE_MESSAGE

    info = info + BODY_POSTFIX

    return info


def get_attachment(filename):
    file_stream = open(filename, 'rb')
    file_content = file_stream.read()

    return file_content


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
