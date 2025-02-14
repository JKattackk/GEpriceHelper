Very much an early work in progress.  Still deciding exactly what data I want to calculate and store as well as how I want to make it easily viewable.
WARNING: this will create a lot of files and currently does not trim old data in the price logs. 
Data will be stored in "~/Documents/GElog/"

This retrieves and stores price data for certain OSRS items using the OSRS wiki real time prices API (https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices).
Currently chooses these items based on a minimum buy limit value, minimum hourly throughput (itemPrice*volume), minimum hourly volume, and maximum item price.
Stores high price, low price, high volume, and low volume data for each item in 5 minute intervals.
When first ran it grabs up to 365 previous 5 minute averages for each item. Continuosly grabs new 5 minute averages and appends the data while ran.
Does the same for a first derivative and second derivative series for each item (currently only high price)
Also calcualtes the 24 hour average for each item and the percentage change between the latest 5 minute average and the 24 hour average for each item.

I'm currently using an excel spreadsheet to view the data as I haven't really worked with GUI's (yet).
