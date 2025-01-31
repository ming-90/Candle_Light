import os
import urllib
import json
import requests
import geocoder
from shapely.geometry import Point, LineString
import math
from dotenv import load_dotenv

from sample.file import file

load_dotenv()

naver_client_id = os.environ.get('NAVER_ID')
naver_client_secret = os.environ.get('NAVER_SECRET')
sk_secret = os.environ.get('SK_SECRET')

class Navigation:
    # def __init__(self):
        # self.start = self.get_location(start)
        # self.end = self.get_location(end)
        # self.get_optimal_route(self.start, self.end)

    def get_gps(self):
        g = geocoder.ip('me')
        latitude = g.latlng[0]
        longitude = g.latlng[1]

        return latitude, longitude

    def get_location(self, loc) :
        url = f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={loc}"

        # 헤더 설정
        headers = {
            'X-NCP-APIGW-API-KEY-ID': naver_client_id,
            'X-NCP-APIGW-API-KEY': naver_client_secret
        }

        # 요청 보내기
        response = requests.get(url, headers=headers)

        # 응답 처리
        res_code = response.status_code
        response_body = response.json()

        if (res_code == 200) : # 응답이 정상적으로 완료되면 200을 return한다
            if response_body['meta']['totalCount'] == 1 :
                # 위도, 경도 좌표를 받아와서 return해 줌.
                lat = response_body['addresses'][0]['y']
                lon = response_body['addresses'][0]['x']
                return (lon, lat)
            else :
                print('location not exist')
                return False

        else :
            print('ERROR')
            return False

    def get_optimal_route(self, start, end, option='' ) :
        url = 'https://apis.openapi.sk.com/transit/routes'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'appKey': sk_secret
        }
        data = {
            "startX": start[0],
            "startY": start[1],
            "endX": end[0],
            "endY": end[1]
        }

        # try:
        #     # TODO : Real data
        #     response = requests.post(url, headers=headers, json=data)
        #     data = response.json()
        # except Exception as e:
        #     # Test
        data = file

        self.turn_point = []
        self.turn_point = data['metaData']['plan']['itineraries'][0]['legs']
        return self.turn_point

    def haversine(self, coord1, coord2):
        # 지구의 반지름 (킬로미터 단위)
        R = 6371.0

        # 위도와 경도를 라디안 단위로 변환
        lat1, lon1 = math.radians(float(coord1[1])), math.radians(float(coord1[0]))
        lat2, lon2 = math.radians(float(coord2[1])), math.radians(float(coord2[0]))

        # 위도와 경도의 차이 계산
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Haversine 공식을 사용하여 거리 계산
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # 두 점 사이의 거리 (킬로미터 단위)
        distance_km = R * c

        # 거리 변환 (미터 단위)
        distance_m = distance_km * 1000

        return distance_m

    def direction(self, p1, p2, p3):
        # 벡터1: p1 -> p2
        p1 = [float(i) for i in p1]
        p2 = [float(i) for i in p2]
        p3 = [float(i) for i in p3]

        vector1 = (p2[0] - p1[0], p2[1] - p1[1])

        # 벡터2: p1 -> p3
        vector2 = (p3[0] - p1[0], p3[1] - p1[1])

        # 외적 계산 (벡터의 z 성분만 필요)
        cross_product = vector1[0] * vector2[1] - vector1[1] * vector2[0]

        if cross_product > 0:
            return "좌회전"
        elif cross_product < 0:
            return "우회전"
        else:
            return "직진"

    def traffic_location(self, turn_point):
        traffic = []
        for leg in turn_point:
            route = ''
            if leg['mode'] == 'BUS':
                route = leg['route']
            traffic += [{
                'mode': leg['mode'],
                'start': [leg['start']['lat'], leg['start']['lon']],
                'end': [leg['end']['lat'], leg['end']['lon']],
                'route': route
            }]
        return traffic

    def move_coor(self, turn_point):
        '''
        테스트용 함수.
        실제로 걸어가면서 테스트 할 수 없기 때문에 네비게이션 데이터에서
        이동하는 좌표들을 모아 내 위치를 표시
        '''
        move = []
        for leg in turn_point:
            linestring = []
            if leg['mode'] == 'WALK':
                for step in leg['steps']:
                    result = [list(map(float, coordinate.split(','))) for coordinate in step['linestring'].split()]
                    linestring.extend(result)
                move += linestring

            elif leg['mode'] == 'BUS':
                result = [list(map(float, coordinate.split(','))) for coordinate in leg['passShape']['linestring'].split()]
                move += result

        return move
