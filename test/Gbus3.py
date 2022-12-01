from bs4 import BeautifulSoup   #크롤링할 데이터 분석을 위해 사용.
import requests                 #open api애서 데이터를 가져오기 위해 사용.
import time                     #타임 슬립을 사용하기 위해 사용.

key = 'Fl+MjXgGrTViuvJTy/RB8zodh2OEXStIUPEaFDSeUHAN5iMIG8zqFW4ROqV//eIee3K9KmL3TdAQQmm4cmnoOQ=='    #key값을 변수에 저장
rid = '235000092'           #얻고자하는 정보의 값을 변수에 저장


def bus():                      #함수선언
    for i in range(1000):       # 계속 반복하게 반복문 사용
        url = 'http://apis.data.go.kr/6410000/busrouteservice/getBusRouteInfoItem'        #open api 주소
        params ={'serviceKey' : key, 'routeId' : rid }              #open api를 사용하기 위한 키값과 얻고자하는 변수의 값
        response = requests.get(url, params=params)                 #response이라는 변수에 requests라이브러리를 이용하여 url정보를 가져옴
        soup = BeautifulSoup(response.content, 'xml')  #soup라는 변수에 xml파일 형식의 데이터를 저장
        print(soup)
        locations = soup.select('busRouteInfoItem')                  # locations 변수 내에 busLocationList에 해당하는 내용만 select
        for busRouteInfoItem in locations:                           # 반복문 사용
            queryTime= soup.select('queryTime')                     #queryTime이라는 변수에soup안에 queryTime이라는 데이터를 저장
            routeId = busRouteInfoItem.select_one('routeName').text            #routeId(노선id)안에있는 데이터를 하나만 select하여 routeId라는 변수에 저장
            stationId = busRouteInfoItem.select_one('startStationName').text        #stationId(정류소id)안에있는 데이터를 하나만 select하여 stationId라는 변수에 저장
            stationSeq = busRouteInfoItem.select_one('endStationName').text      #stationSeq(정류소순번)안에있는 데이터를 하나만 select하여 stationSeq라는 변수에 저장
            plateNo = busRouteInfoItem.select_one('plateNo').text            #plateNo(버스번호)안에있는 데이터를 하나만 select하여 라는 변수에 저장
            print(routeId ,stationSeq, stationId, plateNo)                  #변수값들이 잘 저장되었는지 출력
        time.sleep(60)                                                      #60초에 한번 실행되게 시간 지연

bus()                       #해당 함수 실행
