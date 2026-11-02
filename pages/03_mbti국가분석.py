import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --------------------------------------------------
# 1. 기본 화면 설정
# --------------------------------------------------

st.set_page_config(
    page_title="세계 MBTI 탐험",
    page_icon="🌎",
    layout="wide"
)

# --------------------------------------------------
# 2. 앱 제목
# --------------------------------------------------

st.title("🌎 세계 MBTI 탐험")
st.subheader("국가별 MBTI 유형 분포를 알아보자!")
st.caption("158개 국가의 MBTI 유형별 비율을 그래프로 비교해 보세요.")

st.divider()


# --------------------------------------------------
# 3. CSV 파일 불러오기
# --------------------------------------------------

@st.cache_data
def load_data():
    file_name = "countriesMBTI_16types.csv"

    try:
        df = pd.read_csv(file_name, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(file_name, encoding="cp949")

    # 국가명 앞뒤 공백 제거
    df["Country"] = df["Country"].astype(str).str.strip()

    # 국가명을 제외한 나머지 열을 MBTI 유형으로 설정
    mbti_types = [col for col in df.columns if col != "Country"]

    # MBTI 데이터 숫자형으로 변환
    for col in mbti_types:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 결측값이 있는 행 제거
    df = df.dropna(subset=["Country"] + mbti_types)

    return df, mbti_types


try:
    df, mbti_types = load_data()

except FileNotFoundError:
    st.error(
        "CSV 파일을 찾을 수 없습니다. "
        "GitHub 저장소에 CSV 파일을 업로드했는지 확인해 주세요."
    )
    st.stop()

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# --------------------------------------------------
# 4. 국가 선택
# --------------------------------------------------

st.markdown("### 🗺️ 어떤 국가의 MBTI를 알아볼까요?")

countries = sorted(df["Country"].unique())

# 대한민국을 기본 선택 국가로 설정
default_index = (
    countries.index("South Korea")
    if "South Korea" in countries
    else 0
)

selected_country = st.selectbox(
    "국가 선택하기",
    countries,
    index=default_index
)


# --------------------------------------------------
# 5. 선택한 국가 데이터 분석
# --------------------------------------------------

country_data = df[
    df["Country"] == selected_country
].iloc[0]

# MBTI 유형별 비율을 데이터프레임으로 변환
result = pd.DataFrame({
    "MBTI": mbti_types,
    "비율": [country_data[m] * 100 for m in mbti_types]
})

# 비율이 높은 순서대로 정렬
result = result.sort_values(
    by="비율",
    ascending=False
).reset_index(drop=True)


# --------------------------------------------------
# 6. 그래프 색상 설정
# --------------------------------------------------

def make_gradient(start_color, end_color, steps):
    """두 색상 사이의 그라데이션 색상 생성"""

    start = tuple(
        int(start_color[i:i+2], 16)
        for i in (1, 3, 5)
    )

    end = tuple(
        int(end_color[i:i+2], 16)
        for i in (1, 3, 5)
    )

    colors = []

    for i in range(steps):
        ratio = i / max(steps - 1, 1)

        rgb = tuple(
            int(start[j] + (end[j] - start[j]) * ratio)
            for j in range(3)
        )

        colors.append(
            "rgb({}, {}, {})".format(*rgb)
        )

    return colors


# 1위는 빨간색
first_color = "#EF4444"

# 2위부터 16위까지 파란색 그라데이션
blue_colors = make_gradient(
    "#2563EB",
    "#DBEAFE",
    len(result) - 1
)

# 최종 색상 목록
all_colors = [first_color] + blue_colors

result["색상"] = all_colors


# --------------------------------------------------
# 7. 최고 비율 MBTI 정보
# --------------------------------------------------

top_mbti = result.iloc[0]["MBTI"]
top_rate = result.iloc[0]["비율"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🌎 선택한 국가",
        value=selected_country
    )

with col2:
    st.metric(
        label="🏆 가장 높은 MBTI",
        value=top_mbti
    )

with col3:
    st.metric(
        label="📊 최고 비율",
        value=f"{top_rate:.2f}%"
    )


st.divider()


# --------------------------------------------------
# 8. MBTI 막대그래프
# --------------------------------------------------

st.markdown(
    f"### 📊 {selected_country}의 MBTI 유형별 비율"
)

st.markdown(
    "가장 비율이 높은 유형은 **빨간색**, "
    "나머지 유형은 **파란색 그라데이션**으로 표시됩니다."
)

# 가로 막대그래프에서 높은 순위가 위쪽에 오도록 역순 배치
chart_data = result.iloc[::-1]

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=chart_data["비율"],
        y=chart_data["MBTI"],
        orientation="h",

        marker=dict(
            color=chart_data["색상"],
            line=dict(width=0)
        ),

        text=[
            f"{value:.2f}%"
            for value in chart_data["비율"]
        ],

        textposition="outside",

        hovertemplate=(
            "<b>%{y}</b><br>"
            "비율: %{x:.2f}%"
            "<extra></extra>"
        )
    )
)

fig.update_layout(
    height=650,

    xaxis=dict(
        title="비율 (%)",
        showgrid=True,
        gridcolor="#E5E7EB",
        zeroline=False
    ),

    yaxis=dict(
        title="MBTI 유형",
        categoryorder="array",
        categoryarray=chart_data["MBTI"].tolist()
    ),

    plot_bgcolor="white",
    paper_bgcolor="white",

    margin=dict(
        l=40,
        r=60,
        t=30,
        b=40
    ),

    font=dict(
        size=14
    ),

    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# 9. MBTI 순위표
# --------------------------------------------------

st.divider()

st.markdown("### 🏅 MBTI 유형별 순위")

display_data = result[["MBTI", "비율"]].copy()

display_data.insert(
    0,
    "순위",
    range(1, len(display_data) + 1)
)

display_data["비율"] = display_data["비율"].map(
    lambda x: f"{x:.2f}%"
)

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# 10. 데이터 안내
# --------------------------------------------------

st.divider()

st.info(
    "💡 이 자료는 국가별 MBTI 유형 분포를 비교하기 위한 "
    "데이터입니다. 실제 국민 전체의 성격을 확정하는 "
    "통계로 해석하지 않도록 주의하세요."
)

st.caption(
    "WORLD MBTI EXPLORER | Data Analysis with Streamlit"
)
