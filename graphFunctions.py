import matplotlib.pyplot as plt
import json
import os.path

def showPlot(id):
    priceDataFilePath = os.path.expanduser("~/Documents/GElog/priceData/")
    derivedPriceDataFilePath = os.path.expanduser("~/Documents/GElog/priceData/derivedData/")
    fig, (fig1, fig2, fig3) = plt.subplots(3)

    with open(priceDataFilePath + id + '.json', "r") as f:
        priceData = json.load(f)
    fig1.plot([d['timestamp'] for d in priceData], [d['avgHighPrice'] for d in priceData])

    with open(derivedPriceDataFilePath + id + '_1d.json', "r") as f:
        priceData_1d = json.load(f)
    fig2.plot([d['timestamp'] for d in priceData_1d], [d['avgHighPrice'] for d in priceData_1d])
    # fig2.set_yticks([-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100])
    # fig2.set_ylim(-150, 150)

    with open(derivedPriceDataFilePath + id + '_2d.json', "r") as f:
        priceData_2d = json.load(f)
    fig3.plot([d['timestamp'] for d in priceData_2d], [d['avgHighPrice'] for d in priceData_2d])
    # fig3.set_yticks([-0.2, -0.1, 0, 0.1, 0.2])
    # fig3.set_ylim(-2, 2)
    plt.show()

showPlot('2')