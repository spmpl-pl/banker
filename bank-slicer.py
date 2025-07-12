#!/usr/bin/env python
#####################################################################################################
#####################################################################################################
##  Banker -- app to extract specific transaction                                                 ##
##                                                                                                 ##
##  Author: Bartosz Chmielewski                                                                    ##
#####################################################################################################
#####################################################################################################
import argparse
import xml.etree.ElementTree as ET




# Set up argument parser
parser = argparse.ArgumentParser(description='Import the account history in XML format and categorize the entries')
parser.add_argument('xml_file', type=str, help='Path to the XML file')
parser.add_argument('period', type=str, help='Period to extract in YYMM format')
parser.add_argument('-v', action='store_true', default=False, help="Verbose mode.",)
args = parser.parse_args()

verbose = args.v

# Parse the XML file
tree = ET.parse(args.xml_file)
root = tree.getroot()
new_root = ET.Element('operations')

year = args.period[0:2]
month = args.period[2:4]


for operation in root.findall('.//operation'):
    date = operation.find('order-date').text
    if date[2:4] == year and date[5:7] == month:
        new_root.append(operation)

filename = year + month + ".xml"
new_tree = ET.ElementTree(new_root)
new_tree.write(filename, encoding='utf-8', xml_declaration=True)
