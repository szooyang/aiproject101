
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from pathlib import Path

# --------------------------------
# 1. 페이지 설정
# --------------------------------
st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 평균기온 분석 및 미래 기온 예측")
st.write("과거 기온 데이터를 분석하고 선형회귀 알고리즘으로 미래 기온을 예측합니다.")

# --------------------------------
# 2. CSV 파일 불러오기
# --------------------------------
@st.cache_data
def load_data():
    current_dir = Path(__file__).resolve().parent

    # pages 폴더의 상위 폴더에서 CSV 찾기
    file_path = current_dir.parent / "temperature.csv"

    # 같은 폴더에 있는 경우도 확인
    if not file_path.exists():
        file_path = current_dir / "temperature.csv"

    if not file_path.exists():
        return None

    # 한글 CSV 파일 인코딩 처리
    try:
        data = pd.read_csv(file_path, encoding="cp949")
    except UnicodeDecodeError:
        data = pd.read_csv(file_path, encoding="utf-8-sig")

    # 날짜 데이터 변환
    data["날짜"] = pd.to_datetime(
        data["일시"],
        format="%b-%y",
        errors="coerce"
    )

    # 연도와 월 추출
    data["연도"] = data["날짜"].dt.year
    data["월"] = data["날짜"].dt.month

    # 평균기온 숫자 변환
    data["평균기온(℃)"] = pd.to_numeric(
        data["평균기온(℃)"],
        errors="coerce"
    )

    return data


df = load_data()

if df is None:
    st.error("temperature.csv 파일을 찾을 수 없습니다.")
    st.info("CSV 파일은 프로젝트의 최상위 폴더에 넣어주세요.")
    st.stop()

# --------------------------------
# 3. 사용자 입력
# --------------------------------
st.subheader("🔍 예측 조건 선택")

col1, col2 = st.columns(2)

month_names = {
    1: "1월", 2: "2월", 3: "3월",
    4: "4월", 5: "5월", 6: "6월",
    7: "7월", 8: "8월", 9: "9월",
    10: "10월", 11: "11월", 12: "12월"
}

with col1:
    selected_month_name = st.selectbox(
        "분석할 월을 선택하세요.",
        list(month_names.values()),
        index=9
    )

selected_month = [
    key for key, value in month_names.items()
    if value == selected_month_name
][0]

# 선택한 월의 데이터만 추출
month_data = df[
    (df["월"] == selected_month) &
    (df["평균기온(℃)"].notna()) &
    (df["연도"].notna())
].copy()

month_data = month_data.sort_values("연도")

if len(month_data) < 2:
    st.error("예측에 필요한 데이터가 부족합니다.")
    st.stop()

latest_year = int(month_data["연도"].max())

with col2:
    prediction_year = st.number_input(
        "예측할 연도를 입력하세요.",
        min_value=latest_year + 1,
        max_value=latest_year + 100,
        value=latest_year + 5,
        step=1
    )

prediction_year = int(prediction_year)

# --------------------------------
# 4. 선형회귀 모델 학습
# --------------------------------

# 입력 데이터 X: 연도
# 정답 데이터 y: 평균기온
X = month_data[["연도"]]
y = month_data["평균기온(℃)"]

# 선형회귀 알고리즘 생성
model = LinearRegression()

# 과거 데이터를 이용해 학습
model.fit(X, y)

# 사용자가 입력한 연도의 기온 예측
prediction = model.predict(
    pd.DataFrame({"연도": [prediction_year]})
)[0]

# 학습에 사용된 과거 데이터의 예측값
month_data["회귀예측기온"] = model.predict(X)

# --------------------------------
# 5. 예측 결과 표시
# --------------------------------
st.divider()
st.subheader(f"🌡️ {selected_month_name} 평균기온 예측 결과")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "예측 연도",
        f"{prediction_year}년"
    )

with col2:
    st.metric(
        "예측 평균기온",
        f"{prediction:.1f} ℃"
    )

with col3:
    st.metric(
        "분석에 사용한 데이터",
        f"{len(month_data)}개"
    )

# --------------------------------
# 6. 그래프 작성
# --------------------------------

# 실제 데이터와 예측 구간을 포함하는 회귀 직선
line_years = list(range(
    int(month_data["연도"].min()),
    prediction_year + 1
))

line_data = pd.DataFrame({
    "연도": line_years
})

line_data["회귀기온"] = model.predict(
    line_data[["연도"]]
)

fig = go.Figure()

# 실제 평균기온 데이터
fig.add_trace(go.Scatter(
    x=month_data["연도"],
    y=month_data["평균기온(℃)"],
    mode="lines+markers",
    name="실제 평균기온",
    line=dict(color="royalblue", width=2),
    marker=dict(size=7),
    hovertemplate="%{x}년<br>실제 기온: %{y:.1f}℃<extra></extra>"
))

# 선형회귀 추세선
fig.add_trace(go.Scatter(
    x=line_data["연도"],
    y=line_data["회귀기온"],
    mode="lines",
    name="선형회귀 직선",
    line=dict(color="red", width=3, dash="dash"),
    hovertemplate="%{x}년<br>회귀 기온: %{y:.1f}℃<extra></extra>"
))

# 미래 예측 지점
fig.add_trace(go.Scatter(
    x=[prediction_year],
    y=[prediction],
    mode="markers+text",
    name="미래 예측 기온",
    marker=dict(
        color="green",
        size=20,
        symbol="star"
    ),
    text=[f"{prediction:.1f}℃"],
    textposition="top center",
    textfont=dict(size=14, color="green"),
    hovertemplate="%{x}년<br>예측 기온: %{y:.1f}℃<extra></extra>"
))

fig.update_layout(
    title=f"{selected_month_name} 연도별 평균기온 및 미래 예측",
    xaxis_title="연도",
    yaxis_title="평균기온 (℃)",
    hovermode="x unified",
    template="plotly_white",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),
    height=550
)

fig.update_xaxes(
    dtick=2,
    tickformat="d"
)

fig.update_yaxes(
    ticksuffix="℃"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# 7. 선형회귀 계산 결과
# --------------------------------
st.subheader("📐 선형회귀 알고리즘의 계산 결과")

st.write(
    f"**회귀 직선의 기울기:** {model.coef_[0]:.4f}"
)

st.write(
    f"**회귀 직선의 절편:** {model.intercept_:.2f}"
)

st.latex(
    r"y = {:.4f}x + {:.2f}".format(
        model.coef_[0],
        model.intercept_
    )
)

st.info(
    f"{selected_month_name}의 과거 기온 데이터를 분석한 결과, "
    f"{prediction_year}년의 예상 평균기온은 "
    f"**{prediction:.1f}℃**입니다."
)

# --------------------------------
# 8. 선형회귀 알고리즘 설명
# --------------------------------
st.divider()

st.subheader("📚 선형회귀 알고리즘이란?")

st.markdown("""
선형회귀는 과거의 데이터들을 분석하여 가장 적합한 **직선**을 찾고,
그 직선을 이용해 미래의 값을 예측하는 알고리즘입니다.

### ① 실제 데이터를 확인합니다.
- 파란색 점은 과거에 실제로 측정한 평균기온입니다.
- 연도에 따라 평균기온이 어떻게 변화했는지 확인합니다.

### ② 가장 적합한 직선을 찾습니다.
- 빨간색 점선은 선형회귀 알고리즘이 찾은 직선입니다.
- 실제 데이터와 직선 사이의 오차가 전체적으로 작아지도록 직선을 계산합니다.
- 이때 각 데이터의 세로 방향 오차를 제곱하여 모두 더한 값이 최소가 되도록 합니다.

### ③ 직선을 연장하여 미래를 예측합니다.
- 학습한 직선의 기울기와 절편을 이용합니다.
- 사용자가 입력한 미래 연도를 직선의 식에 넣습니다.
- 초록색 별표가 바로 예측된 평균기온입니다.

### 선형회귀의 기본 공식

""")

st.latex(r"\hat{y} = b_0 + b_1x")

st.markdown("""
| 기호 | 의미 |
|---|---|
| x | 연도 |
| ŷ | 예측한 평균기온 |
| b₀ | 직선의 시작 위치를 결정하는 절편 |
| b₁ | 연도가 변할 때 기온이 변하는 정도인 기울기 |

### 💡 생각해 보기

1. 빨간색 직선은 파란색 실제 데이터와 얼마나 가까운가요?
2. 빨간색 직선이 오른쪽으로 올라간다면 기온은 어떻게 변하고 있다는 뜻일까요?
3. 예측 연도를 더 미래로 바꾸면 어떤 결과가 나타날까요?
4. 실제 기온이 매년 일정하게 변하지 않는데도 직선으로 예측하는 것이 적절할까요?

**주의:** 선형회귀는 과거의 기온 변화 추세가 미래에도 이어진다고 가정합니다. 실제 기온은 기후변화, 기상현상 등 다양한 요인에 영향을 받으므로 예측값이 실제 측정값과 다를 수 있습니다.
""")

# --------------------------------
# 9. 데이터 확인
# --------------------------------
with st.expander("📋 분석에 사용된 실제 데이터 확인하기"):
    st.dataframe(
        month_data[["연도", "평균기온(℃)"]],
        use_container_width=True,
        hide_index=True
    )
