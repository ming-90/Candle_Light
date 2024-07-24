from nevigation import *
import time

from data.walk import walk


def main():
    start = "서울 종로구 사직로8길 31 서울경찰청"
    end = "서울 중구 세종대로 40"

    print("1. 출발지, 도착지 좌표 가져오기")
    navi = Navigation(start, end)
    walking = 0

    while True:
        print("2. GPS 좌표 가져오기")
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
