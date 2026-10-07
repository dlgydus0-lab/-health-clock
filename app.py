import streamlit as st
from datetime import datetime, timezone, timedelta

# 1. 페이지 설정 (모바일 최적화 및 타이틀)
st.set_page_config(
    page_title="지하철 착석 위치 추천 서비스",
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
        padding: 14px;
        border-radius: 8px;
        border: 1px solid #e1e4e8;
        font-family: monospace;
        font-size: 13px;
        line-height: 1.6;
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
    .criteria-box {
        background-color: #ffffff;
        padding: 14px;
        border-radius: 8px;
        border: 1px solid #d0d7de;
        font-size: 13px;
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
        <h3 style="margin:0; font-size:20px;">🚇 지하철 착석 위치 추천 서비스</h3>
        <p style="margin: 4px 0 0 0; font-size: 13px; color: #d0d7de;">관찰 기반 스마트 좌석 가이드</p>
    </div>
""", unsafe_allow_html=True)

# 실시간 시간 배지 출력
st.markdown(f"<div style='text-align: center;'><span class='time-badge'>🕒 조회 기준 시각: {time_display}</span></div>", unsafe_allow_html=True)

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

# 출발지와 도착지가 같을 경우 예외 처리
if boarding_station == drop_station:
    st.warning("⚠️ 탑승할 역과 내릴 역이 같습니다. 서로 다른 역을 선택해주세요.")
    st.stop()

# 정거장 수 계산 로직 (인덱스 차이 활용)
board_idx = station_list.index(boarding_station)
drop_idx = station_list.index(drop_station)
# 순환선이나 단순 리스트 거리 계산 (절댓값 또는 방향 고려)
distance = abs(drop_idx - board_idx)
if distance == 0:
    distance = 1

st.markdown("---")

# 4. 추천 및 분석 로직
def get_recommendation(boarding, drop, dist, hour):
    is_commute = (7 <= hour <= 9) or (17 <= hour <= 19)
    
    if boarding in ["천안역", "아산역", "수원역", "강남역", "신도림역", "서울역"]:
        best_car = "4호차"
        best_pos = "출입문 바로 앞 (오른쪽 문)"
        stars = "★★★★★"
        status = "매우 높음"
        expected_time = "탑승 후 약 1~2정거장 이내"
    elif boarding in ["신창역", "온양온천역", "평택역", "역삼역"]:
        best_car = "7호차"
        best_pos = "출입문 중앙"
        stars = "★★★★☆"
        status = "높음"
        expected_time = "탑승 후 약 2~3정거장 이내"
    else:
        best_car = "3호차"
        best_pos = "교통약자석 부근 일반석"
        stars = "★★★☆☆"
        status = "보통"
        expected_time = "탑승 후 약 3정거장 이상 소요 가능"

    reasons = [
        f"출입문 주변 좌석은 하차 승객이 발생할 가능성이 가장 높은 위치입니다.",
        f"통로와 인접하여 좌석이 비었을 때 곧바로 이동하기 매우 편리합니다.",
        f"선택하신 [{boarding}]역은 승객의 이동이 비교적 많은 거점 구역입니다.",
        f"총 {dist}개 정거장을 이동하는 동안 환승 및 하차 패턴에 따라 좌석 회전이 발생할 수 있습니다."
    ]
    
    if is_commute:
        reasons.append("현재 출퇴근 혼잡 시간대로 승하차 인원이 많아 자리 이동 기회가 상대적으로 자주 발생합니다.")

    return best_car, best_pos, stars, status, expected_time, reasons

car, position, star_rating, seat_status, est_time, reason_list = get_recommendation(boarding_station, drop_station, distance, current_hour)

# 5. 결과 시각화 (출발->도착 및 카드 형태)
st.markdown(f"### 🎯 **{boarding_station} ➔ {drop_station}** 착석 가이드")
st.markdown(f"<p style='font-size: 13px; color: #555; margin-top: -10px;'>이동 거리: 총 <b>{distance}개 정거장</b> 구간</p>", unsafe_allow_html=True)

st.markdown(f"""
    <div class="card">
        <h4 style="margin-top:0; color:#1b365d; font-size:16px;">🏆 추천 탑승 위치</h4>
        <p style="margin: 8px 0;">👉 <span class="highlight">{car}</span> / <span class="highlight">{position}</span></p>
        <hr style="border:0; border-top:1px solid #eee; margin: 10px 0;">
        <p style="margin: 0 0 6px 0;"><b>착석 가능성:</b> {star_rating} ({seat_status})</p>
        <p style="margin: 0; font-size: 13px; color: #444;"><b>⏱️ 예상 착석 시점 (추정):</b> {est_time}</p>
    </div>
""", unsafe_allow_html=True)

# 6. 직관적인 지하철 좌석 배치 시각화 (📍 강조)
st.markdown("### 💺 지하철 칸 내부 추천 위치")
st.markdown(f"<p style='font-size:13px; color:#555;'>💡 아래 배치도에서 빨간색 테두리와 <span style='color:#d9534f; font-weight:bold;'>📍 [추천 위치]</span>로 표시된 자리가 가장 유리합니다.</p>", unsafe_allow_html=True)

seat_layout_html = f"""
<div class="seat-box">
🚪 [ 출입문 (Door) ]<br>
&nbsp;&nbsp;&nbsp;&nbsp;👇<br>
<div style="background-color: #eef2f7; border: 2px solid #0052A4; padding: 6px; border-radius: 6px; display:inline-block;">
<span style="color:#0052A4; font-weight:bold;">📍 [추천 위치: {position}]</span>
</div><br>
------------------------------------------------<br>
💺 일반좌석 &nbsp;&nbsp;&nbsp; 💺 일반좌석 &nbsp;&nbsp;&nbsp; 💺 일반좌석<br>
------------------------------------------------<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🚶 [ 통로 공간 ]<br>
------------------------------------------------<br>
💺 일반좌석 &nbsp;&nbsp;&nbsp; 💺 일반좌석 &nbsp;&nbsp;&nbsp; 💺 일반좌석<br>
------------------------------------------------<br>
🚪 [ 출입문 (Door) ]
</div>
"""
st.markdown(seat_layout_html, unsafe_allow_html=True)

# 7. 추천 이유 자세히 보기 (아코디언 토글)
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("💡 추천 이유 자세히 보기"):
    st.markdown(f"**[{boarding_station} ➔ {drop_station} | {car} {position} 추천 상세 근거]**")
    for idx, reason in enumerate(reason_list, 1):
        st.markdown(f"**{idx}.** {reason}")
    st.markdown("<p style='font-size: 11px; color: #888; margin-top: 8px;'>※ 본 서비스는 현장 관찰 및 시나리오를 바탕으로 한 추정 모델을 사용합니다.</p>", unsafe_allow_html=True)

# 8. 착석 추천 기준 영역 (직접 관찰 내용 추가 가능)
st.markdown("### 📐 착석 추천 기준 안내")
st.markdown("""
<div class="criteria-box">
    <p style="margin:0 0 8px 0; font-weight:bold; color:#1b365d;">📌 본 서비스의 핵심 추천 기준</p>
    <ul style="margin:0; padding-left:20px; font-size:13px; color:#333; line-height:1.6;">
        <li><b>출입문 주변 좌석:</b> 승하차가 가장 빈번하게 일어나 회전율이 높은 구역</li>
        <li><b>하차 승객 패턴:</b> 주요 환승역 및 거점역 접근 시 비워지는 좌석 위치</li>
        <li><b>통로 및 이동 동선:</b> 좌석이 비었을 때 즉시 착석하기 수월한 통로 인근 위치</li>
        <li><b>현장 관찰 데이터:</b> (※ 추후 직접 관찰한 내용을 아래에 자유롭게 추가할 수 있습니다.)</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# 9. 하단 안내 문구
st.markdown("<hr style='border:0; border-top:1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 11px; color: #888;'>"
    "※ 착석 가능성 및 예상 시점은 승객의 이동 상황에 따라 달라질 수 있습니다."
    "</p>", 
    unsafe_allow_html=True
)
