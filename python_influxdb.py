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

def get_ifdb(db, host='54.180.128.66', port=8086, user='ssg', passwd='qwer1234'):
    # InfluxDB에 연결하기 위한 정보를 포함하는 객체 생성
    client = InfluxDBClient(host, port, user, passwd, db)

    try:
        # 데이터베이스 생성 시도.
        client.create_database(db)

        # DB를 만들 수 있거나 DB가 있는 경우
        print('========접속  성공=======')
        print('=======================')
        print('        접속  정보')
        print('=======================')
        print('host :', host)
        print('port :', port)
        print('username :', user)
        print('database :', db)
    except:
        # DB에 접속을 할수 없는경우
        print('Connection Failed')
        pass

    return client


def bus_data(ifdb):
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
        tablename = 'G1300'
        fieldname = 'zero'
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



        ifdb.write_points(json_body)    #json_body에 저장


    result = ifdb.query('select * from %s' % tablename)
    pprint.pprint(result.raw)


def data_save():
    # InfluxDB에 접속
    bus_db = get_ifdb(db='Bus_DB')

    # DB에 데이터 쓰기
    bus_data(bus_db)


if __name__ == '__main__':
    data_save()