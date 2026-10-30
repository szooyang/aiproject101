
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import html

st.set_page_config(
    page_title="서울 1박 2일 관광 코스",
    page_icon="🗺️",
    layout="wide"
)

# =====================================
# 1. 여행 일정 데이터
# =====================================

itinerary = [

    # 1일 차
    {
        "day": "1일 차",
        "time": "09:00",
        "name": "아침 식사 · 애즈라이크 서촌",
        "kind": "아침",
        "lat": 37.5780,
        "lon": 126.9710,
        "duration": "40분",
        "detail": "샌드위치, 샐러드, 커피로 아침 식사",
        "url": "https://www.google.com/maps/search/?api=1&query=As+Like+Seochon+Seoul"
    },
    {
        "day": "1일 차",
        "time": "09:45",
        "name": "경복궁",
        "kind": "관광",
        "lat": 37.5796,
        "lon": 126.9770,
        "duration": "1시간 15분",
        "detail": "조선 왕조의 법궁과 근정전, 경회루 관람",
        "url": "https://www.google.com/maps/search/?api=1&query=Gyeongbokgung+Palace+Seoul"
    },
    {
        "day": "1일 차",
        "time": "11:10",
        "name": "북촌한옥마을",
        "kind": "관광",
        "lat": 37.5826,
        "lon": 126.9830,
        "duration": "50분",
        "detail": "전통 한옥 골목과 한국의 주거 문화 체험",
        "url": "https://www.google.com/maps/search/?api=1&query=Bukchon+Hanok+Village+Seoul"
    },
    {
        "day": "1일 차",
        "time": "12:10",
        "name": "점심 · 삼청동 수제비",
        "kind": "점심",
        "lat": 37.5840,
        "lon": 126.9810,
        "duration": "1시간",
        "detail": "수제비와 감자전 등 한국 음식",
        "url": "https://www.google.com/maps/search/?api=1&query=Samcheongdong+Sujebi+Seoul"
    },
    {
        "day": "1일 차",
        "time": "13:20",
        "name": "명동",
        "kind": "관광",
        "lat": 37.5636,
        "lon": 126.9869,
        "duration": "1시간",
        "detail": "화장품, 패션 매장과 길거리 음식 쇼핑",
        "url": "https://www.google.com/maps/search/?api=1&query=Myeongdong+Seoul"
    },
    {
        "day": "1일 차",
        "time": "14:40",
        "name": "N서울타워",
        "kind": "관광",
        "lat": 37.5512,
        "lon": 126.9882,
        "duration": "1시간 30분",
        "detail": "남산에서 서울 도심 전망 감상",
        "url": "https://www.google.com/maps/search/?api=1&query=N+Seoul+Tower"
    },
    {
        "day": "1일 차",
        "time": "16:30",
        "name": "저녁 · 명동교자",
        "kind": "저녁",
        "lat": 37.5630,
        "lon": 126.9855,
        "duration": "1시간",
        "detail": "칼국수와 만두로 유명한 명동 식당",
        "url": "https://www.google.com/maps/search/?api=1&query=Myeongdong+Kyoja+Seoul"
    },

    # 2일 차
    {
        "day": "2일 차",
        "time": "09:00",
        "name": "아침 · 광장시장",
        "kind": "아침",
        "lat": 37.5700,
        "lon": 126.9997,
        "duration": "45분",
        "detail": "빈대떡, 김밥 등 한국 전통시장 먹거리",
        "url": "https://www.google.com/maps/search/?api=1&query=Gwangjang+Market+Seoul"
    },
    {
        "day": "2일 차",
        "time": "09:50",
        "name": "광장시장",
        "kind": "관광",
        "lat": 37.5700,
        "lon": 126.9997,
        "duration": "35분",
        "detail": "한국의 전통시장과 다양한 먹거리 체험",
        "url": "https://www.google.com/maps/search/?api=1&query=Gwangjang+Market+Seoul"
    },
    {
        "day": "2일 차",
        "time": "10:40",
        "name": "동대문디자인플라자",
        "kind": "관광",
        "lat": 37.5671,
        "lon": 127.0095,
        "duration": "50분",
        "detail": "독특한 건축물과 디자인 전시 공간 관람",
        "url": "https://www.google.com/maps/search/?api=1&query=Dongdaemun+Design+Plaza"
    },
    {
        "day": "2일 차",
        "time": "12:00",
        "name": "점심 · 코엑스몰 식당가",
        "kind": "점심",
        "lat": 37.5116,
        "lon": 127.0592,
        "duration": "50분",
        "detail": "코엑스몰에서 한식과 다양한 세계 음식 선택",
        "url": "https://www.google.com/maps/search/?api=1&query=restaurants+COEX+Mall+Seoul"
    },
    {
        "day": "2일 차",
        "time": "13:00",
        "name": "코엑스·별마당도서관",
        "kind": "관광",
        "lat": 37.5116,
        "lon": 127.0592,
        "duration": "55분",
        "detail": "별마당도서관과 코엑스 쇼핑몰 관람",
        "url": "https://www.google.com/maps/search/?api=1&query=Starfield+Library+COEX"
    },
    {
        "day": "2일 차",
        "time": "14:05",
        "name": "강남역",
        "kind": "관광",
        "lat": 37.4979,
        "lon": 127.0276,
        "duration": "45분",
        "detail": "서울의 현대적인 상업 거리와 쇼핑 공간",
        "url": "https://www.google.com/maps/search/?api=1&query=Gangnam+Station+Seoul"
    },
    {
        "day": "2일 차",
        "time": "15:10",
        "name": "서울숲",
        "kind": "관광",
        "lat": 37.5444,
        "lon": 127.0374,
        "duration": "45분",
        "detail": "도심 속 공원에서 산책과 휴식",
        "url": "https://www.google.com/maps/search/?api=1&query=Seoul+Forest"
    },
    {
        "day": "2일 차",
        "time": "16:10",
        "name": "홍대 거리",
        "kind": "관광",
        "lat": 37.5563,
        "lon": 126.9236,
        "duration": "1시간 10분",
        "detail": "거리 공연과 개성 있는 상점, 젊은 문화 체험",
        "url": "https://www.google.com/maps/search/?api=1&query=Hongdae+Street+Seoul"
    },
    {
        "day": "2일 차",
        "time": "17:30",
        "name": "저녁 · 홍대 식당가",
        "kind": "저녁",
        "lat": 37.5560,
        "lon": 126.9230,
        "duration": "1시간 15분",
        "detail": "한국식 구이, 치킨, 한식 등 저녁 식사",
        "url": "https://www.google.com/maps/search/?api=1&query=Korean+restaurants+Hongdae+Seoul"
    }
]


# =====================================
# 2. 호텔 추천 데이터
# =====================================

hotels = [
    {
        "name": "호텔 PJ 명동",
        "area": "충무로·을지로",
        "reason": "명동, 남산, 광장시장, 동대문 이동에 편리한 위치",
        "url": "https://www.google.com/maps/search/?api=1&query=Hotel+PJ+Myeongdong"
    },
    {
        "name": "롯데시티호텔 명동",
        "area": "을지로3가·명동",
        "reason": "도심 중심부에 위치해 쇼핑과 지하철 이동에 편리",
        "url": "https://www.google.com/maps/search/?api=1&query=LOTTE+City+Hotel+Myeongdong"
    },
    {
        "name": "포시즌스 호텔 서울",
        "area": "광화문",
        "reason": "경복궁과 광화문 관광에 편리한 고급 호텔",
        "url": "https://www.google.com/maps/search/?api=1&query=Four+Seasons+Hotel+Seoul"
    }
]


# =====================================
# 3. 화면 제목
# =====================================

st.title("🗺️ 서울 주요 관광지 TOP 10")
st.subheader("1박 2일 서울 여행 플래너")

st.write(
    "오전 9시부터 오후 7시까지 "
    "서울의 대표 관광지를 둘러보는 추천 일정입니다."
)

st.info(
    "관광지 10곳을 모두 포함한 압축 일정입니다. "
    "특히 2일 차는 이동 거리가 길어 다소 바쁠 수 있습니다."
)


# =====================================
# 4. 호텔 추천
# =====================================

st.header("🏨 추천 호텔")

st.write(
    "전체 여행 동선을 고려하면 "
    "명동·충무로·을지로 주변에 숙소를 잡는 것이 좋습니다."
)

hotel_cols = st.columns(3)

for col, hotel in zip(hotel_cols, hotels):

    with col:

        st.subheader(hotel["name"])

        st.caption(hotel["area"])

        st.write(hotel["reason"])

        st.link_button(
            "호텔 위치 및 예약 정보 ↗",
            hotel["url"],
            use_container_width=True
        )

st.caption(
    "호텔 링크는 지도 검색 링크입니다. "
    "요금과 객실 예약 가능 여부는 방문 날짜에 따라 확인하세요."
)


# =====================================
# 5. 식당 추천
# =====================================

st.header("🍽️ 동선에 맞춘 식당 추천")

meal_data = [
    {
        "meal": "1일 차 아침",
        "name": "애즈라이크 서촌",
        "menu": "샌드위치·샐러드·커피",
        "reason": "경복궁과 가까운 서촌에서 아침 식사",
        "url": "https://www.google.com/maps/search/?api=1&query=As+Like+Seochon+Seoul"
    },
    {
        "meal": "1일 차 점심",
        "name": "삼청동 수제비",
        "menu": "수제비·감자전",
        "reason": "북촌한옥마을 관람 후 식사하기 좋은 위치",
        "url": "https://www.google.com/maps/search/?api=1&query=Samcheongdong+Sujebi+Seoul"
    },
    {
        "meal": "1일 차 저녁",
        "name": "명동교자",
        "menu": "칼국수·만두",
        "reason": "남산 관람 후 명동으로 내려와 식사",
        "url": "https://www.google.com/maps/search/?api=1&query=Myeongdong+Kyoja+Seoul"
    },
    {
        "meal": "2일 차 아침",
        "name": "광장시장",
        "menu": "빈대떡·김밥",
        "reason": "첫 관광지인 광장시장에서 바로 식사",
        "url": "https://www.google.com/maps/search/?api=1&query=Gwangjang+Market+Seoul"
    },
    {
        "meal": "2일 차 점심",
        "name": "코엑스몰 식당가",
        "menu": "한식·세계 음식",
        "reason": "DDP 관람 후 강남 이동 중 식사",
        "url": "https://www.google.com/maps/search/?api=1&query=restaurants+COEX+Mall+Seoul"
    },
    {
        "meal": "2일 차 저녁",
        "name": "홍대 식당가",
        "menu": "구이·치킨·한식",
        "reason": "마지막 관광지 홍대에서 저녁 식사",
        "url": "https://www.google.com/maps/search/?api=1&query=Korean+restaurants+Hongdae+Seoul"
    }
]

meal_cols = st.columns(3)

for i, meal in enumerate(meal_data):

    with meal_cols[i % 3]:

        st.markdown(
            f"**{meal['meal']} · {meal['name']}**"
        )

        st.caption(meal["menu"])

        st.write(meal["reason"])

        st.markdown(
            f"[식당 위치 및 메뉴 확인 ↗]({meal['url']})"
        )

st.caption(
    "식당의 영업시간, 휴무일, 가격 및 대기 여부는 "
    "방문 전에 확인하세요."
)


# =====================================
# 6. 지도 표시
# =====================================

st.divider()

st.header("📍 서울 여행 동선 지도")

day_filter = st.radio(
    "지도 표시 선택",
    ["전체 일정", "1일 차", "2일 차"],
    horizontal=True
)

if day_filter == "전체 일정":

    visible = itinerary

else:

    visible = [
        p for p in itinerary
        if p["day"] == day_filter
    ]


m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    control_scale=True
)

day_colors = {
    "1일 차": "red",
    "2일 차": "blue"
}


for p in visible:

    popup_html = f"""
    <div style="width:250px">
        <h4>{html.escape(p['name'])}</h4>
        <b>{p['day']} · {p['time']}</b>
        <p>{html.escape(p['detail'])}</p>
        <a href="{p['url']}" target="_blank">
            장소 정보 확인
        </a>
    </div>
    """

    marker_icon = (
        "cutlery"
        if p["kind"] in ["아침", "점심", "저녁"]
        else "info-sign"
    )

    folium.Marker(
        location=[p["lat"], p["lon"]],
        tooltip=f"{p['time']} · {p['name']}",
        popup=folium.Popup(
            popup_html,
            max_width=300
        ),
        icon=folium.Icon(
            color=day_colors[p["day"]],
            icon=marker_icon
        )
    ).add_to(m)


# 날짜별 이동 순서 연결
for day in ["1일 차", "2일 차"]:

    day_points = [
        p for p in visible
        if p["day"] == day
    ]

    if len(day_points) > 1:

        folium.PolyLine(
            [
                [p["lat"], p["lon"]]
                for p in day_points
            ],
            color=day_colors[day],
            weight=3,
            opacity=0.65
        ).add_to(m)


if visible:

    m.fit_bounds(
        [
            [p["lat"], p["lon"]]
            for p in visible
        ],
        padding=(25, 25)
    )


st_folium(
    m,
    use_container_width=True,
    height=570,
    returned_objects=[]
)

st.caption(
    "빨간색은 1일 차, 파란색은 2일 차입니다. "
    "지도 연결선은 실제 도로 경로가 아닌 방문 순서를 나타냅니다."
)


# =====================================
# 7. 상세 일정표
# =====================================

st.divider()

st.header("🗓️ 1박 2일 상세 일정표")

st.write(
    "지도 아래에서 날짜별 여행 일정을 확인할 수 있습니다."
)

for day in ["1일 차", "2일 차"]:

    st.subheader(day)

    rows = []

    for p in itinerary:

        if p["day"] == day:

            rows.append({
                "시간": p["time"],
                "방문 장소": p["name"],
                "구분": p["kind"],
                "체류 시간": p["duration"],
                "주요 활동": p["detail"],
                "장소 링크": p["url"]
            })

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "시간": st.column_config.TextColumn(
                "시간",
                width="small"
            ),
            "방문 장소": st.column_config.TextColumn(
                "방문 장소",
                width="medium"
            ),
            "구분": st.column_config.TextColumn(
                "구분",
                width="small"
            ),
            "체류 시간": st.column_config.TextColumn(
                "체류 시간",
                width="small"
            ),
            "주요 활동": st.column_config.TextColumn(
                "주요 활동",
                width="large"
            ),
            "장소 링크": st.column_config.LinkColumn(
                "지도 링크",
                display_text="위치 보기 ↗"
            )
        }
    )


# =====================================
# 8. 여행 안내
# =====================================

st.divider()

st.header("💡 여행 전 확인 사항")

st.markdown("""
- 경복궁은 매주 화요일 휴궁하므로 방문 요일을 확인하세요.
- 북촌한옥마을은 주민 거주 지역이므로 관람 예절을 지켜 주세요.
- 서울 지하철과 버스를 이용하면 편리합니다.
- 관광지의 운영시간과 휴관일을 미리 확인하세요.
- 식당과 호텔의 가격 및 예약 가능 여부는 방문일 기준으로 확인하세요.
""")

st.markdown(
    "[서울 공식 관광 정보](https://english.visitseoul.net/)  \n"
    "[서울교통공사](https://www.seoulmetro.co.kr/)  \n"
    "[대한민국 구석구석](https://korean.visitkorea.or.kr/)"
)

st.caption(
    "서울의 주요 관광지 10곳을 포함한 추천 일정입니다. "
    "교통 상황에 따라 방문 순서와 체류 시간을 조정할 수 있습니다."
)
