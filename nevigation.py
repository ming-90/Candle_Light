import urllib
import json
from urllib.request import Request, urlopen
import geocoder

from file import file

naver_client_id = ''
naver_client_secret = ''
odsay_secret = ''
sk_secret = ''

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

    print(f"위도: {latitude}, 경도: {longitude}")

def get_location_from_file():
    aa = file['metaData']['plan']['itineraries'][0]['legs'][1]
    print(aa)

start = "경기도 안산시 상록구 이동 645-4"
end = "서울시 영등포구 양평로 157 선유도투웨니퍼스트밸리"
# start = get_location(start)
# end = get_location(end)

# get_optimal_route(start, end, option='')

# get_gps()
get_location_from_file()