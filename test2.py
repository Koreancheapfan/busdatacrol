from bs4 import BeautifulSoup
import requests
import datetime
import pandas as pd
import lxml
import time

key = 'Fl+MjXgGrTViuvJTy/RB8zodh2OEXStIUPEaFDSeUHAN5iMIG8zqFW4ROqV//eIee3K9KmL3TdAQQmm4cmnoOQ=='
rid = '235000092'

for bus in range(1, 10):
    url = 'http://apis.data.go.kr/6410000/buslocationservice/getBusLocationList'
    params ={'serviceKey' : key, 'routeId' : rid }
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, 'xml')
    locations = soup.select('busLocationList')
    for busLocationList in locations:
        queryTime= soup.select_one('queryTime').text
        routeId = busLocationList.select_one('routeId').text          #노선id
        stationId = busLocationList.select_one('stationId').text                #정류장ID
        stationSeq = busLocationList.select_one('stationSeq').text       #정류소순번
        plateNo = busLocationList.select_one('plateNo').text     #차량번호
        query_Time = [queryTime]
        route_Id = [routeId]
        station_Id = [stationId]
        station_Seq = [stationSeq]
        plate_No = [plateNo]
        df = pd.DataFrame(query_Time, columns=['query_Time'])
        df['route_Id'] = route_Id
        df['station_Id'] = station_Id
        df['station_Seq'] = station_Seq
        df['plate_No'] = plate_No
        df.to_csv("test.csv", index=False)
    time.sleep(1)



