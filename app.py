from datetime import datetime, timedelta
import streamlit as st

# 1. 웹 페이지 기본 설정
st.set_page_config(
    page_title="나의 인생 & 건강 시계", page_icon="⏰", layout="centered"
)

st.title("⏰ 시간대별 맞춤 건강 & 인생 시계")
st.write(
    "파이썬으로 만든 나만의 스마트 인생/건강 시계입니다. 내 출생 정보를"
    " 입력해보세요!"
)

# 2. 사이드바 - 사용자 출생 정보 및 건강 기록 입력 받기
st.sidebar.header("👤 나의 출생 정보")
birth_year = st.sidebar.number_input(
    "태어난 연도 (출생년도)", min_value=1940, max_value=2025, value=2007
)
birth_month = st.sidebar.number_input(
    "태어난 월", min_value=1, max_value=12, value=12
)
birth_day = st.sidebar.number_input(
    "태어난 일", min_value=1, max_value=31, value=14
)
birth_hour = st.sidebar.number_input(
    "태어난 시간 (시, 24시 기준)", min_value=0, max_value=23, value=12
)

st.sidebar.header("📝 오늘의 건강 기록")
sleep_hours = st.sidebar.number_input(
    "어젯밤 수면 시간 (시간)", min_value=0.0, max_value=24.0, value=7.0, step=0.5
)
water_cups = st.sidebar.slider(
    "오늘 마신 물 (컵, 1컵=250ml)", min_value=0, max_value=15, value=3
)
did_exercise = st.sidebar.checkbox("오늘 운동 완료함! 💪")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 시간 및 화면 새로고침"):
  st.rerun()

# 3. 현재 시간 가져오기 (한국 표준시 KST)
utc_now = datetime.utcnow()
kst_now = utc_now + timedelta(hours=9)
current_hour = kst_now.hour
current_time_str = kst_now.strftime("%Y-%m-%d %H:%M:%S")

st.markdown(f"**현재 한국 시각 (KST):** `{current_time_str}`")

# 4. 출생 시각 및 나이, 살아온 시간 계산
current_year = kst_now.year
birth_datetime = datetime(
    int(birth_year), int(birth_month), int(birth_day), int(birth_hour), 12
)
time_lived = kst_now - birth_datetime
days_lived = time_lived.days
hours_lived = int(time_lived.total_seconds() // 3600)

# 만 나이 정확히 계산
current_age = current_year - int(birth_year)
if (kst_now.month, kst_now.day) < (int(birth_month), int(birth_day)):
  current_age -= 1

# 5. 기대수명(83세) 기준 남은 '진짜 토요일/일요일' 일수 계산
avg_life_expectancy = 83  # 기대수명
death_target_date = datetime(
    int(birth_year) + avg_life_expectancy,
    int(birth_month),
    int(birth_day),
    int(birth_hour),
    12,
)


# 오늘부터 사망 시점까지 하루씩 넘어가며 토요일(5), 일요일(6) 카운트
def count_exact_weekend_days(start_dt, end_dt):
  weekend_days = 0
  current = start_dt
  while current <= end_dt:
    # weekday(): 월(0)~금(4), 토(5), 일(6)
    if current.weekday() in [5, 6]:
      weekend_days += 1
    current += timedelta(days=1)
  return weekend_days


# 계산 실행 (오늘부터 기대수명까지)
total_remaining_weekend_days = count_exact_weekend_days(kst_now, death_target_date)
# 주말(토,일)의 '주(Week)' 수로 보려면 총 주말 일수를 2로 나눔
total_remaining_weekend_weeks = total_remaining_weekend_days // 2

avg_healthy_age = 73
remaining_healthy_years = max(0, avg_healthy_age - current_age)

# 6. 화면에 결과 표시
st.markdown(f"### ⏳ 나의 인생 시계 (현재 만 {current_age}세)")

col_a, col_b = st.columns(2)
with col_a:
  st.metric(label="👶 내가 태어난 지", value=f"{days_lived:,}일째")
with col_b:
  st.metric(label="⏰ 살아온 시간", value=f"{hours_lived:,}시간째")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
  st.metric(
      label="🏖️ 평생 남은 진짜 주말",
      value=f"약 {total_remaining_weekend_weeks:,}주",
      delta=f"총 {total_remaining_weekend_days:,}일 (토·일)",
  )
with col2:
  st.metric(
      label="💪 건강하게 활동할 남은 기간",
      value=f"약 {remaining_healthy_years}년",
  )

st.info(
    f"💡 **인생 시계 인사이트:** 기대수명 83세까지 앞으로 맞이할 **진짜 토요일과"
    f" 일요일은 총 {total_remaining_weekend_days:,}일 (약"
    f" {total_remaining_weekend_weeks:,}주)**입니다. 소중한 주말을 알차게"
    " 보내세요!"
)


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
st.markdown("### 🎯 지금 나에게 필요한 건강 코칭")

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
      " 한 잔은 신진대사에 아주 좋습니다."
  )
elif time_zone == "오후 🌤️":
  if not did_exercise:
    st.write(
        "- 나른한 오후 시간입니다. 가벼운 산책이나 계단 오르기로 활력을"
        " 채워보세요!"
    )
  else:
    st.write(
        "- 이미 운동을 완료하셨군요! 집중력이 흐트러질 때 심호흡을 해보세요."
    )
elif time_zone == "저녁 🌙":
  st.write(
      "- 하루를 마무리할 시간입니다. 과식은 피하고 편안한 휴식을 취하세요."
  )
else:
  st.write(
      "- 🛌 수면 준비 시간입니다. 스마트폰 화면 밝기를 낮추고 숙면을 위한"
      " 환경을 만들어주세요."
  )
