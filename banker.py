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
    for e in CategoryMatchingTableSpozywcze:   
        if e in operation['description']: return "Spożywcze"
    for e in CategoryMatchingTableKawiarnieLody:   
        if e in operation['description']: return "KawiarnieLody"
    for e in CategoryMatchingTableZdrowie:   
        if e in operation['description']: return "Zdrowie"   
    for e in CategoryMatchingTableDrogerie:   
        if e in operation['description']: return "Drogerie"   
    for e in CategoryMatchingTableDzieci:   
        if e in operation['description']: return "Dzieci"   

    return 0
CategoryList = [
    {"id": 0, "name": "Unknown"},
    {"id": 1, "name": "Spożywcze"},
    {"id": 2, "name": "Podróże"},
    {"id": 3, "name": "Ubrania"},
    {"id": 4, "name": "Dom"},
    {"id": 5, "name": "KawiarnieLody"},
    {"id": 6, "name": "Zdrowie"},
    {"id": 7, "name": "Drogerie"},
    {"id": 8, "name": "Dzieci"},    
    {"id": 31, "name": "Dzieci-Ubrania"},
    {"id": 32, "name": "Dzieci-Zabawki"},
    {"id": 33, "name": "Dzieci-ZajęciaDodatkowe"}
]

CategoryMatchingTableSpozywcze = [
    "GROMULSKI", "BIEDRONKA", "SOKOLOW-NET", "ZABKA", "TRUSKAWKI", "PUTKA", "OSKROBA", "PIEKARNIA", "LUBASZKA", "Carrefour"
]

CategoryMatchingTableKawiarnieLody = [
    "COSTA", "Smietankowe Cafe", "KUFLOTEKA"
]

CategoryMatchingTableZdrowie = [
    "APTEKA"
]

CategoryMatchingTableDzieci = [
    "EMPIK", "SMYK"
]

CategoryMatchingTableDrogerie = [
    "HEBE", "ROSSMANN"
]

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
    entry = {
        'date': operation.find('order-date').text,
        'type': operation.find('type').text,
        'amount': operation.find('amount').text,
        'category': 0,
        'saldo': operation.find('ending-balance').text,
        'description': operation.find('description').text
    }
    entry['category'] = FindCategory(entry)
    table.append(entry)



for row in table:
    if row['category'] == 0 : print(row)
    print()
