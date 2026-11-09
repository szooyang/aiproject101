
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="월별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

# 제목
st.title("🌡️ 월별 기온분석")
st.write("원하는 월을 선택하면 전체 연도의 최고기온과 최저기온을 비교합니다.")

# CSV 파일 경로 찾기
file_name = "temperature(1).csv"

current_folder = Path(__file__).resolve().parent

possible_paths = [
    current_folder / file_name,
    current_folder.parent / file_name
]

file_path = None

for path in possible_paths:
    if path.exists():
        file_path = path
        break

# CSV 파일 읽기
if file_path is None:
    st.error("CSV 파일을 찾을 수 없습니다. temperature(1).csv 파일의 위치를 확인해주세요.")
    st.stop()

try:
    df = pd.read_csv(file_path, encoding="cp949")
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding="utf-8-sig")

# 필요한 열만 선택
df = df[["일시", "최고기온(℃)", "최저기온(℃)"]].copy()

# 월 영문 약자를 숫자로 변환
month_dict = {
    "Jan": 1, "Feb": 2, "Mar": 3,
    "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9,
    "Oct": 10, "Nov": 11, "Dec": 12
}

# 일시에서 연도와 월 추출
df["월영문"] = df["일시"].str[:3]
df["연도"] = pd.to_numeric(
    df["일시"].str[-2:],
    errors="coerce"
)

# 2자리 연도를 4자리 연도로 변환
df["연도"] = df["연도"].apply(
    lambda x: int(x) + 2000 if pd.notna(x) and x <= 26
    else (int(x) + 1900 if pd.notna(x) else None)
)

df["월"] = df["월영문"].map(month_dict)

# 기온 데이터 숫자 변환
df["최고기온(℃)"] = pd.to_numeric(
    df["최고기온(℃)"], errors="coerce"
)

df["최저기온(℃)"] = pd.to_numeric(
    df["최저기온(℃)"], errors="coerce"
)

# 잘못된 날짜 데이터 제거
df = df.dropna(subset=["연도", "월"])

# 월 선택
month_names = {
    1: "1월", 2: "2월", 3: "3월",
    4: "4월", 5: "5월", 6: "6월",
    7: "7월", 8: "8월", 9: "9월",
    10: "10월", 11: "11월", 12: "12월"
}

selected_month = st.selectbox(
    "📅 분석할 월을 선택하세요.",
    options=list(month_names.keys()),
    format_func=lambda x: month_names[x]
)

# 선택한 월의 데이터만 추출
month_df = df[df["월"] == selected_month].copy()

# 같은 연도와 월에 데이터가 여러 개 있으면 평균 계산
# 결측치는 각 기온 항목별로 자동 제외
result = (
    month_df.groupby("연도")[
        ["최고기온(℃)", "최저기온(℃)"]
    ]
    .mean()
    .reset_index()
    .sort_values("연도")
)

# 그래프
st.subheader(f"📊 {month_names[selected_month]} 월별 기온분석")

if result.empty:
    st.warning("선택한 월에 해당하는 데이터가 없습니다.")

else:
    fig = go.Figure()

    # 최고기온 그래프
    fig.add_trace(
        go.Scatter(
            x=result["연도"],
            y=result["최고기온(℃)"],
            mode="lines+markers",
            name="최고기온",
            line=dict(color="hotpink", width=3),
            marker=dict(size=8)
        )
    )

    # 최저기온 그래프
    fig.add_trace(
        go.Scatter(
            x=result["연도"],
            y=result["최저기온(℃)"],
            mode="lines+markers",
            name="최저기온",
            line=dict(color="skyblue", width=3),
            marker=dict(size=8)
        )
    )

    # 그래프 제목 및 축 설정
    fig.update_layout(
        title={
            "text": "월별 기온분석",
            "x": 0.5,
            "xanchor": "center"
        },
        xaxis_title="연도",
        yaxis_title="온도(℃)",
        legend_title="기온 구분",
        hovermode="x unified",
        template="plotly_white",
        height=550
    )

    # 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # 데이터 표 출력
    st.subheader("📋 분석 데이터")
    st.dataframe(
        result.rename(columns={
            "연도": "연도",
            "최고기온(℃)": "최고기온(℃)",
            "최저기온(℃)": "최저기온(℃)"
        }).style.format({
            "최고기온(℃)": "{:.1f}",
            "최저기온(℃)": "{:.1f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    # 간단한 통계
    st.subheader("📈 선택한 월의 기온 통계")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "평균 최고기온",
            f"{result['최고기온(℃)'].mean():.1f}℃"
        )

    with col2:
        st.metric(
            "평균 최저기온",
            f"{result['최저기온(℃)'].mean():.1f}℃"
        )
