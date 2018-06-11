#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
email_results.py

This module works to email the results of the plugin output query. It is able to read the recipients list from a file
as well as read in from the command line. It uses an SMTP server to send out each message attached with the results
table created from the last query.
"""

#       get_recipients()
#
#
def get_recipients():
    # try to find a file with email addresses
    # if file doesnt exist or is empty,
        # read in addresses manually

    # give user prompt about exactly what users are being sent the data
    # have user confirm, allow them to go back and edit


def message_setup():
    # function to create the message that will be sent

    # get sender
    # call on function to get recipients
    # create descriptive subject line
    # MAKE HEADER

    # attach results.html

    # try send / except errorMsg