
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 관광 명소 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

# 관광지 데이터
attractions = [
    {
        "name": "명동",
        "english": "Myeong-dong",
        "category": "쇼핑·먹거리",
        "lat": 37.5636,
        "lon": 126.9869,
        "description": "화장품, 패션 매장과 다양한 길거리 음식을 즐길 수 있는 대표 쇼핑 거리입니다."
    },
    {
        "name": "N서울타워",
        "english": "N Seoul Tower",
        "category": "전망·랜드마크",
        "lat": 37.5512,
        "lon": 126.9882,
        "description": "남산 정상에서 서울의 아름다운 전경을 감상할 수 있는 명소입니다."
    },
    {
        "name": "코엑스·별마당도서관",
        "english": "COEX & Starfield Library",
        "category": "쇼핑·문화",
        "lat": 37.5116,
        "lon": 127.0592,
        "description": "대형 쇼핑 공간과 독특한 서가로 유명한 별마당도서관을 즐길 수 있습니다."
    },
    {
        "name": "강남역",
        "english": "Gangnam Station",
        "category": "쇼핑·도심",
        "lat": 37.4979,
        "lon": 127.0276,
        "description": "다양한 음식점과 상점, 한국의 최신 유행을 경험할 수 있는 번화가입니다."
    },
    {
        "name": "홍대 거리",
        "english": "Hongdae Street",
        "category": "문화·공연",
        "lat": 37.5563,
        "lon": 126.9236,
        "description": "거리 공연과 음악, 예술, 개성 있는 상점들을 경험할 수 있습니다."
    },
    {
        "name": "동대문디자인플라자",
        "english": "Dongdaemun Design Plaza",
        "category": "건축·전시",
        "lat": 37.5671,
        "lon": 127.0095,
        "description": "독특한 건축물과 다양한 전시, 디자인 행사를 만날 수 있습니다."
    },
    {
        "name": "북촌한옥마을",
        "english": "Bukchon Hanok Village",
        "category": "전통·문화",
        "lat": 37.5826,
        "lon": 126.9830,
        "description": "전통 한옥이 모여 있는 골목에서 한국의 역사와 전통문화를 체험할 수 있습니다."
    },
    {
        "name": "광장시장",
        "english": "Gwangjang Market",
        "category": "전통시장·먹거리",
        "lat": 37.5700,
        "lon": 126.9997,
        "description": "빈대떡과 다양한 한국 전통 음식을 맛볼 수 있는 전통시장입니다."
    },
    {
        "name": "경복궁",
        "english": "Gyeongbokgung Palace",
        "category": "역사·문화",
        "lat": 37.5796,
        "lon": 126.9770,
        "description": "조선 왕조의 대표 궁궐로 한국의 역사와 궁궐 건축을 살펴볼 수 있습니다."
    },
    {
        "name": "서울숲",
        "english": "Seoul Forest",
        "category": "공원·휴식",
        "lat": 37.5444,
        "lon": 127.0374,
        "description": "도심 속에서 산책과 휴식, 아름다운 자연 풍경을 즐길 수 있는 공원입니다."
    }
]

# 제목
st.title("🗺️ 서울 외국인 관광 명소 TOP 10")
st.write("외국인 관광객에게 인기 있는 서울의 주요 관광지를 지도에서 확인해 보세요!")

st.markdown("---")

# 사이드바 검색
st.sidebar.header("🔍 관광지 검색")

categories = ["전체"] + sorted(
    list(set(place["category"] for place in attractions))
)

selected_category = st.sidebar.selectbox(
    "관광지 분류 선택",
    categories
)

keyword = st.sidebar.text_input(
    "관광지 이름 검색",
    placeholder="예: 명동, 경복궁"
)

# 관광지 필터링
filtered = attractions.copy()

if selected_category != "전체":
    filtered = [
        place for place in filtered
        if place["category"] == selected_category
    ]

if keyword:
    filtered = [
        place for place in filtered
        if keyword.lower() in place["name"].lower()
        or keyword.lower() in place["english"].lower()
    ]

# 화면 구성
col1, col2 = st.columns([1.6, 1])

with col1:
    st.subheader("📍 서울 관광 명소 지도")

    if filtered:
        m = folium.Map(
            location=[37.5665, 126.9780],
            zoom_start=12,
            control_scale=True
        )

        for index, place in enumerate(filtered):
            popup_html = f"""
            <div style="width:230px">
                <h3>{place['name']}</h3>
                <p><b>{place['english']}</b></p>
                <p>{place['category']}</p>
                <p>{place['description']}</p>
            </div>
            """

            folium.Marker(
                location=[place["lat"], place["lon"]],
                tooltip=place["name"],
                popup=folium.Popup(
                    popup_html,
                    max_width=280
                ),
                icon=folium.Icon(
                    color="red" if index < 5 else "blue",
                    icon="info-sign"
                )
            ).add_to(m)

        bounds = [
            [place["lat"], place["lon"]]
            for place in filtered
        ]

        m.fit_bounds(bounds, padding=(25, 25))

        st_folium(
            m,
            width=None,
            height=600,
            use_container_width=True,
            returned_objects=[]
        )

    else:
        st.warning("검색 결과가 없습니다.")

with col2:
    st.subheader("⭐ 관광지 TOP 10")

    for place in filtered:
        original_index = attractions.index(place) + 1

        st.markdown(
            f"### {original_index}. {place['name']}"
        )

        st.caption(
            f"{place['english']} | {place['category']}"
        )

        st.write(place["description"])

        st.divider()

# 하단 정보
st.markdown("---")

st.subheader("🌏 서울 여행 정보")

st.write(
    "서울에는 전통문화, 쇼핑, 음식, 예술, 자연 등 "
    "다양한 매력을 가진 관광지가 있습니다."
)

st.caption(
    "※ 본 목록은 서울시 외국인 관광객 방문 동향과 관광객 리뷰 등을 참고한 추천 목록이며, "
    "공식적인 전체 관광지 순위는 아닙니다."
)

st.markdown(
    "[서울시 관광 정보 바로가기](https://english.visitseoul.net/)"
)
