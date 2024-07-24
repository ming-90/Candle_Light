import urllib
import json
from urllib.request import Request, urlopen
import geocoder
from shapely.geometry import Point, LineString
import math

from file import file

naver_client_id = 'glb0gfor6m'
naver_client_secret = 'Nc7MTdjiVg2VUCdEki0IXjm59j5FLwAAfu4p73rY'
odsay_secret = 'VYHh//C1T/566H9k3t1PrAurE2nh1VVxFYwT08637Fk'
sk_secret = 'PA42941D6i1vXYkzyNQ6r9nvYbUghfh4aeDmMHnz'

def get_location(loc) :
    url = f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=" \
            + urllib.parse.quote(loc)

    # 주소 변환
    request = urllib.request.Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', naver_client_id)
    request.add_header('X-NCP-APIGW-API-KEY', naver_client_secret)

    response = urlopen(request)
    res = response.getcode()

    if (res == 200) : # 응답이 정상적으로 완료되면 200을 return한다
        response_body = response.read().decode('utf-8')
        response_body = json.loads(response_body)
        print(response_body)
        # 주소가 존재할 경우 total count == 1이 반환됨.
        if response_body['meta']['totalCount'] == 1 :
            # 위도, 경도 좌표를 받아와서 return해 줌.
            lat = response_body['addresses'][0]['y']
            lon = response_body['addresses'][0]['x']
            return (lon, lat)
        else :
            print('location not exist')

    else :
        print('ERROR')

def get_optimal_route(start, goal, option='' ) :

    encoded_api_key = urllib.parse.quote(odsay_secret, safe='')
    urlInfo = f"https://api.odsay.com/v1/api/searchPubTransPathT?lang=0&"\
            + f"SX={start[0]}&SY={start[1]}&EX={end[0]}&EY={end[1]}"\
            + f"&apiKey={encoded_api_key}"

    request = urllib.request.Request(urlInfo)

    response = urlopen(request)
    res = response.getcode()

    if (res == 200) : # 응답이 정상적으로 완료되면 200을 return한다
        response_body = response.read().decode('utf-8')
        response_body = json.loads(response_body)
        print(response_body)

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


def haversine(coord1, coord2):
    # 지구의 반지름 (킬로미터 단위)
    R = 6371.0

    # 위도와 경도를 라디안 단위로 변환
    lat1, lon1 = math.radians(coord1[1]), math.radians(coord1[0])
    lat2, lon2 = math.radians(coord2[1]), math.radians(coord2[0])

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

start = "경기도 안산시 상록구 이동 645-4"
end = "서울시 영등포구 양평로 157 선유도투웨니퍼스트밸리"
# start = get_location(start)
# end = get_location(end)

# get_optimal_route(start, end, option='')

# get_gps()
# get_location_from_file()
point1 = (126.8463,37.313393)
point2 = (126.84635,37.31414)

# print(haversine(point1, point2))
# print(file['metaData']['plan']['itineraries'][0]['legs'][0])
aa = 0
print(file['metaData']['plan']['itineraries'][0]['legs'][aa]['steps'])
# print(file['metaData']['plan']['itineraries'][0]['legs'][aa]['mode'])

# line_locate((126.84627, 37.313635), [point1,point2])

class Navigation:
    def __init__(self):
        self.status = 0