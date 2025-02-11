import json
import os.path
import requests
from datetime import datetime, timedelta
import time

import matplotlib.pyplot as plt
import numpy as np

headers = {
    'User-Agent': 'GE price trend tracking wip discord @kat6541',
    'From': 'jkattackk@gmail.com'  # This is another valid field
}
filename = os.path.expanduser("~/Documents/GElog/grand_exchange.json")
itemDataFile = os.path.expanduser("~/Documents/GElog/itemData.json")
filteredItemDataFile = os.path.expanduser("~/Documents/GElog/filteredItemData.json")
priceDataFilePath = os.path.expanduser("~/Documents/GElog/priceData/")

tempTrackingID = '2'
latestURL = "https://prices.runescape.wiki/api/v1/osrs/latest"
itemListURL = "https://chisel.weirdgloop.org/gazproj/gazbot/os_dump.json"
minBuyLimitValue = 1000000 #used as a minimum value for itemPrice*buyLimit
minHourlyThroughput = 1000000 #used as a minimum value for itemPrice*volume
maxPrice = 120000000 #used as a maximum value for individual item price


#    itemList = json.loads(requests.get(itemListURL).text)
#    with open(itemDataFile, "w") as f:
#        json.dump(itemList, f)
#        print(f"New data saved to {itemDataFile}")
def getPriceDataHistory(itemID):
        url = "https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=5m&id=" + itemID
        response = requests.get(url, headers=headers)
        # Save the data to the file
        filePath = priceDataFilePath + itemID + ".json"
        with open(filePath, "w") as f:
            json.dump(json.loads(response.text)['data'], f)
            print(f"New data saved to {filePath}")

def updateItemList():
    # examine, highalch, icon, id, last, limit, lowalch, members, name, price, value, volume
    itemWatchCount = 0
    filteredItemList = {}
    with open(itemDataFile, "r") as f:
        itemList = json.load(f)
        #itemList = itemList['10344']
        print("test")
    for item in itemList.keys():
        if isinstance(itemList[item], int) or isinstance(itemList[item], float):
            print("not an item")
        else:
            try:
                buyLimitValue = itemList[item].get("limit") * itemList[item].get("last")
            except:
                buyLimitValue = 500000
            try:
                hourlyThroughput = itemList[item].get("volume") * itemList[item].get("last")
            except:
                hourlyThroughput = 1
            try:
                lastPrice = itemList[item].get("last")
            except:
                lastPrice = 0
            print(itemList[item].get("name"), itemList[item].get("id"))
            if hourlyThroughput > minHourlyThroughput and buyLimitValue > minBuyLimitValue and lastPrice < maxPrice:
                filteredItemList[item] = itemList[item]
                itemWatchCount = itemWatchCount + 1
                print("id: ", itemList[item].get("id"), "name: ", itemList[item].get("name"), " price: ",
                      itemList[item].get("last"), " limit: ", itemList[item].get("limit"), "volume: ",
                      itemList[item].get("volume"))
    print(itemWatchCount)
    with open(filteredItemDataFile, "w") as f:
        json.dump(filteredItemList, f)
        print(f"New data saved to {filteredItemDataFile}")

# BEGIN MAIN
if not os.path.exists(priceDataFilePath + tempTrackingID + ".json"):
    getPriceDataHistory(tempTrackingID)

with open(priceDataFilePath + tempTrackingID + '.json', "r") as f:
    priceData = json.load(f)
    lastCheckTime = time.time()
while 1:
    if (int(time.time()) - int(lastCheckTime)) > 550:
        url = "https://prices.runescape.wiki/api/v1/osrs/5m"
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        lastCheckTime = data.get('timestamp')
        data.get('data').get('2')['timestamp'] = data.get('timestamp')
        priceData.append(data.get('data').get('2'))

        with open(priceDataFilePath + tempTrackingID + '.json', "w") as f:
            json.dump(priceData, f)
            print(f"New data saved to {tempTrackingID}")
        time.sleep(300)













