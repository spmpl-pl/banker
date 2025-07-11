#!/usr/bin/env python
#####################################################################################################
#####################################################################################################
##  Banker -- app to categorize spendings in Banks                                                 ##
##                                                                                                 ##
##  Author: Bartosz Chmielewski                                                                    ##
#####################################################################################################
#####################################################################################################
import json
import argparse
import xml.etree.ElementTree as ET


def FindCategory(operation):
    return {'category': 'unknown'}


# Set up argument parser
parser = argparse.ArgumentParser(description='Import the account history in XML format and categorize the entries')
parser.add_argument('xml_file', type=str, help='Path to the XML file')
args = parser.parse_args()

# Parse the XML file
tree = ET.parse(args.xml_file)
root = tree.getroot()

# Process the data
table = []
for operation in root.findall('.//operation'):
    categorization = FindCategory(operation)
    entry = {
        'date': operation.find('order-date').text,
        'type': operation.find('type').text,
        'amount': operation.find('amount').text,
        'category': categorization['category'],
        'saldo': operation.find('ending-balance').text,
        'description': operation.find('description').text
    }
    table.append(entry)



for row in table:
    print(row)
    print()
