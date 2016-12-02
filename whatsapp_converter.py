#! /usr/bin/env python2
# Converts exported Whatsapp conversation txt files into CSV spreadsheets with serialized dates and times.

import csv
import datetime

raw_text = open('Conversation.txt').read().split('\n')

processed_text = []

for i in raw_text:
    try:
        if i[2] == '/' and i[5] == '/':  # If the line starts with a date, append it to processed_list
            processed_text.append(i)
        else:
            processed_text[-1] += " " + i.strip()  # If the message contains a line break, add the text after the break
    except Exception as e:                         # to the last line appended to processed_list
        print e


def excel_date(date1):
    temp = datetime.datetime(1903, 12, 30)
    delta = date1 - temp
    return delta.days


def excel_time(time1):
    hour = time1.hour
    minute = time1.minute
    seconds = (hour * 3600) + (minute * 60)
    return float(seconds) / float(86400)


final_list = []

for i in processed_text:
    addition = []

    # Get date and time and convert it to Excel serialization format
    date_string = i[:i.find(',')].strip()
    date_object = datetime.datetime.strptime(date_string, "%d/%m/%Y")
    time_string = i[i.find(', ') + 2:i.find(' - ')].strip().replace('.', '')
    time_object = datetime.datetime.strptime(time_string, "%I:%M %p")
    addition.append(excel_date(date_object))
    addition.append(excel_time(time_object))

    # Get name text
    name_startpoint = i.find(' - ')
    string = i[name_startpoint + 3:]
    name_endpoint = string.find(':')
    name_text = string[:name_endpoint].strip()
    addition.append(name_text)

    # Get message text
    msg_startpoint = i.find(name_text)
    string = i[msg_startpoint:]
    msg_startpoint1 = string.find(':')
    msg_text = string[msg_startpoint1 + 2:].strip()
    addition.append(msg_text)

    # Omit lines that aren't messages
    skip_phrases = ['messages you send to this group', 'changed', 'added', 'created', "you're now an"]
    add = True
    for phrase in skip_phrases:
        if phrase in name_text.lower():
            add = False

    if add:
        final_list.append(addition)

# Write the output CSV file
with open('whatsapp_output.csv', 'wb') as outfile:
    w = csv.writer(outfile)
    w.writerow(['Date', 'Time', 'Name', 'Message'])
    for row in final_list:
        w.writerow(row)
