import urllib
import json
import requests
import geocoder
from shapely.geometry import Point, LineString
import math

from data.file import file
from data.file2 import file as file2

naver_client_id = 'glb0gfor6m'
naver_client_secret = 'Nc7MTdjiVg2VUCdEki0IXjm59j5FLwAAfu4p73rY'
odsay_secret = 'VYHh//C1T/566H9k3t1PrAurE2nh1VVxFYwT08637Fk'
sk_secret = 'PA42941D6i1vXYkzyNQ6r9nvYbUghfh4aeDmMHnz'

def get_location(loc) :
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

    else :
        print('ERROR')



def get_gps():
    g = geocoder.ip('me')
    latitude = g.latlng[0]
    longitude = g.latlng[1]

    return latitude, longitude


def get_location_from_file():
    steps = file['metaData']['plan']['itineraries'][0]['legs'][0]['steps']

    linestring = []
    for step in steps:
        linestring += step['linestring'].split(' ')

    print(linestring)

def line_locate(current_location, point):
    line = LineString(point)

    # 현재 위치를 Shapely Point 객체로 변환합니다.
    current_point = Point(current_location)

    # 선분 위에 있는지 확인합니다.
    # 현재 위치가 선분 위에 있거나, 선분의 경계점에 있는 경우 True를 반환합니다.
    is_on_line = line.distance(current_point) < 1e-4  # 허용 오차를 사용하여 부동 소수점 비교

    print(is_on_line)  # True 또는 False를 반환합니다.



# start = "서울 종로구 사직로8길 31 서울경찰청"
# point1 = (126.9720724,37.5750599)
# end = "서울 중구 세종대로 40"
# point2 = (126.9753282,37.5599922)
# start = get_location(start)
# end = get_location(end)

# get_optimal_route(start, end, option='')

# get_gps()
# get_location_from_file()


# print(haversine(point1, point2))
# print(file['metaData']['plan']['itineraries'][0]['legs'][0])
# aa = 0
# end_list = []
# walk_list = []
# print(file['metaData']['plan']['itineraries'][0]['legs'][aa])
# steps = file2['metaData']['plan']['itineraries'][0]['legs'][aa]['steps']
# for step in steps:
#     walk_list.append(step['linestring'].split(' '))

# for i in walk_list:
#     for j in i:
#         end_list.append(j.split(','))

# print(end_list)

class Navigation:
    def __init__(self, start, end):
        self.start = get_location(start)
        self.end = get_location(end)
        self.get_optimal_route(self.start, self.end)

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

        # Real data
        # response = requests.post(url, headers=headers, json=data)
        # data = response.json()

        # Test
        data = file2

        self.turn_point = []
        steps = data['metaData']['plan']['itineraries'][0]['legs'][0]['steps']
        for step in steps:
            self.turn_point.append(step['linestring'].split(' ')[-1].split(','))

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