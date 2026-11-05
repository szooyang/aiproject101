
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import re

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="서울시 연령별 인구 분석",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 2. 제목 및 안내
# ==========================================
st.title("📊 서울시 연령별 인구 분석")
st.markdown(
    "행정구역, 성별, 연도를 선택하여 "
    "연령별 인구 분포를 확인해 보세요."
)

# ==========================================
# 3. CSV 파일 불러오기
# ==========================================
@st.cache_data
def load_data():

    # 현재 파일의 위치를 기준으로 상위 폴더의 CSV 파일 찾기
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "..", "population.csv")

    # 한글 인코딩 처리
    df = pd.read_csv(
        csv_path,
        encoding="cp949"
    )

    # 데이터 열 이름 앞뒤 공백 제거
    df.columns = df.columns.str.strip()

    # 행정구역 이름 정리
    df["행정구역"] = (
        df["행정구역"]
        .astype(str)
        .str.replace(r"\s*\(\d+\)", "", regex=True)
        .str.strip()
    )

    # 서울특별시 접두어 제거
    df["행정구역"] = df["행정구역"].str.replace(
        "서울특별시 ",
        "",
        regex=False
    )

    # 인구 데이터의 쉼표 제거 및 숫자 변환
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False),
            errors="coerce"
        )

    return df


# 데이터 불러오기
try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "population.csv 파일을 찾을 수 없습니다. "
        "CSV 파일이 프로젝트의 상위 폴더에 있는지 확인해 주세요."
    )
    st.stop()

except UnicodeDecodeError:
    st.error(
        "CSV 파일의 인코딩을 읽을 수 없습니다. "
        "파일의 인코딩을 확인해 주세요."
    )
    st.stop()

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# ==========================================
# 4. 선택 메뉴 만들기
# ==========================================

# 행정구역 목록
districts = sorted(df["행정구역"].unique().tolist())

# 연도 목록
years = list(range(2020, 2026))

# 성별 목록
genders = ["전체", "남자", "여자"]

# 화면에 선택 메뉴 배치
col1, col2, col3 = st.columns(3)

with col1:
    selected_district = st.selectbox(
        "📍 행정구역 선택",
        districts
    )

with col2:
    selected_gender = st.selectbox(
        "👥 성별 선택",
        genders
    )

with col3:
    selected_year = st.selectbox(
        "📅 연도 선택",
        years,
        index=len(years) - 1,
        format_func=lambda x: f"{x}년"
    )


# ==========================================
# 5. 연령별 인구 데이터 추출
# ==========================================

# 성별에 따른 열 이름 구분
if selected_gender == "전체":
    gender_prefix = "거주자"

elif selected_gender == "남자":
    gender_prefix = "남_거주자"

else:
    gender_prefix = "여_거주자"


# 선택한 행정구역 데이터 찾기
selected_data = df[
    df["행정구역"] == selected_district
]

if selected_data.empty:
    st.error("선택한 행정구역의 데이터를 찾을 수 없습니다.")
    st.stop()


# 연령 구간 목록
age_groups = [
    "0~9세",
    "10~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~69세",
    "70~79세",
    "80~89세",
    "90~99세",
    "100세 이상"
]


# 연령별 인구수 추출
population_values = []

for age in age_groups:

    column_name = (
        f"{selected_year}년_"
        f"{gender_prefix}_"
        f"{age}"
    )

    if column_name in df.columns:

        population = selected_data[column_name].iloc[0]

        if pd.isna(population):
            population = 0

        population_values.append(int(population))

    else:
        st.error(
            f"데이터 열을 찾을 수 없습니다: {column_name}"
        )
        st.stop()


# ==========================================
# 6. 인구 데이터 표로 정리
# ==========================================

chart_df = pd.DataFrame({
    "연령": age_groups,
    "인구수": population_values
})


# ==========================================
# 7. 주요 정보 표시
# ==========================================

total_population = sum(population_values)

metric1, metric2 = st.columns(2)

with metric1:
    st.metric(
        label="선택한 조건",
        value=f"{selected_district} · {selected_gender}",
        help=f"{selected_year}년 기준"
    )

with metric2:
    st.metric(
        label="연령별 인구 합계",
        value=f"{total_population:,}명"
    )


# ==========================================
# 8. 꺾은선 그래프 만들기
# ==========================================

st.subheader(
    f"📈 {selected_year}년 "
    f"{selected_district} 연령별 인구"
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=chart_df["연령"],
        y=chart_df["인구수"],

        mode="lines+markers",

        name="인구수",

        line=dict(
            color="#FF1493",
            width=3
        ),

        marker=dict(
            color="#FF1493",
            size=8
        ),

        hovertemplate=(
            "연령: %{x}<br>"
            "인구수: %{y:,}명"
            "<extra></extra>"
        )
    )
)


# ==========================================
# 9. 그래프 디자인 설정
# ==========================================

fig.update_layout(

    # 그래프 크기
    height=600,

    # 배경
    plot_bgcolor="white",
    paper_bgcolor="white",

    # 제목 및 축 제목
    title=dict(
        text=(
            f"{selected_district} "
            f"{selected_gender} 인구 분포"
        ),
        x=0.5,
        xanchor="center"
    ),

    xaxis=dict(
        title="나이",

        # 연령 구간을 순서대로 표시
        categoryorder="array",
        categoryarray=age_groups,

        # 가로축 구분선
        showgrid=True,
        gridcolor="#E5E5E5",
        gridwidth=1,

        # 연령 구간마다 눈금 표시
        tickmode="array",
        tickvals=age_groups,
        ticktext=age_groups,

        # 축선
        showline=True,
        linecolor="#999999"
    ),

    yaxis=dict(
        title="인구수 (명)",

        # 세로축 10만 명 단위
        dtick=100000,

        # 0부터 시작
        rangemode="tozero",

        # 세로축 구분선
        showgrid=True,
        gridcolor="#E5E5E5",
        gridwidth=1,

        # 축선
        showline=True,
        linecolor="#999999",

        # 숫자 표시
        tickformat=","
    ),

    # 그래프 여백
    margin=dict(
        l=80,
        r=30,
        t=80,
        b=100
    ),

    # 범례
    showlegend=False
)


# 그래프 출력
st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================================
# 10. 데이터 표 표시
# ==========================================

with st.expander("📋 연령별 인구 데이터 확인"):

    display_df = chart_df.copy()

    display_df["인구수"] = display_df["인구수"].apply(
        lambda x: f"{x:,}명"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# 11. 데이터 다운로드
# ==========================================

csv_download = chart_df.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    label="📥 연령별 인구 데이터 다운로드",
    data=csv_download,
    file_name=(
        f"{selected_district}_"
        f"{selected_gender}_"
        f"{selected_year}_인구.csv"
    ),
    mime="text/csv"
)


# ==========================================
# 12. 하단 안내
# ==========================================

st.divider()

st.caption(
    "📌 자료: 서울시 연령별 인구 통계 "
    "| 원본 CSV 파일을 기반으로 작성"
)

st.caption(
    "※ 100세 이상은 하나의 연령 구간으로 표시됩니다."
)
