from bs4 import BeautifulSoup
import requests
import datetime
import lxml
import time
import pandas as pd

key = 'Fl+MjXgGrTViuvJTy/RB8zodh2OEXStIUPEaFDSeUHAN5iMIG8zqFW4ROqV//eIee3K9KmL3TdAQQmm4cmnoOQ=='
rid = '235000092'

for i in range(1, 1000):
    url = 'http://apis.data.go.kr/6410000/buslocationservice/getBusLocationList'
    params ={'serviceKey' : key, 'routeId' : rid }
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, 'xml')
    locations = soup.select('busLocationList')
    save = open("temp.csv", "w")
    for busLocationList in locations:
        queryTime= soup.select_one('queryTime').text
        routeId = busLocationList.select_one('routeId').text
        stationId = busLocationList.select_one('stationId').text
        stationSeq = busLocationList.select_one('stationSeq').text
        plateNo = busLocationList.select_one('plateNo').text
        print(queryTime)
        print(routeId)
        print(stationId)
        print(stationSeq)
        print(plateNo)
        save.write(queryTime + "," + routeId + "," + stationId + "," + stationSeq + "," + plateNo + "\n")
    time.sleep(60)