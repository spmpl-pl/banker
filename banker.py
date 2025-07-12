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
    for c in CategoryList:
        #print(c[1])
        for e in c[1]:   
            if e.lower() in operation['description'].lower(): return c[0] 
    return "Inne"


CategoryList = [
    

    ["Spożywcze", 
        [ "GROMULSKI", "BIEDRONKA", "SOKOLOW-NET", "ZABKA", "TRUSKAWKI", "PUTKA", "OSKROBA", "PIEKARNIA", "LUBASZKA", "Lubaszka", "Carrefour", "Stacja Ordona", "GRUSZKA BEZ FARTUSZK", "MECHANICZNA POMARANCZA", "Warzywozercy", 
    "DELIKATESY MIESNE", "LIDL", "KAUFLAND", "Stokrotka", "Hala Wola", "Arcypiekarz", "Auchan", "Galeria wypiekow", "Wesola Pani", "Spozywczy", "kawa365",
    "Delikatesy", "PRZYSTANEK SMAKOW", "go4taste.pl", "WSS Spolem" ]],
    
    ["Podróże", 
        ["skycash.com", "Urbancard", "CAMPING", "intercity", "SZYNDZIELNI", "STACJA PALIW", "ORLEN", "PARKOMAT", "MPK KRAKOW", "Kolej Linowa"]],

    ["Ubrania",
        ["KappAhl", "ZARA", "zara.com", "ODZIEZ", "Rylko", "intimissimi", "TK Maxx", "Carry", "C & A", "Reserved", "CALZEDONIA", "sportano.pl", "MANGO WARSAW",
         "borsetka.pl", "marsala-butik.pl", "HM Miasto", "lanea.com.pl", "zalamo" ]],
    
    ["KawiarnieLody",
        ["COSTA", "Smietankowe Cafe", "Al Passo", "LODOVA", "LODOMANIA", "SLODKIE CIOCIE", "POLISH LODY", "ALL GOOD S.A.", "CAFE", "COFFEE", "Caffe",
         "Cukiernia", "Stolica Lodow", "Stacja Lody", "Slodka Buda", "Kawiarnia", "PROCHOWNIA ZOLIBORZ" ]],

    ["JedzeniePozaDomem",
        ["BAR MLECZNY", "BEACH BAR", "SLIMAK", "KUFLOTEKA", "BISTRO WIEM", "CAMPING TUMIANY RESTAU", "FOLWARK", "POD BRYKAJACYM KUCYKIE", "Bufet", "Mleczarnia",
         "McDonald", "Restauracja", "Bar Centralny", "Grill", "Ciacho", "Pierogarnia", "Bistro", "Pizzeria", "Nalesnikarnia", "Kebab", "KOLANKO NO 6",
           "Bar Zabkowsk"  ]],

    ["Zdrowie",
        ["APTEKA", "Apteka", "SUPER - PHARM", "Dental Gallery"]],

    ["Drogerie",
        ["HEBE", "ROSSMANN", "rossmann.pl"]],

    ["SportIHobby",
        ["OSIR", "Osrodek Moczydlo", "PLYWALNIA MIEJSKA", "SAMOCHODY FILMOWE", "kicket.com", "DFZ  SP ZOO", "Kross", "Decathlon", "Stolica Ruchu"]],

    ["DomIOgród",
        ["Action", "temu.com", "Castorama", "IKEA", "MediaExpert", "EURO-NET", "KWIACIARNIA GARDENIA"]],

    ["Dzieci",
        ["EMPIK", "SMYK", "IBEX", "PEPCO", "dePapel", "patataj-kanie", "Haircut", "Relay", "Ksiegarnie", "Ksiegarnia", "Mybasic", "airo.fun", "pstro.com.pl",
         "TuSzyte", "Szkola Narciarska", "bossobuty.pl", "Sklep Kupklocki.pl", "zalando", "aniakruk.pl", 
          ]],

    ["eCommerce",
        ["inpost.pl", "allegro.pl", "gopay.cz", "vinted", "Selmo", ]],

    ["WypłatyZBankomatów", ["XXXXXXXXXXXXXXXXXXX"]],

    ["Przelewy", ["XXXXXXXXXXXXXXXXXXX"]],
    
    ["Inne", ["XXXXXXXXXXXXXXXXXXX"]],

]




# Set up argument parser
parser = argparse.ArgumentParser(description='Import the account history in XML format and categorize the entries')
parser.add_argument('xml_file', type=str, help='Path to the XML file')
parser.add_argument('-v', action='store_true', default=False, help="Verbose mode.",)
args = parser.parse_args()

verbose = args.v

# Parse the XML file
tree = ET.parse(args.xml_file)
root = tree.getroot()

# Process the data
table = []
NotAnalyzedCategories = []
for operation in root.findall('.//operation'):
    date = operation.find('order-date').text
    type = operation.find('type').text
    if type in ['Obciążenie', "Płatność web - kod mobilny", "Płatność kartą", "Wypłata w bankomacie - kod mobilny", "Wypłata z bankomatu", "Przelew na telefon przychodz. zew.", "Przelew na telefon przychodz. wew.", "Przelew z rachunku", "Zagraniczna płatność zbliżeniowa BLIKIEM" ]:
        if operation.find('amount').text[0] == "-":
            amount = float(operation.find('amount').text[1:])
            saldo = operation.find('ending-balance').text
            description = operation.find('description').text
            if "Adres : " in description:
                descriptionShort = description.split("Adres : ")[1].split(" Kraj :")[0].split(" 'Operacja :")[0].strip()
            else:   
                descriptionShort = description


            entry = {
                'date': date,
                'type': type,
                'amount': amount,
                'category': 0,
                'saldo': saldo,
                'description': description,
                'descriptionShort': descriptionShort
            }
            
            if type[:7] == "Wypłata": entry['category'] = "WypłatyZBankomatów"
            elif type[:7] == "Przelew": 
                entry['category'] = "Przelewy"
                if "Nazwa odbiorcy :  " in description: entry['descriptionShort'] = description.split("Nazwa odbiorcy :  ")[1]
                else: descriptionShort = description

            else: entry['category'] = FindCategory(entry)
            table.append(entry)
    else:
        if type not in NotAnalyzedCategories:
            NotAnalyzedCategories.append(type)
        #print("  ===   ", type, float(operation.find('amount').text),  operation.find('description').text)

table.sort(key=lambda row: row['date'])


if verbose:
    print("Not Analyzed categories:")
    for row in NotAnalyzedCategories:
        print (" -", row)

CategorySums = {}
SumTotal = 0

for category in CategoryList:
    if verbose: print("\n\nZakupy w kategorii:", category[0])
    CategorySums[category[0]] = 0
    for row in table:
        if row['category'] == category[0] : 
            if verbose: print("   ",row['date']," | ", f"{row['amount']:8.2f}", " | ", f"{row['type']:<40}", " | ", f"{row['descriptionShort'][:48]:<50}", " |")
            CategorySums[category[0]] = CategorySums[category[0]] + row['amount']
    if verbose: print("Sum:", f"{CategorySums[category[0]]:7.2f}", "PLN")
    SumTotal = SumTotal + CategorySums[category[0]]


print("\nKategorie wydatków:")
for category, value in CategorySums.items():
    print("  ", f"{category:<20}" + ":",  f"{value:8.2f}", "PLN")

print("\nSuma wszystkich wydatków:", f"{SumTotal:8.2f}", "PLN")
