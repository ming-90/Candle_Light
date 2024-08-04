import streamlit as st
from source import *
from streamlit_folium import st_folium
import folium

import time

## Streamlit option
def st_write(text, size):
    new_title = f'<p style="font-family:sans-serif; font-size: {size}px;">{text}</p>'
    st.markdown(new_title, unsafe_allow_html=True)

## Streamlit session
if 'start_text' not in st.session_state:
    st.session_state.start_text = ""
if 'end_text' not in st.session_state:
    st.session_state.end_text = ""
if 'count' not in st.session_state:
    st.session_state.count = 1
if 'walk' not in st.session_state:
    st.session_state.walk = []
if 'walk_count' not in st.session_state:
    st.session_state.walk_count = 0
if 'mode' not in st.session_state:
    st.session_state.mode = 'WALK'
if 'leg' not in st.session_state:
    st.session_state.leg = 0
if 'bus' not in st.session_state:
    st.session_state.bus = False
if 'turn_point' not in st.session_state:
    st.session_state.turn_point = []


audio = Audio()
gemini = Gemini()
navi = Navigation()

st.title("네비게이션")

if st.session_state.count >= 1:
    ## 출발지 음성 INPUT
    st_write("1. 출발지 음성 검색 (STT with Gemini)", '22')

    col1, col2 = st.columns([7,3])
    with col1:
        st_write('출발지 음성 녹음', '13')
        start_mic = st.button("마이크 켜기", key='start-mic')
    with col2:
        ## 출발지 음성 샘플
        st_write('출발지 음성 샘플', '13')
        start_sample = st.button("서울경찰청", key='start-sample')
        if start_sample:
            start_sample = 'sample/start.mp3'

    text = ""
    if start_mic:
        audio.recorde('data/start.wav', 'data/start.mp3')
        ## STT with Gemini
        st.session_state.start_text = gemini.audio('data/start.mp3')
    if start_sample:
        st.session_state.start_text = gemini.audio(start_sample)
    if st.session_state.start_text != "":
        st_write(st.session_state.start_text, 15)
        st.session_state.count += 1


if st.session_state.count >= 2:
    ## 도착지 음성 INPUT
    st_write("2. 도착지 음성 검색 (STT with Gemini)", 22)

    col1, col2 = st.columns([7,3])
    with col1:
        st_write('도착지 음성 녹음', '13')
        end_mic = st.button("마이크 켜기", key='end-mic')
    with col2:
        ## 도착지 음성 샘플
        st_write('도착지 음성 샘플', '13')
        end_sample = st.button("숭례문", key='end-sample')
        if end_sample:
            end_sample = 'sample/end.mp3'

    text = ""
    if end_mic:
        path = audio.recorde('data/end.wav', 'data/end.mp3')
        ## STT with Gemini
        st.session_state.end_text = gemini.audio(path)
    if end_sample:
        st.session_state.end_text = gemini.audio(end_sample)

    if st.session_state.end_text != "":
        st_write(st.session_state.end_text, 15)
        st.session_state.count += 1


def add_fg(fg, coor, color):
    fg.add_child(
        folium.Marker(
            location = coor,
            icon=folium.Icon(color=color,icon='star')
            )
    )

def my_location_fg(fg):
    fg.add_child(
        folium.CircleMarker(st.session_state.walk,
                    radius=7,     # 원의 반지름
                    color='red', # 원의 둘레 색상
                    fill=True,
                    fill_color='white', # 원을 채우는 색
                    fill_opacity=1  # 투명도
                    )
    )

def dumy_location():
    walk = navi.move_coor(st.session_state.turn_point)
    return walk[st.session_state.walk_count][::-1]

def cal_traffic(traffics):
    for traffic in traffics:
        # 현재 위치와 다음 포인트 까지 거리 계산
        distance = navi.haversine(
            st.session_state.walk,
            traffic['start']
        )
        distance = round(distance)
        print(distance)
        if distance < 5:
            return True
        else:
            return False

if st.session_state.count >= 3:
    st_write("3. 네비게이션 길 찾기", 22)

    start = "서울 종로구 사직로8길 31 서울경찰청"
    start_loc = navi.get_location(start)
    end = "서울 중구 세종대로 40"
    end_loc = navi.get_location(end)

    # 네비게이션 정보
    if st.session_state == []:
        st.session_state.turn_point = navi.get_optimal_route(start_loc, end_loc)
    traffics = navi.traffic_location(st.session_state.turn_point)

    # 지도 정보 INIT
    map = folium.Map(location=start_loc, zoom_start=17, control_scale=True)
    fg = folium.FeatureGroup(name="Markers")

    # 출발지 마크
    add_fg(fg, start_loc[::-1], 'blue')
    # 도착지 마크
    add_fg(fg, end_loc[::-1], 'red')
    # 버스, 지하철 마크
    for traffic in traffics:
        if traffic['mode'] != 'WALK':
            add_fg(fg, traffic['start'], 'green')

    if st.button('걷기'):
        st.session_state.walk_count += 1

    # TODO : 테스트용 내 위치 더미 데이터
    try:
        st.session_state.walk = dumy_location()
    except IndexError as e:
        st.session_state.mode = 'END'
        st_write("도착지에 도착했습니다.", 15)

    if st.session_state.mode == 'WALK':
        # IP 를 이용하여 현재 위치 받아오기
        # st.session_state.walk = navi.get_gps()

        # 내위치 마크
        my_location_fg(fg)

        st_folium(
            map,
            center=st.session_state.walk,
            key="new",
            feature_group_to_add=fg,
            height=400,
            width=700,
        )

        distance = navi.haversine(
            st.session_state.walk,
            traffics[st.session_state.leg]['end']
        )

        st_write(f'{distance}m 도착 입니다.', 15)

        if distance < 5:
            st.session_state.leg += 1
            st.session_state.mode = traffics[st.session_state.leg]['mode']

    elif st.session_state.mode =='BUS':
        st_write('4. 버스 번호 확인 (OCR with Gemini)', '22')
        if st.session_state.bus:
            my_location_fg(fg)

            # 내위치 마크
            my_location_fg(fg)

            st_folium(
                map,
                center=st.session_state.walk,
                key="new",
                feature_group_to_add=fg,
                height=400,
                width=700,
            )

            distance = navi.haversine(
                st.session_state.walk,
                traffics[st.session_state.leg]['end']
            )

            st_write(f'{distance}m 앞 하차입니다.', 15)

            if distance < 5:
                st.session_state.leg += 1
                st.session_state.mode = traffics[st.session_state.leg]['mode']

        else:
            col1, col2 = st.columns([7,3])
            with col1:
                img_file = st.file_uploader('이미지를 업로드 하세요.', type=['png', 'jpg', 'jpeg'])
            with col2:
                st_write('버스 이미지 샘플', '13')
                img_sample = st.button("샘플", key='img-sample')
                if img_sample:
                    img_sample = 'sample/bus.jpeg'

            if img_file:
                bus_num = 0
                with open(('data/bus.jpeg'), 'wb') as f:
                    f.write(img_file.getbuffer()) # 해당 내용은 Buffer로 작성하겠다.
                bus_num = gemini.image('data/bus.jpeg')

                if bus_num in traffics[st.session_state.leg]['route']:
                    st_write(f'{bus_num} 번 버스 탑습 입니다.', 15)
                    st.session_state.bus = True
                else:
                    st_write(f'{bus_num} 번 버스는 탑승 버스가 아닙니다.', 15)

            if img_sample:
                bus_num = gemini.image('sample/bus.jpeg')
                print(bus_num, traffics[st.session_state.leg]['route'])
                if bus_num in traffics[st.session_state.leg]['route']:
                    st_write(f'{bus_num} 번 버스 탑습 입니다.', 15)
                    st.session_state.bus = True


