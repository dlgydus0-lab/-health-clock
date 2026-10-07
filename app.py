import streamlit as st

# 1. 페이지 설정 (모바일 최적화 및 타이틀)
st.set_page_config(
    page_title="지하철 착석 확률 추천기",
    page_icon="🚇",
    layout="centered"
)

# 2. 지하철 감성의 커스텀 CSS 디자인 적용 (모바일 가독성 최적화)
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f8;
    }
    .stApp {
        background-color: #f4f6f8;
    }
    .subway-header {
        background: linear-gradient(135deg, #1b365d, #2c3e50);
        padding: 16px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .card {
        background-color: white;
        padding: 16px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border-left: 5px solid #0052A4; /* 2호선 블루 포인트 컬러 */
    }
    .highlight {
        color: #0052A4;
        font-weight: bold;
    }
    .seat-box {
        background-color: #ffffff;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #e1e4e8;
        font-family: monospace;
        font-size: 13px;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# 상단 헤더 배너
st.markdown("""
    <div class="subway-header">
        <h3 style="margin:0; font-size:20px;">🚇 지하철 착석 가이드</h3>
        <p style="margin: 4px 0 0 0; font-size: 13px; color: #d0d7de;">지금, 어느 칸에 타야 앉을 수 있을까?</p>
    </div>
""", unsafe_allow_html=True)

# 3. 사용자 입력 섹션 (노선 선택에 따른 역 목록 동적 변경)
col1, col2 = st.columns(2)
with col1:
    line_choice = st.selectbox("노선 선택", ["1호선", "2호선 (순환)", "3호선", "4호선"])
with col2:
    direction_choice = st.selectbox("방향 선택", ["상행 / 청량리·광운대 방면", "하행 / 신창 방면"])

# 선택한 노선에 따른 탑승역 리스트 분기
if line_choice == "1호선":
    station_list = [
        "신창역", "온양온천역", "배방역", "탕정역", 
        "아산역", "쌍용역", "봉명역", "천안역"
    ]
else:
    station_list = ["강남역", "역삼역", "선릉역", "교대역", "사당역", "서울역", "홍대입구역", "신도림역"]

station_choice = st.selectbox("현재 탑승할 역", station_list)

st.markdown("---")

# 4. 확률 및 추천 계산 로직 (과제용 예시 데이터)
def get_recommendation(station):
    # 1호선 주요 역(예: 천안역, 아산역 등)에 따른 맞춤형 시나리오
    if station in ["천안역", "아산역", "온양온천역", "강남역", "교대역", "홍대입구역", "신도림역"]:
        best_car = "4호차"
        best_pos = "출입문 바로 앞 (오른쪽 문)"
        stars = "★★★★★"
        status = "매우 높음"
        reasons = [
            "출입문 주변은 환승 및 하차 승객이 발생할 가능성이 높은 위치입니다.",
            "좌석이 비었을 때 곧바로 이동하기 편리한 통로 인근 위치입니다.",
            "승객의 이동이 비교적 많아 좌석 회전율이 높은 구역입니다."
        ]
    elif station in ["신창역", "배방역", "탕정역", "역삼역", "선릉역"]:
        best_car = "7호차"
        best_pos = "출입문 중앙"
        stars = "★★★★☆"
        status = "높음"
        reasons = [
            "주변 이용객의 하차 패턴이 뚜렷한 중간 칸 위치입니다.",
            "문과 문 사이의 좌석 비움 확률을 고려한 배치입니다."
        ]
    else:
        best_car = "3호차"
        best_pos = "교통약자석 부근 일반석"
        stars = "★★★☆☆"
        status = "보통"
        reasons = [
            "전체적인 혼잡도가 평이하며 일반적인 회전율을 보이는 구간입니다."
        ]
        
    return best_car, best_pos, stars, status, reasons

car, position, star_rating, seat_status, reason_list = get_recommendation(station_choice)

# 5. 결과 시각화 (역 이름 동적 반영 및 카드 형태)
st.markdown(f"### 🎯 **{station_choice} 착석 가이드**")

st.markdown(f"""
    <div class="card">
        <h4 style="margin-top:0; color:#1b365d; font-size:16px;">🏆 추천 탑승 위치</h4>
        <p style="margin: 8px 0;">👉 <span class="highlight">{car}</span> / <span class="highlight">{position}</span></p>
        <hr style="border:0; border-top:1px solid #eee; margin: 10px 0;">
        <p style="margin: 0;"><b>착석 가능성:</b> {star_rating} ({seat_status})</p>
    </div>
""", unsafe_allow_html=True)

# 6. 직관적인 지하철 좌석 배치 시각화
st.markdown("### 💺 지하철 칸 내부 추천 위치")
st.markdown(f"<p style='font-size:13px; color:#555;'>💡 아래 배치도에서 <span style='color:#0052A4; font-weight:bold;'>📍 [추천 위치]</span>로 표시된 자리에 서 있는 것이 유리합니다.</p>", unsafe_allow_html=True)

seat_layout_html = f"""
<div class="seat-box">
🚪 [ 출입문 (Door) ]<br>
&nbsp;&nbsp;&nbsp;&nbsp;👇<br>
<span style="color:#0052A4; font-weight:bold;">📍 [추천 위치: {position}]</span><br>
------------------------------------<br>
💺 좌석 &nbsp;&nbsp;&nbsp; 💺 좌석 &nbsp;&nbsp;&nbsp; 💺 좌석<br>
------------------------------------<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🚶 [ 통로 공간 ]<br>
------------------------------------<br>
💺 좌석 &nbsp;&nbsp;&nbsp; 💺 좌석 &nbsp;&nbsp;&nbsp; 💺 좌석<br>
------------------------------------<br>
🚪 [ 출입문 (Door) ]
</div>
"""
st.markdown(seat_layout_html, unsafe_allow_html=True)

# 7. 추천 이유 보기 (아코디언 형태 토글 기능)
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("💡 추천 이유 자세히 보기"):
    st.markdown(f"**[{station_choice} {car} 추천 근거]**")
    for idx, reason in enumerate(reason_list, 1):
        st.markdown(f"**{idx}.** {reason}")
    st.markdown("<p style='font-size: 11px; color: #888; margin-top: 8px;'>※ 본 내용은 과제 수행을 위한 현장 관찰 및 시나리오 기반 가상 데이터입니다.</p>", unsafe_allow_html=True)

# 8. 하단 안내 문구 (작은 글씨)
st.markdown("<br><hr style='border:0; border-top:1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 11px; color: #888;'>"
    "※ 착석 가능성은 승객의 이동 상황에 따라 달라질 수 있습니다."
    "</p>", 
    unsafe_allow_html=True
)
