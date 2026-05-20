import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from streamlit_drawable_canvas import st_canvas

# 1. 페이지 기본 설정 및 모바일 스타일 조정
st.set_page_config(
    page_title="💖 하트 그리기 마스터",
    page_icon="💖",
    layout="centered"
)

st.markdown("""
    <style>
    h1 { font-size: 1.8rem !important; text-align: center; }
    h3 { font-size: 1.3rem !important; }
    .stButton>button { width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.title("💖 AI 하트 그리기 완벽도 테스트")
st.write("아래 회색 캔버스 안에 손가락(터치)이나 마우스로 하트를 예쁘게 따라 그려보세요. AI가 수학적 공식과 비교하여 완벽도를 측정합니다!")
st.markdown("---")

# 2. 캔버스 설정 (모바일/PC 겸용 300x300 콤팩트 크기)
canvas_size = 300

# 배경에 가이드라인으로 보여줄 실제 완벽한 하트의 위치 미리 계산
t_guide = np.linspace(0, 2 * np.pi, 100)
# 캔버스 중앙(150, 150) 반경 내에 들어오도록 스케일 조정
x_guide = 150 + 7 * (16 * np.sin(t_guide) ** 3)
y_guide = 150 - 7 * (13 * np.cos(t_guide) - 5 * np.cos(2*t_guide) - 2 * np.cos(3*t_guide) - np.cos(4*t_guide))

# 드로잉 칠판 배치
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # 채우기 없음
    stroke_width=4,                      # 붓 두께
    stroke_color="#DE1A1A",              # 하트 붉은 선
    background_color="#F0F2F6",          # 캔버스 배경색
    height=canvas_size,
    width=canvas_size,
    drawing_mode="freedraw",             # 자유 그리기 모드
    key="canvas",
)

# ==========================================
# [AI 판독 구역] 사용자가 그린 선 분석 및 수식 비교
# ==========================================
if canvas_result.json_data is not None:
    objects = canvas_result.json_data["objects"]
    
    # 사용자가 선을 그렸는지 확인
    if len(objects) > 0:
        user_x = []
        user_y = []
        
        # 캔버스 패스 데이터에서 사용자가 터치한 점들의 좌표 추출
        for obj in objects:
            if "path" in obj:
                for p in obj["path"]:
                    if p[0] in ["M", "L", "Q"]:  # 이동 및 드로잉 좌표 필터링
                        user_x.append(p[-2])
                        user_y.append(p[-1])
        
        if len(user_x) > 10:  # 최소한의 선이 그려졌을 때 판독 시작
            user_x = np.array(user_x)
            user_y = np.array(user_y)
            
            # 1. 사용자가 그린 하트의 중심점 및 크기 정규화 (크게 그리든 작게 그리든 매칭되도록)
            user_x_centered = user_x - np.mean(user_x)
            user_y_centered = user_y - np.mean(user_y)
            user_radius = np.max(np.sqrt(user_x_centered**2 + user_y_centered**2))
            
            if user_radius > 0:
                user_x_norm = user_x_centered / user_radius * 16
                user_y_norm = -user_y_centered / user_radius * 13  # 화면 좌표계 반전 보정
                
                # 2. 완벽한 수학적 하트 공식의 기준점들과 거리 비교 측정
                t_perfect = np.linspace(0, 2 * np.pi, len(user_x_norm))
                x_perfect = 16 * np.sin(t_perfect) ** 3
                y_perfect = 13 * np.cos(t_perfect) - 5 * np.cos(2*t_perfect) - 2 * np.cos(3*t_perfect) - np.cos(4*t_perfect)
                
                # 오차 제곱 평균 계산 (MSE 알고리즘 기반)
                distances = []
                for ux, uy in zip(user_x_norm, user_y_norm):
                    # 가장 가까운 완벽한 수식점과의 거리 계산
                    dist = np.min((x_perfect - ux)**2 + (y_perfect - uy)**2)
                    distances.append(dist)
                
                mean_error = np.mean(distances)
                
                # 3. 오차 값을 0 ~ 100% 점수로 정밀 환산
                per = int(max(0, min(100, 100 - (mean_error * 1.5))))
            else:
                per = 0
        else:
            per = None
    else:
        per = None
else:
    per = None

# ==========================================
# [성향 진단 구역] 실시간 터치 퍼센트별 리포트
# ==========================================
st.markdown("---")

if per is not None:
    st.subheader(f"📊 AI 판독 결과 완벽도: **{per}%**")
    
    if 0 <= per <= 35:
        st.error("### 🌪️ 0% ~ 35%: 자유분방한 혼돈의 하트")
        st.write("""
        - **그림 상태:** 기성 예술의 틀을 부수는 추상화 스타일의 터치입니다.
        - **성향 분석:** 당신은 규격화된 정형성을 거부하는 **자유로운 영혼**입니다! 
        남들의 시선이나 정해진 규칙보다는 내 직관과 영감을 신뢰하는 편입니다. 아이디어가 독창적이어서 예술가나 크리에이터 성향이 매우 강합니다.
        """)
        
    elif 36 <= per <= 65:
        st.warning("### 🧩 36% ~ 65%: 매력 만점 인간미 하트")
        st.write("""
        - **그림 상태:** 정감 가고 귀여운 굴곡이 살아있는 하트입니다.
        - **성향 분석:** 당신은 이성과 감성이 마음속에서 기분 좋게 공존하는 **매력적인 소통가**입니다. 
        약간의 빈틈을 인정할 줄 아는 유연함을 가졌으며, 주변 사람들에게 편안하고 유머러스하다는 평가를 자주 듣는 인간미 넘치는 타입입니다.
        """)
        
    elif 66 <= per <= 85:
        st.info("### ⚖️ 66% ~ 85%: 황금 비율 균형의 하트")
        st.write("""
        - **그림 상태:** 대칭과 볼륨감이 아주 훌륭한 정석적인 하트입니다.
        - **성향 분석:** 당신은 현실과 이상, 일과 삶의 균형을 아주 잘 잡는 **지혜로운 멀티플레이어**입니다. 
        계획성이 뛰어나며 무모한 모험보다는 안정적인 성장 속에서 행복을 찾아냅니다. 인간관계에서도 중간 조율사 역할을 톡톡히 해냅니다.
        """)
        
    else:
        st.success("### 💎 86% ~ 100%: 1% 무결점 완벽주의 하트")
        st.write("""
        - **그림 상태:** 자로 잰 듯 좌우 대칭이 정밀하게 일치하는 신의 터치입니다.
        - **성향 분석:** 당신은 단 1mm의 오차도 피하고 싶어 하는 **철두철미한 타협 없는 완벽주의자**입니다! 
        일 처리가 자로 잰 듯 정확하고 정돈된 상태를 좋아하여 조직이나 팀에서 엄청난 신뢰를 받는 에이스 유형입니다.
        """)
else:
    st.info("💡 캔버스에 하트를 다 그리는 순간 AI가 자동으로 퍼센트와 성향을 계산하여 이곳에 띄워줍니다.")