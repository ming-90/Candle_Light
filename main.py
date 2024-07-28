import time

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

    walking = 0
    print("4. GPS 좌표 가져오기")
    while True:
        ## 현재 위치 받아 오기
        # my_location = get_gps() # Real location
        my_location = walk[walking] # Test location

        ## 현재 위치와 다음 포인트 까지 거리 계산
        distance = navi.haversine(my_location, navi.turn_point[0])
        distance = round(distance)

        ## 다음 포인트에서 방향 (좌회전, 우회전) 계산
        turn = navi.direction(my_location, navi.turn_point[0], navi.turn_point[1])

        print(f"네비게이션 : {distance} m 앞 {turn} 입니다")

        if distance < 3:
            del navi.turn_point[0]

        time.sleep(2)
        walking += 1


main()
