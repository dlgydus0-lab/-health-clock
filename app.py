from datetime import datetime, timedelta
import streamlit as st

# 1. 한국 표준시(KST, UTC+9) 현재 시간 정확히 가져오기
utc_now = datetime.utcnow()
kst_now = utc_now + timedelta(hours=9)
current_hour = kst_now.hour
current_time_str = kst_now.strftime("%Y-%m-%d %H:%M:%S")

# 2. 낮과 밤에 따른 자동 다크/라이트 모드 테마 설정 (아기자기한 파스텔톤)
# 낮(오전 6시 ~ 오후 8시): 크림 베이지 & 피치 톤 (라이트 모드)
# 밤(오후 8시 ~ 오전 6시): 포근한 다크 네이비 톤 (다크 모드)
is_night = current_hour < 6 or current_hour >= 20

if is_night:
  # 다크 모드 (밤/새벽) - 눈이 편안한 감성 스타일
  bg_color = "#1E1E2F"
  card_bg = "#2B2B40"
  text_color = "#F4F4F9"
  sub_text = "#B0B0C3"
  border_color = "#3E3E5C"
  mode_name = "다크 모드 🌙"
else:
  # 라이트 모드 (낮/아침/저녁) - 아기자기한 파스텔 크림/피치 톤
  bg_color = "#FFFBF7"
  card_bg = "#FFFFFF"
  text_color = "#2D3748"
  sub_text = "#718096"
  border_color = "#FED7D7"
  mode_name = "라이트 모드 ☀️"

# 웹 페이지 기본 설정 및 디자인 CSS 주입
st.set_page_config(
    page_title="나의 스마트 인생 & 건강 시계", page_icon="⏰", layout="centered"
)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .css-1104ytp, .css-6qob1r {{
        background-color: {card_bg};
    }}
    /* 카드 디자인 스타일 */
    .custom-card {{
        background-color: {card_bg};
        border: 2px solid {border_color};
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}
    h1, h2, h3, p, label {{
        color: {text_color} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# 헤더 타이틀
st.title("⏰ 아기자기 스마트 인생 & 건강 코치")
st.write(
    f"파이썬으로 만든 나만의 감성 시간 관리 앱입니다! (현재 테마: **{mode_name}**)"
)

# 3. 사이드바 - 사용자 정보 및 새로운 습관 루틴 입력
st.sidebar.header("👤 나의 설정 및 루틴")

# 출생 정보 (기본값: 2007년 12월 14일 12시 12분)
with st.sidebar.expander("👶 출생 정보 수정", expanded=False):
  birth_year = st.number_input(
      "태어난 연도", min_value=1940, max_value=2025, value=2007
  )
  birth_month = st.number_input("태어난 월", min_value=1, max_value=12, value=12)
  birth_day = st.number_input("태어난 일", min_value=1, max_value=31, value=14)
  birth_hour = st.sidebar.number_input(
      "태어난 시간 (시)", min_value=0, max_value=23, value=12
  )

st.sidebar.markdown("---")
st.sidebar.header("🎯 오늘의 생활 루틴")
# [신규] 아침 영양제 체크
took_supplements = st.sidebar.checkbox("💊 아침 영양제 챙겨먹기 완료!")
# [신규] 공부 시간 입력 (목표: 90분 이상)
study_minutes = st.sidebar.slider(
    "📚 오늘 공부한 시간 (분)", min_value=0, max_value=300, value=60, step=10
)

st.sidebar.markdown("---")
st.sidebar.header("💧 건강 기록")
sleep_hours = st.sidebar.number_input(
    "어젯밤 수면 시간 (시간)", min_value=0.0, max_value=24.0, value=7.0, step=0.5
)
water_cups = st.sidebar.slider(
    "오늘 마신 물 (컵, 1컵=250ml)", min_value=0, max_value=15, value=3
)
did_exercise = st.sidebar.checkbox("💪 오늘 운동 완료함!")

if st.sidebar.button("🔄 시간 및 화면 새로고침"):
  st.rerun()

st.markdown(f"**현재 한국 시각 (KST):** `{current_time_str}`")
st.markdown("---")

# 4. 나이, 살아온 시간, 남은 주말 계산 로직
current_year = kst_now.year
birth_datetime = datetime(
    int(birth_year), int(birth_month), int(birth_day), int(birth_hour), 12
)
time_lived = kst_now - birth_datetime
days_lived = time_lived.days
hours_lived = int(time_lived.total_seconds() // 3600)

current_age = current_year - int(birth_year)
if (kst_now.month, kst_now.day) < (int(birth_month), int(birth_day)):
  current_age -= 1

# 기대수명 83세 기준 진짜 주말 계산
avg_life_expectancy = 83
death_target_date = datetime(
    int(birth_year) + avg_life_expectancy,
    int(birth_month),
    int(birth_day),
    int(birth_hour),
    12,
)


def count_exact_weekend_days(start_dt, end_dt):
  weekend_days = 0
  current = start_dt
  while current <= end_dt:
    if current.weekday() in [5, 6]:
      weekend_days += 1
    current += timedelta(days=1)
  return weekend_days


total_remaining_weekend_days = count_exact_weekend_days(kst_now, death_target_date)
total_remaining_weekend_weeks = total_remaining_weekend_days // 2
avg_healthy_age = 73
remaining_healthy_years = max(0, avg_healthy_age - current_age)

# 5. [파스텔톤 카드 UI 1] 인생 & 시간 시계
st.markdown(
    f"""
    <div class="custom-card">
        <h3>⏳ 나의 인생 시계 (만 {current_age}세)</h3>
        <p>👶 내가 태어난 지 <b>{days_lived:,}일째</b> ({hours_lived:,}시간째 살아가는 중)</p>
        <hr style="border: 0.5px solid {border_color};">
        <p>🏖️ 기대수명 83세까지 남은 진짜 주말: <b>약 {total_remaining_weekend_weeks:,}주</b> (총 {total_remaining_weekend_days:,}일의 토·일)</p>
        <p>💪 건강수명(73세)까지 남은 기간: <b>약 {remaining_healthy_years}년</b></p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 6. [파스텔톤 카드 UI 2] 오늘의 루틴 체크 (공부 & 영양제)
st.markdown("### 📋 오늘의 습관 & 루틴 체크")
col_r1, col_r2 = st.columns(2)

with col_r1:
  if took_supplements:
    st.success("💊 **아침 영양제:** 섭취 완료! 훌륭해요 ✨")
  else:
    st.warning("💊 **아침 영양제:** 아직 안 드셨다면 지금 챙겨드세요!")

with col_r2:
  study_goal = 90  # 1시간 30분 = 90분
  if study_minutes >= study_goal:
    st.success(
        f"📚 **공부 목표:** {study_minutes}분 달성! (목표 90분 돌파 🎓)"
    )
  else:
    st.info(
        f"📚 **공부 목표:** 현재 {study_minutes}분 / 목표 90분 (조금만 더"
        " 화이팅!)"
    )

st.markdown("---")


# 7. 시간대 판별 및 맞춤 코칭 로직
def get_time_zone(hour):
  if 6 <= hour < 12:
    return "아침 ☀️"
  elif 12 <= hour < 17:
    return "오후 🌤️"
  elif 17 <= hour < 21:
    return "저녁 🌙"
  else:
    return "밤/새벽 🌌"


time_zone = get_time_zone(current_hour)
st.subheader(f"지금은 하루 중 **{time_zone}**입니다.")

# 8. 건강 상태 피드백 및 미션 추천
st.markdown("### 🎯 맞춤형 건강 코칭")

if sleep_hours < 6:
  st.warning(
      "⚠️ **수면 부족 경고:** 어제 잠을 너무 적게 주셨어요. 오늘은 낮에 15분"
      " 정도 짧은 낮잠이나 휴식을 추천해요!"
  )
else:
  st.success("✨ **수면 상태 양호:** 적절한 수면 시간을 유지하고 계시네요!")

water_goal = 8
water_progress = min(water_cups / water_goal, 1.0)
st.write(
    f"💧 **물 섭취량:** 목표 8컵 중 현재 **{water_cups}컵** 드셨습니다."
)
st.progress(water_progress)

if water_cups < 4:
  st.info(
      "👉 **추천 행동:** 목이 마르지 않더라도 지금 책상 위에 물 한 잔을 떠다"
      "두고 조금씩 마셔보세요."
  )
elif water_cups < 8:
  st.info(
      "👉 **추천 행동:** 아주 잘하고 있어요! 조금만 더 마시면 하루 목표를"
      " 달성할 수 있습니다."
  )
else:
  st.success("🎉 **목표 달성:** 오늘 충분한 수분을 섭취하셨습니다!")

# 시간대별 맞춤 가이드
st.markdown("### 🧭 시간대별 맞춤 생활 가이드")
if time_zone == "아침 ☀️":
  st.write(
      "- 가벼운 기지개와 스트레칭으로 하루를 시작하세요.\n- 아침 공복에 물"
      " 한 잔과 영양제 섭취는 하루 활력을 책임집니다!"
  )
elif time_zone == "오후 🌤️":
  if not did_exercise:
    st.write(
        "- 나른한 오후 시간입니다. 공부 중간중간 스트레칭이나 산책을"
        " 곁들여보세요!"
    )
  else:
    st.write(
        "- 이미 운동을 완료하셨군요! 집중력이 흐트러질 때 심호흡을 해보세요."
    )
elif time_zone == "저녁 🌙":
  st.write(
      "- 하루를 마무리할 시간입니다. 오늘 세운 공부 목표를 점검하고 편안한"
      " 휴식을 취하세요."
  )
else:
  st.write(
      "- 🛌 수면 준비 시간입니다. 스마트폰 화면 밝기를 낮추고 숙면을 위한"
      " 환경을 만들어주세요."
  )
