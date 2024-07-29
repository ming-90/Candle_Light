import time
import re
from data.walk import walk

from source import *

# Init
audio = Audio()
gemini = Gemini()
navi = Navigation()

output_wav = "data/output.wav"
output_mp3 = "data/output.mp3"

def main():

    print("1. 음성으로 출발지 설정")
    while True:
        # audio.recorde(output_wav, output_mp3)
        # start = gemini.audio(output_mp3)
        start = "서울 종로구 사직로8길 31 서울경찰청"
        start_loc = navi.get_location(start)
        if not start:
            print("다시 검색해주세요")
            continue
        else:
            print(f"  - {start}")
            break

    print("2. 음성으로 도착지 설정")
    while True:
        # audio.recorde(output_wav, output_mp3)
        # end = gemini.audio(output_mp3)
        end = "서울 중구 세종대로 40"
        end_loc = navi.get_location(end)
        if not start:
            print("다시 검색해주세요")
            continue
        else:
            print(f"  - {end}")
            break

    print("3. 출발지, 도착지 좌표 가져오기")
    navi.get_optimal_route(start_loc, end_loc)

    leg_count = 0
    walk_count = 0

    my_walk = 0 # TODO : Test data
    check_bus = False
    print("4. GPS 좌표 가져오기")
    while True:
        ## 현재 위치 받아 오기
        # my_location = get_gps() # TODO : Real location
        my_location = walk[my_walk] # TODO delete : Test location

        leg = navi.turn_point[leg_count]
        mode = leg['mode']

        if mode == "WALK":
            linestring = leg['steps'][walk_count]['linestring'].split(' ')[-1].split(',')

            # 현재 위치와 다음 포인트 까지 거리 계산
            distance = navi.haversine(my_location, linestring)
            distance = round(distance)

            try:
                # 다음 포인트에서 방향 (좌회전, 우회전) 계산
                turn = navi.direction(
                    my_location,
                    linestring,
                    leg['steps'][walk_count+1]['linestring'].split(' ')[-1].split(',')
                )

                print(f"네비게이션 WALK : {distance} m 앞 {turn} 입니다")

                if distance < 3:
                    walk_count += 1

            except IndexError as I:
                if distance < 3:
                    walk_count = 0
                    leg_count += 1

            my_walk += 1 # TODO delete : Test data

            time.sleep(1)

        elif mode == "BUS":
            # 버스 검색
            if not check_bus:
                bus_image = 'data/bus.jpeg' # TODO : 이미지를 받아 올수 있는 방법으로 변경
                bus_num = gemini.image(bus_image)

                if re.findall(r'\d+', leg['route'])[0] == bus_num:
                    print(f"네비게이션 BUS : {bus_num}번 버스 탑승 입니다")
                    check_bus = True

            # 버스 탑승
            else:
                my_location = walk[my_walk]
                # linestring = [leg['end']['loc'], leg['end']['lat']]
                linestring = leg['passShape']['linestring'].split(' ')[-1].split(',')
                station = leg['end']['name']
                distance = navi.haversine(my_location, linestring)
                distance = round(distance)

                print(f"네비게이션 BUS : {distance} m 앞에 {station} 하차 입니다.")

                if distance < 10:
                    leg_count += 1

                my_walk += 1  # TODO delete : Test data

            time.sleep(1)
        elif mode == "SUBWAY":
            print('SUBWAY')
            time.sleep(1)

main()
