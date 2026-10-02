from datetime import datetime, timedelta
import streamlit as st

# 1. 웹 페이지 기본 설정
st.set_page_config(
    page_title="나의 스마트 건강 시계", page_icon="⏰", layout="centered"
)

st.title("⏰ 시간대별 맞춤 건강 & 생활 습관 코치")
st.write(
    "파이썬으로 만든 나만의 스마트 건강 시계입니다. 오늘의 컨디션을 입력해보세요!"
)

# 2. 사이드바 - 사용자 정보 입력 받기
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

st.sidebar.info(
    "💡 팁: 시간이 안 맞을 땐 위에 '새로고침' 버튼을 누르면 한국 현재"
    " 시각으로 즉시 갱신돼요!"
)

# 3. 한국 표준시(KST, UTC+9) 현재 시간 정확히 가져오기
utc_now = datetime.utcnow()
kst_now = utc_now + timedelta(hours=9)
current_hour = kst_now.hour
current_time_str = kst_now.strftime("%Y-%m-%d %H:%M:%S")

st.markdown(f"**현재 한국 시각 (KST):** `{current_time_str}`")


# 4. 시간대 판별 및 맞춤 코칭 로직 (if 조건문 활용)
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

# 5. 건강 상태 피드백 및 미션 추천
st.markdown("### 🎯 지금 나에게 필요한 건강 코칭")

# 수면 피드백
if sleep_hours < 6:
  st.warning(
      "⚠️ **수면 부족 경고:** 어제 잠을 너무 적게 주셨어요. 오늘은 낮에 15분"
      " 정도 짧은 낮잠이나 휴식을 추천해요!"
  )
else:
  st.success("✨ **수면 상태 양호:** 적절한 수면 시간을 유지하고 계시네요!")

# 물 섭취 피드백
water_goal = 8  # 하루 권장 8컵
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
