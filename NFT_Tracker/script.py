from typing import Collection
import requests
import json
import csv
from os.path import exists
from datetime import date
def getFilePath():
    f = open('settings.json')
    data = json.load(f)
    print('CSV File location:',data['path_to_csv_files'],'\n\n')
    return data['path_to_csv_files']
filePath = getFilePath()
def collectStats(collectionToFind,cryptoPrice):
    url = "https://api.opensea.io/api/v1/collection/"
    url += collectionToFind 
    url += '/stats'
    
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    list = json.loads(response.text)
    
    if(list['stats']['floor_price']):
        print('\nData recieved for:', collectionToFind)
    else:
        raise Exception("Invalid Collection",collectionToFind, 'Ensure that the name in collecitons.txt is the name that appears in the url')
        
    values = []
    stats = list['stats']
    values.append(date.today().strftime("%m/%d/%Y"))
    values.append(stats['floor_price'])
    values.append(float(values[1]) * float(cryptoPrice))
    values.append(stats['one_day_volume'])
    values.append(stats['one_day_change'])
    values.append(stats['one_day_sales'])

    values.append(stats['seven_day_volume'])
    values.append(stats['seven_day_change'])
    values.append(stats['seven_day_sales'])

    values.append(stats['thirty_day_volume'])
    values.append(stats['thirty_day_change'])
    values.append(stats['thirty_day_sales'])

    values.append(stats['total_volume'])
    values.append(stats['total_sales'])
    values.append(stats['total_supply'])
    values.append(stats['num_owners'])
    values.append(stats['average_price'])
    values.append(float(stats['average_price']) * float(cryptoPrice))
    values.append(stats['market_cap'])
    
    
    return values
def getCryptoExchange(cryptoToFind):
    
    url = 'https://api.coinbase.com/v2/prices/'
    url += cryptoToFind
    url += '-USD/buy'
    crypto_response = requests.request("GET",url)

    CRYPTO_DATA = json.loads(crypto_response.text)
    
    CRYPTO_PRICE = CRYPTO_DATA['data']['amount']
    print('Crypto Price recieved')
    return CRYPTO_PRICE
def toCSV(name, row):
    fileExist = True
    
    fileName = filePath + name + '.csv'
    if(not exists(fileName)):
        print('File',fileName,'not Found, Creating now...')
        fileExist = False
    else:
        print('File',fileName,'found, appending to end...')
    with open(fileName, 'a',newline='') as f_object:
        header = ['Date','Floor Price ETH','Floor Price USD','One Day Volume','One Day Change', 'One Day Sales', 'Seven Day Volume','Seven Day Change', 'Seven Day Sales',
                  'Thirty Day Volume','Thirty Day Change', 'Thirty Day Sales','Total Volume', 'Total Sales','Total Supply','Num Owners', 'Average Price ETH', 'Average Price USD','Market Cap']
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = csv.writer(f_object)
        if(not fileExist):
            writer_object.writerow(header)
        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(row)
        print('Row Created in',fileName,'\n\n')
        #Close the file object
        f_object.close()

with open('collections.txt') as collections:
    lines = collections.readlines()
    cryptoPrice = getCryptoExchange('ETH')
    for i in range(len(lines) - 1):
        temp = lines[i][:-1]
        lines[i] = temp
    for line in lines:
        try:
            stats = (collectStats(line,cryptoPrice))
            try:
                toCSV(line, stats)
            except:
                print("\n\n================ERROR WITH CSV FILE================")
                print('Make sure that the .csv file is not open by another program')
        except:
            print('\n\n================INVALID COLLECTION NAME================')
            print('Invalid collection:',line)
            print('Ensure that the name is the one that appears in the url of collection\n\n')
        
        