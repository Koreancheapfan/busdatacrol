from bs4 import BeautifulSoup
import requests
import datetime
import lxml
import time

key = 'Fl+MjXgGrTViuvJTy/RB8zodh2OEXStIUPEaFDSeUHAN5iMIG8zqFW4ROqV//eIee3K9KmL3TdAQQmm4cmnoOQ=='
rid = '235000092'


def bus():
    for i in range(1000):
        url = 'http://apis.data.go.kr/6410000/buslocationservice/getBusLocationList'
        params ={'serviceKey' : key, 'routeId' : rid }
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.content, 'xml')
        locations = soup.select('busLocationList')
        for busLocationList in locations:
            queryTime= soup.select('queryTime')
            routeId = busLocationList.select_one('routeId').text            #노선id
            stationId = busLocationList.select_one('stationId').text                 #정류장ID
            stationSeq = busLocationList.select_one('stationSeq').text       #정류소순번
            plateNo = busLocationList.select_one('plateNo').text       #차량번호
            print(routeId ,stationSeq, stationId, plateNo)
        time.sleep(60)

bus()
