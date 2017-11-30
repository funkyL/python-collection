
# script not working. api param 'start' is deactived from api. thus its only
# possible to get latest 2000 trades.

# simple script to collect trade price on bitcoin and other cryptocurrensies
# from bitcoincharts.com's api.
# entries split into files, 2000 per file.

import requests
import time


file_dir = './'

start_time = str(int(time.time()) - 60*60*24*380) #380 days into the past

print(start_time)
def url(start):
    base = 'http://api.bitcoincharts.com/v1/'
    endpoint = 'trades.csv'
    params = '?symbol=krakenUSD&start=' + start # start param no longer active.
    return base + endpoint + params

#repeat calling api with new start times untill 30 mins from present time.
while time.time() - 60*30 > int(start_time):
    # get response from api
    resp = requests.get(url(start_time))
    if resp.status_code == 200:
        # write response text to file
        dest = file_dir + start_time + '.csv'
        with open(dest, 'w') as fi:
            write_data = fi.write(resp.text)
        fi.closed
        #go to last line
        for line in resp.text.split('\n'):
            pass
        # select timestamp from last line ( first object in line)
        start_time = str(line.split(',')[0])
        #print timestamp in console
        print('start at: ' + start_time)
    else:
        print("Status: " + str(resp.status_code))

    time.sleep(2)
