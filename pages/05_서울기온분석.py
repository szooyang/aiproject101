
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

# CSV 파일 경로 설정
# 현재 파이썬 파일은 pages 폴더에 있고,
# CSV 파일은 상위 폴더에 있음
current_folder = Path(__file__).resolve().parent
file_path = current_folder.parent / "temperature.csv"

# CSV 파일 읽기
if not file_path.exists():
    st.error("temperature.csv 파일을 찾을 수 없습니다.")
    st.info("CSV 파일이 pages 폴더의 상위 폴더에 있는지 확인해주세요.")
    st.stop()

try:
    df = pd.read_csv(file_path, encoding="cp949")
except UnicodeDecodeError:
    try:
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    except Exception as e:
        st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
        st.stop()
except Exception as e:
    st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
    st.stop()

# 필요한 열만 선택
required_columns = ["일시", "최고기온(℃)", "최저기온(℃)"]

if not all(col in df.columns for col in required_columns):
    st.error("CSV 파일에 필요한 열이 없습니다.")
    st.write("현재 CSV 열 이름:", df.columns.tolist())
    st.stop()

df = df[required_columns].copy()

# 월 영문 약자를 숫자로 변환
month_dict = {
    "Jan": 1, "Feb": 2, "Mar": 3,
    "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9,
    "Oct": 10, "Nov": 11, "Dec": 12
}

# 일시에서 연도와 월 추출
df["월영문"] = df["일시"].astype(str).str[:3]

df["연도"] = pd.to_numeric(
    df["일시"].astype(str).str[-2:],
    errors="coerce"
)

# 2자리 연도를 4자리 연도로 변환
df["연도"] = df["연도"].apply(
    lambda x: int(x) + 2000 if pd.notna(x) and x <= 26
    else int(x) + 1900 if pd.notna(x)
    else None
)

df["월"] = df["월영문"].map(month_dict)

# 기온 데이터 숫자 변환
df["최고기온(℃)"] = pd.to_numeric(
    df["최고기온(℃)"], errors="coerce"
)

df["최저기온(℃)"] = pd.to_numeric(
    df["최저기온(℃)"], errors="coerce"
)

# 날짜 정보가 없는 행 제거
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

# 선택한 월의 데이터 추출
month_df = df[df["월"] == selected_month].copy()

# 같은 연도에 여러 자료가 있으면 평균 계산
result = (
    month_df.groupby("연도")[
        ["최고기온(℃)", "최저기온(℃)"]
    ]
    .mean()
    .reset_index()
    .sort_values("연도")
)

# 그래프 출력
st.subheader(f"📊 {month_names[selected_month]} 월별 기온분석")

if result.empty:
    st.warning("선택한 월에 해당하는 데이터가 없습니다.")

else:
    fig = go.Figure()

    # 최고기온: 핫핑크
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

    # 최저기온: 하늘색
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

    # 그래프 표시
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # 데이터 표
    st.subheader("📋 연도별 기온 데이터")

    st.dataframe(
        result.style.format({
            "최고기온(℃)": "{:.1f}",
            "최저기온(℃)": "{:.1f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    # 기온 통계
    st.subheader("📈 선택한 월의 평균 기온")

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
