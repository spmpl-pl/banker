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
    for e in CategoryMatchingTablePodroze:   
        if e in operation['description']: return "Podróże"
    for e in CategoryMatchingTableUbrania:   
        if e in operation['description']: return "Ubrania"
    for e in CategoryMatchingTableKawiarnieLody:   
        if e in operation['description']: return "KawiarnieLody"
    for e in CategoryMatchingTableJedzeniePozaDomem:   
        if e in operation['description']: return "JedzeniePozaDomem"  
    for e in CategoryMatchingTableZdrowie:   
        if e in operation['description']: return "Zdrowie"   
    for e in CategoryMatchingTableDrogerie:   
        if e in operation['description']: return "Drogerie"   
    for e in CategoryMatchingTableDzieci:   
        if e in operation['description']: return "Dzieci"   

    return "Unknown"

CategoryList = [
    "Unknown", 
    "Spożywcze",
    "Podróże",
    "Ubrania",
    "Dom",
    "KawiarnieLody",
    "JedzeniePozaDomem",
    "Zdrowie",
    "Drogerie",
    "Dzieci",    
]

CategoryMatchingTableSpozywcze = [
    "GROMULSKI", "BIEDRONKA", "SOKOLOW-NET", "ZABKA", "TRUSKAWKI", "PUTKA", "OSKROBA", "PIEKARNIA", "LUBASZKA", "Lubaszka", "Carrefour", "Stacja Ordona", "GRUSZKA BEZ FARTUSZK", "MECHANICZNA POMARANCZA", "Warzywozercy", 
    "DELIKATESY MIESNE"
]

CategoryMatchingTablePodroze = [
    "skycash.com", "Urbancard", "CAMPING"

]

CategoryMatchingTableUbrania = [
    "KappAhl", "ZARA"
]

CategoryMatchingTableKawiarnieLody = [
    "COSTA", "Smietankowe Cafe", "Al Passo", "LODOVA", "LODOMANIA"
]

CategoryMatchingTableJedzeniePozaDomem = [
    "BAR MLECZNY", "BEACH BAR", "SLIMAK", "KUFLOTEKA", "BISTRO WIEM", "CAMPING TUMIANY RESTAU", "FOLWARK"
]

CategoryMatchingTableZdrowie = [
    "APTEKA", "Apteka"
]

CategoryMatchingTableDzieci = [
    "EMPIK", "SMYK", "IBEX", "PEPCO"
]

CategoryMatchingTableDrogerie = [
    "HEBE", "ROSSMANN", "rossmann.pl"
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
NotAnalyzedCategories = []
for operation in root.findall('.//operation'):
    date = operation.find('order-date').text
    type = operation.find('type').text
    if type in ['Obciążenie', "Płatność web - kod mobilny", "Płatność kartą" ]:
        amount = float(operation.find('amount').text[1:])
        saldo = operation.find('ending-balance').text
        description = operation.find('description').text
        if "Adres : " in description:
            descriptionShort = description.split("Adres : ")[1].split(" Miasto :")[0].split(" 'Operacja :")[0].strip()
        else:   
            descriptionShort = ""


        entry = {
            'date': date,
            'type': type,
            'amount': amount,
            'category': 0,
            'saldo': saldo,
            'description': description,
            'descriptionShort': descriptionShort
        }
        entry['category'] = FindCategory(entry)
        table.append(entry)
    else:
        if type not in NotAnalyzedCategories:
            NotAnalyzedCategories.append(type)

print("Not Analyzed categories:")
for row in NotAnalyzedCategories:
    print (" -", row)




for category in CategoryList:
    print("\n\nZakupy w kategorii:", category)
    sum = 0
    for row in table:
        if row['category'] == category : 
            print("DATA:", row['date'], "KWOTA:", row['amount'], "TYP:", row['type'], "KRÓTKI OPIS:", row['descriptionShort'])
            sum = sum + row['amount']
    print("Sum:", sum, "PLN")
