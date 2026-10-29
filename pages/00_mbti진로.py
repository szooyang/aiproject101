
import streamlit as st

st.set_page_config(
    page_title="MBTI 진로 탐험소",
    page_icon="🧭",
    layout="wide"
)

# MBTI별 진로 추천 자료
# 연봉은 참고용 추정 범위이며 공식 통계의 확정값이 아님
CAREERS = {
    "ISTJ": [
        {
            "name": "회계사",
            "major": "회계학과, 경영학과, 세무회계과",
            "personality": "꼼꼼하고 책임감이 강하며 숫자와 규칙을 잘 다루는 사람",
            "salary": "약 5,000만~8,000만 원"
        },
        {
            "name": "정보보안 전문가",
            "major": "컴퓨터공학과, 정보보호학과",
            "personality": "신중하고 논리적으로 문제를 해결하는 사람",
            "salary": "약 3,500만~6,000만 원"
        }
    ],
    "ISFJ": [
        {
            "name": "간호사",
            "major": "간호학과",
            "personality": "세심하고 배려심이 깊으며 책임감이 강한 사람",
            "salary": "약 3,500만~5,000만 원"
        },
        {
            "name": "초등학교 교사",
            "major": "초등교육과",
            "personality": "인내심이 있고 다른 사람의 성장을 돕는 사람",
            "salary": "약 4,000만~7,000만 원"
        }
    ],
    "INFJ": [
        {
            "name": "상담 전문가",
            "major": "심리학과, 상담심리학과",
            "personality": "공감 능력이 뛰어나고 다른 사람을 이해하는 사람",
            "salary": "약 3,000만~5,000만 원"
        },
        {
            "name": "작가",
            "major": "국어국문학과, 문예창작학과",
            "personality": "생각이 깊고 상상력과 표현력이 풍부한 사람",
            "salary": "약 2,500만~5,000만 원"
        }
    ],
    "INTJ": [
        {
            "name": "소프트웨어 개발자",
            "major": "컴퓨터공학과, 소프트웨어학과",
            "personality": "논리적이고 독립적으로 문제를 해결하는 사람",
            "salary": "약 4,000만~7,000만 원"
        },
        {
            "name": "데이터 분석가",
            "major": "통계학과, 데이터과학과",
            "personality": "자료를 분석하고 체계적으로 정리하는 사람",
            "salary": "약 3,500만~6,000만 원"
        }
    ],
    "ISTP": [
        {
            "name": "기계 엔지니어",
            "major": "기계공학과, 자동차공학과",
            "personality": "실용적이고 기계를 다루는 일을 좋아하는 사람",
            "salary": "약 3,500만~6,000만 원"
        },
        {
            "name": "응급구조사",
            "major": "응급구조학과",
            "personality": "침착하고 상황 판단이 빠른 사람",
            "salary": "약 3,000만~4,500만 원"
        }
    ],
    "ISFP": [
        {
            "name": "시각 디자이너",
            "major": "시각디자인학과, 디자인학과",
            "personality": "감각적이고 섬세하며 표현력이 좋은 사람",
            "salary": "약 2,800만~4,500만 원"
        },
        {
            "name": "제과제빵사",
            "major": "제과제빵과, 호텔조리제과학과",
            "personality": "손재주가 좋고 새로운 모양과 맛을 만드는 사람",
            "salary": "약 2,600만~4,000만 원"
        }
    ],
    "INFP": [
        {
            "name": "웹툰 작가",
            "major": "웹툰학과, 만화애니메이션학과",
            "personality": "상상력이 풍부하고 자신만의 이야기를 만드는 사람",
            "salary": "약 2,500만~5,000만 원"
        },
        {
            "name": "콘텐츠 기획자",
            "major": "미디어학과, 광고홍보학과",
            "personality": "창의적이고 새로운 생각을 구체화하는 사람",
            "salary": "약 3,000만~5,000만 원"
        }
    ],
    "INTP": [
        {
            "name": "인공지능 연구원",
            "major": "인공지능학과, 컴퓨터공학과",
            "personality": "호기심이 많고 원리를 깊이 탐구하는 사람",
            "salary": "약 4,000만~8,000만 원"
        },
        {
            "name": "과학 연구원",
            "major": "물리학과, 화학과, 생명과학과",
            "personality": "탐구심이 강하고 실험과 분석을 즐기는 사람",
            "salary": "약 3,500만~6,000만 원"
        }
    ],
    "ESTP": [
        {
            "name": "마케팅 전문가",
            "major": "경영학과, 광고홍보학과",
            "personality": "활동적이고 순발력이 좋으며 도전을 즐기는 사람",
            "salary": "약 3,200만~5,500만 원"
        },
        {
            "name": "경찰관",
            "major": "경찰행정학과 등 관련 학과",
            "personality": "결단력이 있고 상황에 빠르게 대응하는 사람",
            "salary": "약 3,500만~6,000만 원"
        }
    ],
    "ESFP": [
        {
            "name": "방송인 및 진행자",
            "major": "방송영상학과, 미디어학과",
            "personality": "표현력이 좋고 사람들과 어울리기를 좋아하는 사람",
            "salary": "약 3,000만~6,000만 원"
        },
        {
            "name": "호텔 서비스 전문가",
            "major": "호텔경영학과, 관광학과",
            "personality": "친화력이 좋고 고객을 세심하게 배려하는 사람",
            "salary": "약 2,800만~4,500만 원"
        }
    ],
    "ENFP": [
        {
            "name": "광고 기획자",
            "major": "광고홍보학과, 미디어학과",
            "personality": "아이디어가 풍부하고 소통을 즐기는 사람",
            "salary": "약 3,200만~5,500만 원"
        },
        {
            "name": "행사 기획자",
            "major": "이벤트 관련 학과, 관광경영학과",
            "personality": "활동적이고 사람들과 협력하는 사람",
            "salary": "약 3,000만~5,000만 원"
        }
    ],
    "ENTP": [
        {
            "name": "창업가",
            "major": "경영학과, 창업 관련 학과",
            "personality": "도전을 즐기고 새로운 사업 기회를 찾는 사람",
            "salary": "수입 편차가 매우 큼"
        },
        {
            "name": "제품 기획자",
            "major": "산업공학과, 경영학과",
            "personality": "새로운 관점으로 문제를 해결하는 사람",
            "salary": "약 3,500만~6,000만 원"
        }
    ],
    "ESTJ": [
        {
            "name": "경영 관리자",
            "major": "경영학과, 경제학과",
            "personality": "계획적이고 조직을 이끌며 목표 달성을 중시하는 사람",
            "salary": "약 4,000만~7,000만 원"
        },
        {
            "name": "물류 관리자",
            "major": "물류학과, 산업공학과",
            "personality": "체계적이고 업무를 효율적으로 관리하는 사람",
            "salary": "약 3,500만~5,500만 원"
        }
    ],
    "ESFJ": [
        {
            "name": "인사 담당자",
            "major": "경영학과, 행정학과",
            "personality": "협력적이고 사람들과 원활하게 소통하는 사람",
            "salary": "약 3,200만~5,500만 원"
        },
        {
            "name": "초등학교 교사",
            "major": "초등교육과",
            "personality": "친절하고 인내심이 있으며 다른 사람을 돕는 사람",
            "salary": "약 4,000만~7,000만 원"
        }
    ],
    "ENFJ": [
        {
            "name": "교사 및 교육 기획자",
            "major": "교육학과, 사범대학 관련 학과",
            "personality": "소통을 잘하고 다른 사람의 성장을 돕는 사람",
            "salary": "약 3,500만~6,000만 원"
        },
        {
            "name": "홍보 전문가",
            "major": "광고홍보학과, 언론정보학과",
            "personality": "설득력이 있고 사람들과 관계를 잘 맺는 사람",
            "salary": "약 3,200만~5,500만 원"
        }
    ],
    "ENTJ": [
        {
            "name": "경영 컨설턴트",
            "major": "경영학과, 경제학과",
            "personality": "목표 지향적이고 전략적으로 문제를 해결하는 사람",
            "salary": "약 4,000만~8,000만 원"
        },
        {
            "name": "프로젝트 관리자",
            "major": "산업공학과, 경영학과",
            "personality": "추진력이 있고 여러 사람의 업무를 조율하는 사람",
            "salary": "약 4,000만~7,000만 원"
        }
    ]
}

TYPE_NAMES = {
    "ISTJ": "현실적인 계획가",
    "ISFJ": "따뜻한 수호자",
    "INFJ": "의미를 찾는 조언자",
    "INTJ": "전략적인 설계자",
    "ISTP": "실전형 문제 해결사",
    "ISFP": "감각적인 예술가",
    "INFP": "상상력 풍부한 이상가",
    "INTP": "호기심 많은 탐구자",
    "ESTP": "도전을 즐기는 행동가",
    "ESFP": "에너지 넘치는 분위기 메이커",
    "ENFP": "열정적인 아이디어 뱅크",
    "ENTP": "새로운 길을 찾는 발명가",
    "ESTJ": "체계적인 리더",
    "ESFJ": "사람을 챙기는 협력가",
    "ENFJ": "성장을 돕는 리더",
    "ENTJ": "목표를 향해 나아가는 지휘자"
}

# 앱 제목과 소개
st.title("🧭 MBTI 진로 탐험소")
st.subheader("내 성격에 어울리는 직업은 무엇일까? 🔎")

st.write(
    "16가지 MBTI 중 나의 유형을 선택해 봐! "
    "나에게 어울릴 수 있는 진로 2가지를 탐험해 보자. 🚀"
)

st.info(
    "💡 MBTI는 진로를 결정하는 정답지가 아니야. "
    "내가 좋아하는 활동과 잘하는 일도 함께 생각해 보자!"
)

# MBTI 선택
selected_mbti = st.selectbox(
    "🎯 나의 MBTI를 선택해 줘!",
    list(TYPE_NAMES.keys()),
    format_func=lambda x: x + " | " + TYPE_NAMES[x]
)

# 진로 추천 버튼
if st.button("✨ 나의 추천 진로 확인하기"):
    st.session_state["selected_result"] = selected_mbti

# 추천 결과 표시
if "selected_result" in st.session_state:
    result_type = st.session_state["selected_result"]

    st.divider()
    st.header(
        "🌟 " + result_type + " | " + TYPE_NAMES[result_type]
    )

    st.write(
        "아래 직업은 네 성향과 연결해 살펴볼 만한 진로야. "
        "꼭 이 직업을 선택해야 하는 건 아니야!"
    )

    careers = CAREERS[result_type]
    col1, col2 = st.columns(2)

    for i, career in enumerate(careers):
        if i == 0:
            current_col = col1
        else:
            current_col = col2

        with current_col:
            st.subheader("💼 추천 진로 " + str(i + 1))
            st.markdown("### " + career["name"])

            st.markdown("🎓 **관련 학과**")
            st.write(career["major"])

            st.markdown("💛 **이런 성향이라면 잘 맞을 수 있어!**")
            st.write(career["personality"])

            st.markdown("💰 **참고 연봉**")
            st.write(career["salary"])

    st.divider()
    st.subheader("📝 나만의 진로 탐색")
    st.write("추천받은 직업을 살펴보고 질문에 답해 봐!")

    st.text_area(
        "1. 두 직업 중 더 관심이 가는 직업과 그 이유는?",
        key="answer_interest_" + result_type
    )

    st.text_area(
        "2. 그 직업과 관련해 학교에서 해 보고 싶은 활동은?",
        key="answer_activity_" + result_type
    )

    st.text_area(
        "3. 추천 결과와 상관없이 도전하고 싶은 직업은?",
        key="answer_dream_" + result_type
    )

    st.caption(
        "※ 연봉은 참고용 추정 범위이며 공식 통계의 확정값이 아닙니다. "
        "경력, 근무처, 고용 형태 등에 따라 실제 임금은 달라집니다."
    )

    st.markdown(
        "📚 직업별 임금과 업무 내용은 "
        "[고용24](https://www.work24.go.kr/)에서 확인해 봐!"
    )

st.divider()
st.caption("🌱 나를 알아가는 과정도 진로 탐험의 중요한 시작이야!")
