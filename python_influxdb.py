from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from influxdb import InfluxDBClient
from copy import deepcopy
import requests
import lxml
import time
import pprint
import time


key = 'Fl+MjXgGrTViuvJTy/RB8zodh2OEXStIUPEaFDSeUHAN5iMIG8zqFW4ROqV//eIee3K9KmL3TdAQQmm4cmnoOQ=='
rid = '235000092'


url = 'http://apis.data.go.kr/6410000/buslocationservice/getBusLocationList'
params ={'serviceKey' : key, 'routeId' : rid }
response = requests.get(url, params=params)
soup = BeautifulSoup(response.content, 'xml')
locations = soup.select('busLocationList')
for busLocationList in locations:
    queryTime= soup.select_one('queryTime').text
    routeId = busLocationList.select_one('routeId').text
    stationId = busLocationList.select_one('stationId').text
    stationSeq = busLocationList.select_one('stationSeq').text
    plateNo = busLocationList.select_one('plateNo').text
    print(queryTime, routeId ,stationSeq, stationId, plateNo)


def get_ifdb(db, host='54.180.128.66', port=8086, user='ssg', passwd='qwer1234'):
    # Create an object include information for connect to the InfluxDB
    client = InfluxDBClient(host, port, user, passwd, db)

    try:
        # Try to Create database
        client.create_database(db)

        # If you can create database or have a database
        # there is no problem connecting to the InfluxDB
        print('========접속  성공=======')
        print('=======================')
        print('        접속  정보')
        print('=======================')
        print('host :', host)
        print('port :', port)
        print('username :', user)
        print('database :', db)
    except:
        # Generate error if you can't create database (can't connect to ifdb)
        print('Connection Failed')
        pass

    return client


def my_test(ifdb):
    url = 'http://apis.data.go.kr/6410000/buslocationservice/getBusLocationList'
    params = {'serviceKey': key, 'routeId': rid}
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, 'xml')
    locations = soup.find_all('busLocationList')
    for busLocationList in locations:
        queryTime = soup.select_one('queryTime').text
        routeId = busLocationList.select_one('routeId').text
        stationId = busLocationList.select_one('stationId').text
        stationSeq = busLocationList.select_one('stationSeq').text
        plateNo = busLocationList.select_one('plateNo').text

        json_body = []
        tablename = 'bus'
        fieldname = 'bus_info'
        point = {            "measurement": tablename,
            "tags": {
                "routeId": routeId,
                "stationId": stationId,
                "stationSeq": stationSeq,
                "plateNo": plateNo
            },
            "fields": {
                # Initialize data to zero
                fieldname: 0
            },
            "time": None,
        }
        vals = list(range(1))

        for v in vals:
            # InfluxDB is based on UTC
            # so it should be timed with KCT
            dt = datetime.now() - timedelta(hours=-9)

            np = deepcopy(point)
            np['fields'][fieldname] = v
            np['time'] = dt
            json_body.append(np)


        # Write the data for 10 seconds on the influxDB at once
        ifdb.write_points(json_body)
    # save points in the json_body

    # vals = [1, 2, ... 9, 10]


    result = ifdb.query('select * from %s' % tablename)
    pprint.pprint(result.raw)


def do_test():
    # Connect to InfluxDB
    mydb = get_ifdb(db='myDB')

    # DB에 데이터 쓰기
    my_test(mydb)


if __name__ == '__main__':
    do_test()