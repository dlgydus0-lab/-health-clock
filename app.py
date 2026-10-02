from datetime import datetime, timedelta
import streamlit as st

# 1. 웹 페이지 기본 설정
st.set_page_config(
    page_title="나의 인생 & 건강 시계", page_icon="⏰", layout="centered"
)

st.title("⏰ 시간대별 맞춤 건강 & 인생 시계")
st.write(
    "파이썬으로 만든 나만의 스마트 인생/건강 시계입니다. 내 정보를"
    " 입력해보세요!"
)

# 2. 사이드바 - 사용자 정보 입력 받기 (나이 및 건강 기록)
st.sidebar.header("👤 나의 기본 정보")
birth_year = st.sidebar.number_input(
    "태어난 연도 (출생년도)", min_value=1940, max_value=2020, value=2003
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

# 4. 인생 및 건강 나이 계산 로직
current_year = kst_now.year
my_age = current_year - birth_year

# 한국인 기준 통계 설정
avg_life_expectancy = 83  # 평균 기대수명 (세)
avg_healthy_age = 73  # 건강수명 (세) - 질병 없이 활동하는 나이

# 남은 연도 계산
remaining_years = max(0, avg_life_expectancy - my_age)
remaining_healthy_years = max(0, avg_healthy_age - my_age)

# 남은 인생의 총 주말 수 계산 (남은 연도 * 52주)
estimated_remaining_weekends = remaining_years * 52

# 5. 화면에 시각화 카드 표시
st.markdown(
    f"### ⏳ 나의 인생 시계 (현재 나이: 만 {my_age}세 / 기대수명"
    f" {avg_life_expectancy}세 기준)"
)

col1, col2 = st.columns(2)
with col1:
  st.metric(
      label="🏖️ 내 인생 남은 주말 (평생)",
      value=f"약 {estimated_remaining_weekends:,}주",
  )
with col2:
  st.metric(
      label="💪 건강하게 활동할 남은 기간",
      value=f"약 {remaining_healthy_years}년",
  )

if my_age >= avg_healthy_age:
  st.warning(
      "⚠️️ 현재 건강수명(73세) 단계를 지나셨습니다! 지금부터의 꾸준한 건강"
      " 관리가 더더욱 중요합니다."
  )
else:
  st.info(
      f"💡 **메시지:** 건강수명(73세)까지 앞으로 **{remaining_healthy_years}년"
      " (약 {remaining_healthy_years * 365}일)** 남았습니다. 오늘부터"
      " 시작하는 작은 운동과 물 한 잔이 건강한 노후를 만듭니다!"
  )


# 6. 시간대 판별 및 맞춤 코칭 로직
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

# 7. 건강 상태 피드백 및 미션 추천
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

# 시간대별 맞춤 조언
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
