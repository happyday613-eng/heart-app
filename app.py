import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from streamlit_drawable_canvas import st_canvas

# 1. 페이지 기본 설정 및 모바일 스타일 조정
st.set_page_config(
    page_title="💖 AI 하트 연애 조율소",
    page_icon="💖",
    layout="centered"
)

st.markdown("""
    <style>
    h1 { font-size: 1.8rem !important; text-align: center; }
    h3 { font-size: 1.3rem !important; }
    .stButton>button { width: 100%; height: 45px; font-weight: bold; font-size: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("💖 AI 하트 그리기 & 연애 능력 테스트")
st.write("아래 회색 캔버스 안에 손가락(터치)이나 마우스로 하트를 예쁘게 그려보세요. AI가 완벽도를 분석하여 당신의 **'진짜 연애 능력치'**를 감정합니다!")
st.markdown("---")

# 2. 상단 제어 구역 (다시 그리기 버튼 배치)
col_btn1, col_btn2 = st.columns([3, 1])
with col_btn2:
    # 다시 그리기 버튼을 누르면 세션을 리셋하여 캔버스를 깨끗하게 비웁니다.
    if st.button("🔄 다시 그리기", type="secondary"):
        st.rerun()

with col_btn1:
    st.caption("✨ 선을 다 그리고 나면 아래로 스크롤하여 AI 분석 리포트를 확인하세요.")

# 3. 캔버스 설정
canvas_size = 300
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.0)",  # 투명 채우기
    stroke_width=5,                      # 스마트폰 터치용 도톰한 붓 두께
    stroke_color="#DE1A1A",              # 하트 붉은 선
    background_color="#F0F2F6",          # 캔버스 배경색
    height=canvas_size,
    width=canvas_size,
    drawing_mode="freedraw",
    key="canvas_heart_final",
)

# ==========================================
# [AI 판독 구역] 사용자가 그린 선 데이터 연산
# ==========================================
per = None
if canvas_result.json_data is not None:
    objects = canvas_result.json_data["objects"]
    if len(objects) > 0:
        user_x, user_y = [], []
        for obj in objects:
            if "path" in obj:
                for p in obj["path"]:
                    if p[0] in ["M", "L", "Q"]:
                        user_x.append(p[-2])
                        user_y.append(p[-1])
        
        if len(user_x) > 10:
            user_x = np.array(user_x)
            user_y = np.array(user_y)
            
            user_x_centered = user_x - np.mean(user_x)
            user_y_centered = user_y - np.mean(user_y)
            user_radius = np.max(np.sqrt(user_x_centered**2 + user_y_centered**2))
            
            if user_radius > 0:
                user_x_norm = user_x_centered / user_radius * 16
                user_y_norm = -user_y_centered / user_radius * 13
                
                t_perfect = np.linspace(0, 2 * np.pi, len(user_x_norm))
                x_perfect = 16 * np.sin(t_perfect) ** 3
                y_perfect = 13 * np.cos(t_perfect) - 5 * np.cos(2*t_perfect) - 2 * np.cos(3*t_perfect) - np.cos(4*t_perfect)
                
                distances = []
                for ux, uy in zip(user_x_norm, user_y_norm):
                    dist = np.min((x_perfect - ux)**2 + (y_perfect - uy)**2)
                    distances.append(dist)
                
                mean_error = np.mean(distances)
                per = int(max(0, min(100, 100 - (mean_error * 1.5))))

st.markdown("---")

# ==========================================
# [연애 종합 판정 구역] 퍼센트별 연애 능력치 매칭
# ==========================================
if per is not None:
    st.subheader(f"📊 AI 하트 분석 결과 (완벽도: {per}%)")
    
    if 0 <= per <= 35:
        st.error("### 🌪️ [연애 등급: F] 자유분방한 나홀로 경주마형")
        st.markdown("""
        * **연애 능력치 지수:** 🧪 20 / 100 점
        * **하트 매칭 결과:** 형태를 가늠하기 힘든 파격적이고 우발적인 하트입니다.
        * **종합 연애 분석:** 당신은 연애할 때 상대방의 규칙이나 밀당에 얽매이는 것을 극도로 싫어하는 **독고다이 스타일**입니다! 내가 꽂히면 불꽃처럼 직진하지만, 내 개인 시간과 영역을 침범당하면 금방 식어버릴 수 있습니다.
        * **연애 처방전:** 가끔은 상대방의 페이스에 맞춰주는 '정속 주행' 연애 연습이 필요합니다. 연락을 조금만 더 자주 해주세요!
        """)
        
    elif 36 <= per <= 65:
        st.warning("### 🧩 [연애 등급: C] 인간미 넘치는 감성파 밀당 밀크티형")
        st.markdown("""
        * **연애 능력치 지수:** 🧪 55 / 100 점
        * **하트 매칭 결과:** 울퉁불퉁하지만 인간미와 정감이 가득 느껴지는 하트입니다.
        * **종합 연애 분석:** 당신은 연애할 때 머리로 계산하기보다는 **마음이 이끄는 대로 움직이는 감정파**입니다! 가끔 서툴러서 삐걱거리거나 츤데레처럼 굴 때도 있지만, 그 모습 자체가 상대방에게 엄청난 인간적인 매력과 귀여움으로 다가갑니다.
        * **연애 처방전:** 서운한 점이 생겼을 때 혼자 속으로 삭히다가 뿜어내지 말고, 완만하게 말로 표현하는 대화 스킬을 더하면 점수가 80점까지 수직 상승합니다!
        """)
        
    elif 66 <= per <= 85:
        st.info("### ⚖️ [연애 등급: A] 황금 비율의 연애 마스터 밸런서형")
        st.markdown("""
        * **연애 능력치 지수:** 🧪 85 / 100 점
        * **하트 매칭 결과:** 좌우 대칭이 아주 보기 좋고 균형 잡힌 정석적인 하트입니다.
        * **종합 연애 분석:** 당신은 **연애를 가장 건강하고 똑부러지게 잘하는 최고의 연애가**입니다! 밀고 당기기의 타이밍을 본능적으로 알고 있으며, 내 삶과 연애의 균형을 완벽하게 맞출 줄 압니다. 상대방을 편안하게 해주면서도 설렘을 유지하는 능력이 탁월합니다.
        * **연애 처방전:** 이미 완벽합니다! 지금처럼 서로를 존중하는 다정한 연애를 유지하시면 평생 행복한 사랑을 이어갈 수 있습니다.
        """)
        
    else:
        st.success("### 💎 [연애 등급: SSS] 무결점 1% 완벽주의 로맨티스트 대주주형")
        st.markdown("""
        * **연애 능력치 지수:** 🧪 99 / 100 점
        * **하트 매칭 결과:** 오차 1mm도 허용하지 않는 수학적 신의 대칭 하트입니다.
        * **종합 연애 분석:** 당신은 연애에 있어서 **내 사람에게 모든 최고의 것을 서포트하려는 완벽주의 로맨티스트**입니다! 기념일을 칼같이 챙기는 것은 물론, 상대방의 동선과 취향까지 정밀하게 배려하는 완벽한 설계를 보여줍니다.
        * **연애 처방전:** 가끔은 내 계획대로 연애 데이트가 흘러가지 않거나 상대방이 빈틈을 보여도, '그럴 수 있지' 하고 웃어넘기는 유연함 한 스푼만 추가해 보세요!
        """)
else:
    st.info("💡 캔버스에 하트를 다 그리는 순간 AI가 자동으로 연애 능력치를 판독하여 이곳에 종합 보고서를 세이브합니다.")