#currently just a duplicate file I used for testing

import json
import os.path


tempTrackingID = '2'
derivedPriceDataFilePath = os.path.expanduser("~/Documents/GElog/priceData/derivedData/")
priceDataFilePath = os.path.expanduser("~/Documents/GElog/priceData/")

def getDerivative(id):
    with open(priceDataFilePath + id + '.json', "r") as f:
        priceData = json.load(f)
    if not os.path.exists(derivedPriceDataFilePath + id + "_1d.json"):
        data = [dict() for x in range(len(priceData) - 1)]

        for i in range(0, len(priceData) - 1):
            print(i)
            data[i]['timestamp'] = priceData[i + 1].get('timestamp')
            try:
                data[i]['avgHighPrice'] = (priceData[i+1].get('avgHighPrice') - priceData[i].get('avgHighPrice'))/(priceData[i+1].get('timestamp') - priceData[i].get('timestamp'))
            except:
                data[i]['avgHighPrice'] = "null"
                print('incomplete data for point: ', i)
        with open(derivedPriceDataFilePath + tempTrackingID + '_1d.json', "w") as f:
            json.dump(data, f)
            print("New data saved to {tempTrackingID}")
    else:
        with open(derivedPriceDataFilePath + id + '_1d.json', "r") as f:
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
                data[len(priceData) - 2]['avgHighPrice'] = "null"
                print('incomplete data for point: ', len(priceData) - 2)
            with open(derivedPriceDataFilePath + tempTrackingID + '_1d.json', "w") as f:
                json.dump(data, f)
                print("New data saved to {tempTrackingID}")
        else:
            print('no new price point for: ', id)

def getSecondDerivative(id):
    with open(derivedPriceDataFilePath + id + '_1d.json', "r") as f:
        priceData = json.load(f)
    if not os.path.exists(derivedPriceDataFilePath + id + "_2d.json"):
        data = [dict() for x in range(len(priceData) - 1)]
        for i in range(0, len(priceData) - 1):
            print(i)
            data[i]['timestamp'] = priceData[i + 1].get('timestamp')
            try:
                data[i]['avgHighPrice'] = (priceData[i+1].get('avgHighPrice') - priceData[i].get('avgHighPrice'))/(priceData[i+1].get('timestamp') - priceData[i].get('timestamp'))
            except:
                data[i]['avgHighPrice'] = "null"
                print('incomplete data for point: ', i)
        with open(derivedPriceDataFilePath + tempTrackingID + '_2d.json', "w") as f:
            json.dump(data, f)
            print("New data saved to {tempTrackingID}")
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
                data[len(priceData) - 2]['avgHighPrice'] = "null"
                print('incomplete data for point: ', len(priceData) - 2)
            with open(derivedPriceDataFilePath + tempTrackingID + '_2d.json', "w") as f:
                json.dump(data, f)
                print("New data saved to {tempTrackingID}")
        else:
            print('no new price point for: ', id)

getDerivative('2')
getSecondDerivative('2')
# lastCheckTime = priceData[len(priceData) - 1].get('timestamp')
# for entry in reversed(priceData):
#     if (int(lastCheckTime) - int(entry.get('timestamp'))) > 3600:
#         break
#     else:
#         print('time: ', datetime.utcfromtimestamp(entry.get('timestamp')).strftime('%Y-%m-%d %H:%M:%S'), 'value: ', entry.get('avgHighPrice'))


