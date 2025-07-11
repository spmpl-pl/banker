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
import pandas as pd

# Set up argument parser
parser = argparse.ArgumentParser(description='Import the account history in XML format and categorize the entries')
parser.add_argument('xml_file', type=str, help='Path to the XML file')
args = parser.parse_args()

# Parse the XML file
tree = ET.parse(args.xml_file)
root = tree.getroot()

# Extract data
table = []
for operation in root.findall('operations'):
    entry = {
        'date': operation.find('order-date').text,
        'type': operation.find('type').text,
        'description': operation.find('description').text,
        'amount': operation.find('amount').text,
        'saldo': operation.find('ending-balance').text
    }
    table.append(entry)

# Convert to DataFrame
df = pd.DataFrame(table)

# Print table
print(df)
