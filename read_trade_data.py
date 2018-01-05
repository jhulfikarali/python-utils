#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 23:01:40 2017

@author: Jhulfikar
"""

import datetime
import sys

file_name = "/Users/jkabee200/Downloads/WhatsApp Chat with JM Stocks and Options.txt"

if len(sys.argv) >= 2:
    file_name = sys.argv[1]
else:
    print("Defaulted")

print("Filename: %s" % (file_name))

# Keywords to look for getting TRADE Data
trade_keywords=["[TRADE]", "sell", "sold", "buy"]

print("Keywords to parse: %s" % trade_keywords)

DEBUG_MODE=False

# WhatsApp Date Format
whatsapp_datetime_format = "%m/%d/%y, %I:%M %p"

day=datetime.datetime.today()

# Find the last week friday which is our start date
last_friday = (datetime.datetime.today() - datetime.timedelta(days=datetime.datetime.today().weekday() + 3)).replace(hour=0,minute=0,second=0,microsecond=0)

# Find end date by adding a week
this_thursday = last_friday + datetime.timedelta(days= 7)

def extract_data(extract_param):
    try:
        # Get the message sent datetime index
        date_index = line.index("-")

        # Get the message sent datetime
        msg_date = datetime.datetime.strptime(line[0:date_index-1], whatsapp_datetime_format)

        if DEBUG_MODE:
            print("[DEBUG] msg_date: " + str(msg_date))

        if last_friday < msg_date < this_thursday: # Only trade info which is needed for this week

            if DEBUG_MODE:
                print("[DEBUG] " + line)
            # Fetch the name of the person who sent the Trade data
            name = line[date_index+2:line.index(": " + extract_param)]

            # Fetch the trade data
            startIndex = line.index(extract_param)
            if extract_param == '[TRADE]':
                line.index(extract_param)+len(extract_param)

            msg = str(msg_date)  + "  <-->  " + line[startIndex:]

            if DEBUG_MODE:
                print("[DEBUG] " + name+ " : " + msg)
            try:
                msgs = crunched_data[name]
                msgs.append(msg)
            except KeyError:
                msgs = []
                msgs.append(msg)
                crunched_data[name] = msgs

    except ValueError:
        if DEBUG_MODE:
            print("Failed processing line: " + line)

print("Fetching TRADE information for range [" + str(last_friday) + " : " + str(this_thursday) + "\n\n\n")

# Read the data from WhatsApp email
whatsapp_data = open(file_name)
crunched_data = {}

if DEBUG_MODE:
    print("[DEBUG] Date range: [" + str(last_friday) + " - " + str(this_thursday) + "]")

for line in whatsapp_data:
    for keyword in trade_keywords:
        if keyword in line:
            #print("Keyword: %s" % (keyword))
            extract_data(keyword)

if DEBUG_MODE:
    print("[DEBUG] Names: " + str(crunched_data.keys()))
    print("[DEBUG] TradeData: " + str(crunched_data.values()))

for trade_person, value in crunched_data.items():
    print(trade_person)
    for trade_data in value:
        print(trade_data, end=" ")
    print()

