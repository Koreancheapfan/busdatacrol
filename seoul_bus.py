from bs4 import BeautifulSoup
import requests
import datetime
import json
info_url = 'https://bus.go.kr/xmlRequest/getStationByUid.jsp?strBusNumber=23248'
response = requests.get(info_url)
soup = BeautifulSoup(response.content, 'html.parser')
locations = soup.select('stationList')
for stationList in locations:
    print(stationList.select_one('rtNm'), stationList.select_one('arrmsg1'),  stationList.select_one('arrmsg2'))

