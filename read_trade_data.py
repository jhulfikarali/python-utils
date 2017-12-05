#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 23:01:40 2017

@author: Jhulfikar
"""

import datetime

DEBUG_MODE=False

# WhatsApp Date Format
whatsapp_datetime_format = "%m/%d/%y, %I:%M %p"

# Find the last week friday which is our start date
last_friday = (day - datetime.timedelta(days=day.weekday() + 3)).replace(hour=0,minute=0,second=0,microsecond=0)

# Find end date by adding a week
this_thursday = last_friday + datetime.timedelta(days= 7)

print("Fetching TRADE information for range [" + str(last_friday) + " : " + str(this_thursday))

# Read the data from WhatsApp email
whatsapp_data = open("/Users/jkabee200/Downloads/WhatsApp Chat with JM Stocks and Options.txt")
crunched_data = {}

if DEBUG_MODE:
    print("[DEBUG] Date range: [" + str(last_friday) + " - " + str(this_thursday) + "]")

for line in whatsapp_data:
    if "[TRADE]" in line:
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
                name = line[date_index+2:line.index(": [TRADE]")]
                
                # Fetch the trade data
                msg = str(msg_date)  + "  <-->  " + line[line.index("[TRADE]")+7:]
                
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
            print("Failed processing line: " + line)

if DEBUG_MODE:
    print("[DEBUG] Names: " + str(crunched_data.keys()))
    print("[DEBUG] TradeData: " + str(crunched_data.values()))

for trade_person, value in crunched_data.items():
    print(trade_person)
    for trade_data in value:
        print(trade_data, end=" ")
    print()

