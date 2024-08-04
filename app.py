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
    st.session_state.count = 3
if 'marker' not in st.session_state:
    st.session_state.marker = [37.5750599, 126.9720724]

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
        end_sample = st.button("광화문", key='end-sample')
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

if st.session_state.count >= 3:
    st_write("3. 네비게이션 길 찾기", 22)

    start = "서울 종로구 사직로8길 31 서울경찰청"
    start_loc = navi.get_location(start)
    end = "서울 중구 세종대로 40"
    end_loc = navi.get_location(end)

    # navi.get_optimal_route(start_loc, end_loc)

    # st_write(start_loc, 15)
    # st_write(end_loc, 15)
    # if st.button("test", key="test"):
    #     st.session_state.marker = [st.session_state.marker[0] + 0.00001, st.session_state.marker[1] + 0.000001]

    map = folium.Map(location=[37.5750599, 126.9720724], zoom_start=17, control_scale=True)

    fg = folium.FeatureGroup(name="Markers")

    fg.add_child(
        folium.CircleMarker(st.session_state.marker,
                    radius=7,     # 원의 반지름
                    color='red', # 원의 둘레 색상
                    fill=True,
                    fill_color='white', # 원을 채우는 색
                    fill_opacity=1  # 투명도
                    )
    )

    add_fg(fg, [37.5750599, 126.9720724], 'blue')
    add_fg(fg, [37.5750899, 126.9720724], 'red')
    add_fg(fg, [37.5752099, 126.9720724], 'green')

    st_folium(
        map,
        center=st.session_state.marker,
        key="new",
        feature_group_to_add=fg,
        height=400,
        width=700,
    )

    # time.sleep(1)
