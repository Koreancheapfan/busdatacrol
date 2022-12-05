from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from influxdb import InfluxDBClient
from copy import deepcopy
import requests
import lxml
import time
import pprint


seq1 = 0
seq2 = 0

key = 'Fl+MjXgGrTViuvJTy/RB8zodh2OEXStIUPEaFDSeUHAN5iMIG8zqFW4ROqV//eIee3K9KmL3TdAQQmm4cmnoOQ=='
rid = '235000092'

def get_ifdb(db, host='223.130.129.217', port=8086, user='buscrol', passwd='yangju#bu1'):
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
Homebuslist = []
Hometimelist = []
Awaybuslist = []
Awaytimelist = []
bt = 0

for i in range(1140):
    
    try:
        bt = bt + 1
        def bus_data(ifdb):
            url = 'http://apis.data.go.kr/6410000/buslocationservice/getBusLocationList'
            params = {'serviceKey': key, 'routeId': rid}
            response = requests.get(url, params=params)
            soup = BeautifulSoup(response.content, 'xml')
            locations = soup.find_all('busLocationList')
            for busLocationList in locations:
                global seq1, dt, bt
                global seq2
                queryTime = soup.select_one('queryTime').text
                routeId = busLocationList.select_one('routeId').text
                stationId = busLocationList.select_one('stationId').text
                stationSeq = busLocationList.select_one('stationSeq').text
                plateNo = busLocationList.select_one('plateNo').text

                json_body = []
                tablename = 'G1300'
                fieldname = 'zero'
                point = {"measurement": tablename,
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
                    dt = datetime.now()
                    np = deepcopy(point)
                    np['fields'][fieldname] = v
                    np['time'] = dt
                    json_body.append(np)

                ifdb.write_points(json_body)  # json_body에 저장
                result = ifdb.query('select * from %s' % tablename)
                pprint.pprint(result.raw)

                if len(Hometimelist) != 0:
                    if bt > Hometimelist[0] + 20:
                        del Homebuslist[0]
                        del Hometimelist[0]
                        # Homebuslist.remove(0)
                        # Hometimelist.remove(0)
                if len(Awaytimelist) != 0:
                    if bt > Awaytimelist[0] + 20:
                        del Awaybuslist[0]
                        del Awaytimelist[0]
                        # Awaybuslist.remove(0)
                        # Awaytimelist.remove(0)

                if len(Homebuslist) == 0 or plateNo not in Homebuslist:
                    if stationId == "277102386":  # 만약 기점 정류장이면 기점 정류장에있는 버스 정보 저장
                        Homebuslist.append(plateNo)
                        Hometimelist.append(bt)
                        seq1 = seq1 + 1
                        json_body = []
                        tablename = 'HOMEG1300'
                        fieldname = 'zero'
                        point = {"measurement": tablename,
                                 "tags": {
                                     "routeId": routeId,
                                     "stationId": stationId,
                                     "stationSeq": stationSeq,
                                     "plateNo": plateNo,
                                     "homeseqnum": seq1
                                 },
                                 "fields": {
                                     # Initialize data to zero
                                     fieldname: 0
                                 },
                                 "time": None,
                                 }
                        vals = list(range(1))
                        for v in vals:
                            dt = datetime.now()
                            np = deepcopy(point)
                            np['fields'][fieldname] = v
                            np['time'] = dt
                            json_body.append(np)

                        ifdb.write_points(json_body)  # json_body에 저장
                        result = ifdb.query('select * from %s' % tablename)
                        pprint.pprint(result.raw)
                if len(Awaybuslist) == 0 or plateNo not in Homebuslist:
                    if stationId == "277102301" and plateNo not in Awaybuslist:  # 만약 기점 정류장이면 기점 정류장에있는 버스 정보 저장
                        Awaybuslist.append(plateNo)
                        Awaytimelist.append(bt)  # 만약 종점 정류장이면 종점 정류장에있는 버스 정보 저장
                        seq2 = seq2 + 1
                        json_body = []
                        tablename = 'AWAYG1300'
                        fieldname = 'zero'
                        point = {"measurement": tablename,
                                 "tags": {
                                     "routeId": routeId,
                                     "stationId": stationId,
                                     "stationSeq": stationSeq,
                                     "plateNo": plateNo,
                                     "awayseqnum": seq2
                                 },
                                 "fields": {
                                     # Initialize data to zero
                                     fieldname: 0
                                 },
                                 "time": None,
                                 }
                        vals = list(range(1))
                        for v in vals:
                            dt = datetime.now()
                            np = deepcopy(point)
                            np['fields'][fieldname] = v
                            np['time'] = dt
                            json_body.append(np)

                        ifdb.write_points(json_body)  # json_body에 저장
                        result = ifdb.query('select * from %s' % tablename)
                        pprint.pprint(result.raw)


        def data_save():
            # InfluxDB에 접속
            bus_db = get_ifdb(db='Bus_DB')

            # DB에 데이터 쓰기
            bus_data(bus_db)


        if __name__ == '__main__':
            data_save()

        print("====데이터 추출완료====")
        print(len(Homebuslist))
        print(len(Awaybuslist))
        print(Awaybuslist)
        print(Awaytimelist)
        if len(Awaytimelist) != 0:
            print(Awaytimelist[0])
        # print(dt)
        # ct = datetime.now() + timedelta(seconds=1200)
        # print(ct)
        # print(queryTime)
        time.sleep(60)
    except:
        pass


