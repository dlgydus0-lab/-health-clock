import streamlit as st
from datetime import datetime, timezone, timedelta

# 1. 페이지 설정 (모바일 최적화 및 타이틀)
st.set_page_config(
    page_title="지하철 착석 확률 추천기",
    page_icon="🚇",
    layout="centered"
)

# 2. 지하철 감성의 커스텀 CSS 디자인 적용
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
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .card {
        background-color: white;
        padding: 16px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border-left: 5px solid #0052A4; /* 블루 포인트 컬러 */
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
    .time-badge {
        background-color: #e9ecef;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        color: #333;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 한국 표준시(KST, UTC+9) 기준으로 실시간 시간 가져오기
kst = timezone(timedelta(hours=9))
now = datetime.now(kst)
current_hour = now.hour
time_display = now.strftime("%Y년 %m월 %d일 %H:%M")

# 상단 헤더 배너
st.markdown("""
    <div class="subway-header">
        <h3 style="margin:0; font-size:20px;">🚇 지하철 착석 가이드</h3>
        <p style="margin: 4px 0 0 0; font-size: 13px; color: #d0d7de;">실시간 스마트 착석 확률 추천 서비스</p>
    </div>
""", unsafe_allow_html=True)

# 실시간 시간 배지 출력
st.markdown(f"<div style='text-align: center;'><span class='time-badge'>🕒 실시간 조회 기준: {time_display}</span></div>", unsafe_allow_html=True)

# 3. 사용자 입력 섹션 (노선, 방향, 탑승역, 하차역)
col1, col2 = st.columns(2)
with col1:
    line_choice = st.selectbox("노선 선택", ["1호선", "2호선 (순환)"])
with col2:
    direction_choice = st.selectbox("운행 방향", ["상행 (청량리·광운대 방면)", "하행 (신창 방면)"])

# 1호선 주요 거점역 리스트
if line_choice == "1호선":
    station_list = [
        "신창역", "온양온천역", "배방역", "탕정역", 
        "아산역", "쌍용역", "봉명역", "천안역", 
        "성환역", "평택역", "수원역", "구로역", "서울역"
    ]
else:
    station_list = ["강남역", "역삼역", "선릉역", "교대역", "사당역", "서울역", "홍대입구역", "신도림역"]

col_board, col_drop = st.columns(2)
with col_board:
    boarding_station = st.selectbox("탑승할 역 (출발)", station_list)
with col_drop:
    drop_station = st.selectbox("내릴 역 (도착)", station_list)

st.markdown("---")

# 4. 실시간 시간대 및 구간 연동 추천 로직
def get_recommendation(boarding, drop, hour):
    # 출퇴근 시간대 판별 (출근 07~09시, 퇴근 17~19시)
    is_commute = (7 <= hour <= 9) or (17 <= hour <= 19)
    
    if boarding in ["천안역", "아산역", "수원역", "강남역", "신도림역", "서울역"]:
        best_car = "4호차"
        best_pos = "출입문 바로 앞 (오른쪽 문)"
        stars = "★★★★★"
        status = "매우 높음"
    elif boarding in ["신창역", "온양온천역", "평택역", "역삼역"]:
        best_car = "7호차"
        best_pos = "출입문 중앙"
        stars = "★★★★☆"
        status = "높음"
    else:
        best_car = "3호차"
        best_pos = "교통약자석 부근 일반석"
        stars = "★★★☆☆"
        status = "보통"

    reasons = [
        f"선택하신 [{boarding}]역은 주요 거점역으로, 출입문 주변의 승객 회전율이 높은 구역입니다.",
        f"도착역인 [{drop}]역까지 이동하는 동안 환승 및 하차 승객이 발생할 확률이 높습니다."
    ]
    
    if is_commute:
        reasons.append("현재 '출퇴근 혼잡 시간대'에 해당하여 승하차 인원이 많으므로 자리 이동 기회가 자주 생깁니다.")
    else:
        reasons.append("현재 '일반 시간대'로 비교적 안정적인 승객 흐름을 보여주는 구간입니다.")

    return best_car, best_pos, stars, status, reasons

car, position, star_rating, seat_status, reason_list = get_recommendation(boarding_station, drop_station, current_hour)

# 5. 결과 시각화 (출발->도착 및 카드 형태)
st.markdown(f"### 🎯 **{boarding_station} ➔ {drop_station}** 착석 가이드")

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

# 7. 추천 이유 보기 (아코디언 토글)
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("💡 추천 이유 자세히 보기"):
    st.markdown(f"**[{boarding_station} 출발 ➔ {drop_station} 도착 | {car} 추천 근거]**")
    for idx, reason in enumerate(reason_list, 1):
        st.markdown(f"**{idx}.** {reason}")
    st.markdown("<p style='font-size: 11px; color: #888; margin-top: 8px;'>※ 본 서비스는 실시간 시간대와 현장 관찰 시나리오를 결합한 과제용 가상 알고리즘을 사용합니다.</p>", unsafe_allow_html=True)

# 8. 하단 안내 문구
st.markdown("<br><hr style='border:0; border-top:1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 11px; color: #888;'>"
    "※ 착석 가능성은 승객의 이동 상황에 따라 달라질 수 있습니다."
    "</p>", 
    unsafe_allow_html=True
)
