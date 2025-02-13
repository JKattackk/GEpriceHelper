import json
import os.path
import requests
import time
import matplotlib.pyplot as plt
import numpy as np

headers = {
    'User-Agent': 'GE price trend tracking wip discord @kat6541'
}

#directories
filename = os.path.expanduser("~/Documents/GElog/grand_exchange.json")
itemDataFile = os.path.expanduser("~/Documents/GElog/itemData.json")
filteredItemDataFile = os.path.expanduser("~/Documents/GElog/filteredItemData.json")
priceDataFilePath = os.path.expanduser("~/Documents/GElog/priceData/")
derivedPriceDataFilePath = os.path.expanduser("~/Documents/GElog/priceData/derivedData/")


#URL's
latestURL = "https://prices.runescape.wiki/api/v1/osrs/latest"
itemListURL = "https://chisel.weirdgloop.org/gazproj/gazbot/os_dump.json"

tempTrackingID = '28924'
minBuyLimitValue = 5000000 #used as a minimum value for itemPrice*buyLimit
minHourlyThroughput = 100000000 #used as a minimum value for itemPrice*volume
minHourlyVolume = 1000
maxPrice = 120000000 #used as a maximum value for individual item price


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
            print("New price data saved for ", itemID)
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
def showPlot(id):
    fig1.plot([d['timestamp'] for d in priceData], [d['avgHighPrice'] for d in priceData])

    with open(derivedPriceDataFilePath + tempTrackingID + '_1d.json', "r") as f:
        priceData_1d = json.load(f)
    fig2.plot([d['timestamp'] for d in priceData_1d], [d['avgHighPrice'] for d in priceData_1d])
    fig2.set_yticks([-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100])
    fig2.set_ylim(-150, 150)
    with open(derivedPriceDataFilePath + tempTrackingID + '_2d.json', "r") as f:
        priceData_2d = json.load(f)
    fig3.plot([d['timestamp'] for d in priceData_2d], [d['avgHighPrice'] for d in priceData_2d])
    fig3.set_yticks([-0.2, -0.1, 0, 0.1, 0.2])
    fig3.set_ylim(-2, 2)
    plt.show()
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

        data = [dict() for x in range(entryCount)]
        for i in range(0, entryCount - 1):
            data[i]['timestamp'] = priceSeries[i + 1]
            try:
                data[i]['avgHighPrice'] = (priceSeries[i+1] - priceSeries[i])/(priceSeries[i+1] - priceSeries[i])
            except:
                data[i]['avgHighPrice'] = None
                print('incomplete data for point: ', i)
        with open(derivedPriceDataFilePath + id + '_1d.json', "w") as f:
            json.dump(data, f)
            print("New data saved to ", id)
    else:
        with open(derivedPriceDataFilePath + id + '_1d.json', "r") as f:
            data = json.load(f)
        if  (not priceData[len(priceData)-1].get('avgHighPrice') == None) and (not data[len(data)-1].get('timestamp') == priceData[len(priceData)-1].get('timestamp')):
            x = len(priceData) - 2
            foundPriorEntry = False
            while (x >= 0 and (not foundPriorEntry)):
                if (priceData[x].get('avgHighPrice') == None):
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
                    print("New data saved to ", id)
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
                print('incomplete data for point: ', i)
        with open(derivedPriceDataFilePath + id + '_2d.json', "w") as f:
            json.dump(data, f)
            print("New data saved to ", id)
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
                print('incomplete data for point: ', len(priceData) - 2)
            with open(derivedPriceDataFilePath + id + '_2d.json', "w") as f:
                json.dump(data, f)
                print("New data saved to ", id)
        else:
            print('no new price point for: ', id)
# BEGIN MAIN
updateItemList()
with open(filteredItemDataFile, "r") as f:
    trackingList = list(json.load(f).keys())

for entry in trackingList:
    if not os.path.exists(priceDataFilePath + entry + ".json"):
        getPriceDataHistory(entry)
        time.sleep(1)
        getDerivative(entry)
        getSecondDerivative(entry)

print('updated long term price data for 5m averages')
fig, (fig1, fig2, fig3) = plt.subplots(3)
with open(priceDataFilePath + trackingList[0] + '.json', "r") as f:
    priceData = json.load(f)
    lastCheckTime = priceData[len(priceData)-1].get('timestamp')
while 1:
    if (int(time.time()) - int(lastCheckTime)) > 530:
        print('checking')
        url = "https://prices.runescape.wiki/api/v1/osrs/5m"
        print('requesting 5m data history')
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        lastCheckTime = data.get('timestamp')

        for entry in trackingList:
            try:
                data.get('data').get(entry)['timestamp'] = data.get('timestamp')
            except:
                print('error assigning time for ', entry)

            with open(priceDataFilePath + entry + '.json', "r") as f:
                priceData = json.load(f)
            priceData.append(data.get('data').get(entry))
            with open(priceDataFilePath + entry + '.json', "w") as f:
                json.dump(priceData, f)
                print(f"New data saved to {entry}")
            getDerivative(entry)
            getSecondDerivative(entry)

        with open(priceDataFilePath + trackingList[0] + '.json', "r") as f:
            priceData = json.load(f)
            lastCheckTime = priceData[len(priceData) - 1].get('timestamp')


        time.sleep(300)













