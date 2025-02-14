import json
import os.path
import requests
import time
import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

headers = {
    'User-Agent': 'GE price trend tracking wip discord @kat6541'
}

#directories
dataSheetPath = os.path.expanduser("~/Documents/GElog/dataSpreadsheet.xlsx")
filename = os.path.expanduser("~/Documents/GElog/grand_exchange.json")
itemDataFile = os.path.expanduser("~/Documents/GElog/itemData.json")
filteredItemDataFile = os.path.expanduser("~/Documents/GElog/filteredItemData.json")
priceDataFilePath = os.path.expanduser("~/Documents/GElog/priceData/")
derivedPriceDataFilePath = os.path.expanduser("~/Documents/GElog/priceData/derivedData/")


#URL's
latestURL = "https://prices.runescape.wiki/api/v1/osrs/latest"
itemListURL = "https://chisel.weirdgloop.org/gazproj/gazbot/os_dump.json"

minBuyLimitValue = 2000000 #used as a minimum value for itemPrice*buyLimit
minHourlyThroughput = 100000000 #used as a minimum value for itemPrice*volume
minHourlyVolume = 10000
maxPrice = 120000000 #used as a maximum value for individual item price
oneDayTime = 60*60*24
#    itemList = json.loads(requests.get(itemListURL).text)
#    with open(itemDataFile, "w") as f:
#        json.dump(itemList, f)
#        print(f"New data saved to {itemDataFile}")
def getPriceDataHistory(itemID):
        url = "https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=5m&id=" + itemID
        print('requesting data history')
        response = requests.get(url, headers=headers)
        # Save the data to the file
        filePath = priceDataFilePath + itemID + ".json"
        with open(filePath, "w") as f:
            json.dump(json.loads(response.text)['data'], f)
            print("New price history saved for ", itemID)
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
            if hourlyThroughput > minHourlyThroughput and buyLimitValue > minBuyLimitValue and lastPrice < maxPrice and itemList[item].get("volume") > minHourlyVolume:
                filteredItemList[item] = itemList[item]
                itemWatchCount = itemWatchCount + 1
                print("id: ", itemList[item].get("id"), "name: ", itemList[item].get("name"), " price: ",
                      itemList[item].get("last"), " limit: ", itemList[item].get("limit"), "volume: ",
                      itemList[item].get("volume"))
    print(itemWatchCount)
    with open(filteredItemDataFile, "w") as f:
        json.dump(filteredItemList, f)
        print(f"New data saved to {filteredItemDataFile}")
def getOneDayAvg(id):
    aodHighPrice = 0
    aodLowPrice = 0
    aodLowVolume = 0
    aodHighVolume = 0
    highPriceEntries = 0
    lowPriceEntries = 0
    highVolumeEntries = 0
    lowVolumeEntries = 0
    with open(priceDataFilePath + id + '.json', "r") as f:
        priceData = json.load(f)
    latestTime = priceData[len(priceData) - 1].get('timestamp')
    for entry in reversed(priceData):
        if (latestTime - entry.get('timestamp')) > oneDayTime:
            if highPriceEntries == 0:
                aodHighPrice = 0
            else:
                aodHighPrice = aodHighPrice / highPriceEntries
            if lowPriceEntries == 0:
                aodLowPrice = 0
            else:
                aodLowPrice = aodLowPrice / lowPriceEntries
            if highVolumeEntries == 0:
                aodHighVolume = 0
            else:
                aodHighVolume = aodHighVolume / highVolumeEntries
            if lowVolumeEntries == 0:
                aodHighPrice = 0
            else:
                aodLowVolume = aodLowVolume / lowVolumeEntries

            return {"avgHighPrice": aodHighPrice, "avgLowPrice": aodLowPrice, "avgHighVolume": aodHighVolume,
                    "avgLowVolume": aodLowVolume}
        else:
            if not (entry.get('avgHighPrice') == None):
                aodHighPrice = aodHighPrice + entry.get('avgHighPrice')
                highPriceEntries = highPriceEntries + 1
            if not (entry.get('avgLowPrice') == None):
                aodLowPrice = aodLowPrice + entry.get('avgLowPrice')
                lowPriceEntries = lowPriceEntries + 1
            if not (entry.get('avgHighVolume') == None):
                aodHighVolume = aodHighVolume + entry.get('avgHighVolume')
                highVolumeEntries = highVolumeEntries + 1
            if not (entry.get('avgLowVolume') == None):
                aodLowVolume = aodLowVolume + entry.get('avgLowVolume')
                lowVolumeEntries = lowVolumeEntries + 1
    if highPriceEntries == 0:
        aodHighPrice = 0
    else:
        aodHighPrice = aodHighPrice / highPriceEntries
    if lowPriceEntries == 0:
        aodLowPrice = 0
    else:
        aodLowPrice = aodLowPrice / lowPriceEntries
    if highVolumeEntries == 0:
        aodHighVolume = 0
    else:
        aodHighVolume = aodHighVolume / highVolumeEntries
    if lowVolumeEntries == 0:
        aodHighPrice = 0
    else:
        aodLowVolume = aodLowVolume / lowVolumeEntries

    return {"avgHighPrice": aodHighPrice, "avgLowPrice": aodLowPrice, "avgHighVolume": aodHighVolume,
            "avgLowVolume": aodLowVolume}

def getDerivative(id):
    with open(priceDataFilePath + id + '.json', "r") as f:
        priceData = json.load(f)

    if not os.path.exists(derivedPriceDataFilePath + id + "_1d.json"):
        entryCount = 0
        timeSeries = []
        priceSeries = []
        for entry in priceData:
            if not entry.get('avgHighPrice') == None:
                timeSeries.append(entry.get('timestamp'))
                priceSeries.append(entry.get('avgHighPrice'))
                entryCount = entryCount + 1

        data = [dict() for x in range(entryCount-1)]
        for i in range(0, entryCount - 1):
            data[i]['timestamp'] = timeSeries[i + 1]
            try:
                data[i]['avgHighPrice'] = (priceSeries[i+1] - priceSeries[i])/(timeSeries[i+1] - timeSeries[i])
            except:
                data[i]['avgHighPrice'] = None
                #print('incomplete data for point: ', i)
        with open(derivedPriceDataFilePath + id + '_1d.json', "w") as f:
            json.dump(data, f)
            #print("New data saved to ", id)
    else:
        with open(derivedPriceDataFilePath + id + '_1d.json', "r") as f:
            data = json.load(f)
        if (not priceData[len(priceData)-1].get('avgHighPrice') == None) and (not data[len(data)-1].get('timestamp') == priceData[len(priceData)-1].get('timestamp')):
            x = len(priceData) - 2
            foundPriorEntry = False
            while (x >= 0 and (not foundPriorEntry)):
                if (priceData[x].get('avgHighPrice') == None or (priceData[len(data)-1].get('timestamp') - priceData[x].get('timestamp') == 0)):
                    x = x - 1
                else:
                    foundPriorEntry = True
            if foundPriorEntry:
                data.append(dict())
                data[len(data) - 1]['timestamp'] = priceData[len(priceData) - 1].get('timestamp')
                data[len(data) - 1]['avgHighPrice'] = (priceData[len(priceData) - 1].get('avgHighPrice') -
                                                            priceData[x].get('avgHighPrice')) / (
                                                                       priceData[len(priceData) - 1].get('timestamp') -
                                                                       priceData[x].get('timestamp'))
                with open(derivedPriceDataFilePath + id + '_1d.json', "w") as f:
                    json.dump(data, f)
                    #print("New data saved to ", id)
            else:
                print('no old price point for: ', id)
        else:
            print('no new price point for: ', id)
def getSecondDerivative(id):
    with open(derivedPriceDataFilePath + id + '_1d.json', "r") as f:
        priceData = json.load(f)
    if not os.path.exists(derivedPriceDataFilePath + id + "_2d.json"):
        data = [dict() for x in range(len(priceData) - 1)]
        for i in range(0, len(priceData) - 1):
            data[i]['timestamp'] = priceData[i + 1].get('timestamp')
            try:
                data[i]['avgHighPrice'] = (priceData[i+1].get('avgHighPrice') - priceData[i].get('avgHighPrice'))/(priceData[i+1].get('timestamp') - priceData[i].get('timestamp'))
            except:
                data[i]['avgHighPrice'] = None
                #print('incomplete data for point: ', i)
        with open(derivedPriceDataFilePath + id + '_2d.json', "w") as f:
            json.dump(data, f)
            #print("New data saved to ", id)
    else:
        with open(derivedPriceDataFilePath + id + '_2d.json', "r") as f:
            data = json.load(f)
        if len(priceData) > len(data) + 1:
            data.append(dict())
            try:
                data[len(priceData) - 2]['timestamp'] = priceData[len(priceData) - 1].get('timestamp')
                data[len(priceData) - 2]['avgHighPrice'] = (priceData[len(priceData) - 1].get('avgHighPrice') -
                                                            priceData[len(priceData) - 2].get('avgHighPrice')) / (
                                                                   priceData[len(priceData) - 1].get('timestamp') -
                                                                   priceData[len(priceData) - 2].get('timestamp'))
            except:
                data[len(priceData) - 2]['timestamp'] = priceData[len(priceData) - 1].get('timestamp')
                data[len(priceData) - 2]['avgHighPrice'] = None
                #print('incomplete data for point: ', len(priceData) - 2)
            with open(derivedPriceDataFilePath + id + '_2d.json', "w") as f:
                json.dump(data, f)
                #print("New data saved to ", id)
        else:
            print('no new price point for: ', id)
# BEGIN MAIN
updateItemList()
#need actual entries not just ID's now
with open(filteredItemDataFile, "r") as f:
    keys = list(json.load(f).keys())

for entry in keys:
    if not os.path.exists(priceDataFilePath + entry + ".json"):
        getPriceDataHistory(entry)
        time.sleep(1)
        getDerivative(entry)
        getSecondDerivative(entry)

print('updated long term price data for 5m averages')

lastCheckTime = 0
while 1:
    if (int(time.time()) - int(lastCheckTime)) > 530:
        print('checking')
        url = "https://prices.runescape.wiki/api/v1/osrs/5m"
        print('requesting 5m data history')
        response = requests.get(url, headers = headers)
        data = json.loads(response.text)
        lastCheckTime = data.get('timestamp')
        with open(filteredItemDataFile, "r") as f:
            trackingList = json.load(f)
        for entry in keys:
            if (not data.get('data').get(entry) == None):
                try:
                    data.get('data').get(entry)['timestamp'] = data.get('timestamp')
                except:
                     print('error assigning time for ', entry)
                with open(priceDataFilePath + entry + '.json', "r") as f:
                    priceData = json.load(f)
                if not priceData[len(priceData)-1].get("timestamp") == data.get('data').get(entry)['timestamp']:
                    priceData.append(data.get('data').get(entry))
                    with open(priceDataFilePath + entry + '.json', "w") as f:
                        json.dump(priceData, f)
                        #print(f"New data saved to {entry}")
                    getDerivative(entry)
                    getSecondDerivative(entry)
                    newAvg = getOneDayAvg(entry)
                    trackingList[entry]["avgHighPrice"] = newAvg.get("avgHighPrice")
                    trackingList[entry]["avgLowPrice"] = newAvg.get("avgLowPrice")
                    trackingList[entry]["avgHighVolume"] = newAvg.get("avgHighVolume")
                    trackingList[entry]["avgLowVolume"] = newAvg.get("avgLowVolume")

                    # 5m average as a percentage of 24 hour average
                    try:
                        trackingList[entry]["highPriceChange"] = ((data.get('data').get(entry).get(
                            "avgHighPrice") / newAvg.get("avgHighPrice")) * 100) - 100
                    except:
                        trackingList[entry]["highPriceChange"] = "Invalid"
                    try:
                        trackingList[entry]["lowPriceChange"] = ((data.get('data').get(entry).get("avgLowPrice") / newAvg.get("avgLowPrice")) * 100) - 100
                    except:
                        trackingList[entry]["lowPriceChange"] = "Invalid"
                    try:
                        trackingList[entry]["highVolumeChange"] = ((data.get('data').get(entry).get("avgHighVolume") / newAvg.get("avgHighVolume")) * 100) - 100
                    except:
                        trackingList[entry]["highVolumeChange"] = "Invalid"
                    try:
                        trackingList[entry]["lowVolumeChange"] = ((data.get('data').get(entry).get("avgLowVolume") / newAvg.get("avgLowVolume")) * 100) - 100
                    except:
                        trackingList[entry]["lowVolumeChange"] = "invalid"

        with open(priceDataFilePath + keys[0] + '.json', "r") as f:
            priceData = json.load(f)
            lastCheckTime = priceData[len(priceData) - 1].get('timestamp')
        with open(filteredItemDataFile, "w") as f:
            json.dump(trackingList, f)
        print('finished updating 5m price history for: ', lastCheckTime)
        # print("updating table")
        # itemTable = pd.DataFrame([trackingList.values()])
        # # itemTable.to_excel(dataSheetPath ,sheet_name='itemTable', float_format="%.2f", index=False)
        # # print("updated table")
        time.sleep(300)













