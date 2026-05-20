import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="🔥 3인 매력 배틀 리그",
    page_icon="🏆",
    layout="wide" # 세 사람을 한눈에 비교하기 위해 넓은 화면 레이아웃 사용
)

# 한글 깨짐 방지 스타일 설정
st.markdown("""
    <style>
    h1 { text-align: center; color: #4A90E2; font-size: 2.2rem !important; }
    h2 { font-size: 1.5rem !important; }
    .winner-box { background-color: #FFF3CD; border-left: 5px solid #FFD700; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 정혜영 vs 유수진 vs 이성희 매력 배틀 리그")
st.write("각 인물의 역량을 실시간으로 평가하고 최고의 자리에 오를 우승자를 가려보세요!")
st.markdown("---")

# 2. 배틀 평가 항목 설정 (실무/매력 지표 5가지)
categories = ['업무 추진력', '소통 능력', '위기 관리', '친화력', '열정 지수']
N = len(categories)

# 3. 3단 가로 레이아웃으로 세 사람의 점수 입력창 배치
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👩‍💼 정혜영 능력치 심사")
    hy_1 = st.slider("정혜영 - 업무 추진력", 0, 100, 85, key="hy1")
    hy_2 = st.slider("정혜영 - 소통 능력", 0, 100, 90, key="hy2")
    hy_3 = st.slider("정혜영 - 위기 관리", 0, 100, 80, key="hy3")
    hy_4 = st.slider("정혜영 - 친화력", 0, 100, 88, key="hy4")
    hy_5 = st.slider("정혜영 - 열정 지수", 0, 100, 95, key="hy5")
    hy_scores = [hy_1, hy_2, hy_3, hy_4, hy_5]
    hy_total = sum(hy_scores)

with col2:
    st.subheader("👩‍💻 유수진 능력치 심사")
    sj_1 = st.slider("유수진 - 업무 추진력", 0, 100, 90, key="sj1")
    sj_2 = st.slider("유수진 - 소통 능력", 0, 100, 85, key="sj2")
    sj_3 = st.slider("유수진 - 위기 관리", 0, 100, 92, key="sj3")
    sj_4 = st.slider("유수진 - 친화력", 0, 100, 80, key="sj4")
    sj_5 = st.slider("유수진 - 열정 지수", 0, 100, 88, key="sj5")
    sj_scores = [sj_1, sj_2, sj_3, sj_4, sj_5]
    sj_total = sum(sj_scores)

with col3:
    st.subheader("👩‍🎨 이성희 능력치 심사")
    sh_1 = st.slider("이성희 - 업무 추진력", 0, 100, 80, key="sh1")
    sh_2 = st.slider("이성희 - 소통 능력", 0, 100, 95, key="sh2")
    sh_3 = st.slider("이성희 - 위기 관리", 0, 100, 85, key="sh3")
    sh_4 = st.slider("이성희 - 친화력", 0, 100, 92, key="sh4")
    sh_5 = st.slider("이성희 - 열정 지수", 0, 100, 90, key="sh5")
    sh_scores = [sh_1, sh_2, sh_3, sh_4, sh_5]
    sh_total = sum(sh_scores)

st.markdown("---")

# ==========================================
# [실시간 랭킹 시스템] 점수 비교 후 결과 도출
# ==========================================
st.markdown("## 📊 배틀 스코어보드 및 최종 순위")

# 데이터 구조화
results = [
    {"이름": "정혜영", "총점": hy_total, "평균": hy_total/5, "색상": "#FF6B6B"},
    {"이름": "유수진", "총점": sj_total, "평균": sj_total/5, "색상": "#4DABF7"},
    {"이름": "이성희", "총점": sh_total, "평균": sh_total/5, "색상": "#51CF66"}
]

# 총점 기준 내림차순 정렬
ranked_results = sorted(results, key=lambda x: x["총점"], reverse=True)

# 1등 우승자 브리핑 구역
winner = ranked_results[0]
st.markdown(f"""
    <div class="winner-box">
        <h3>👑 현재 배틀 리그 1위: <span style='color:{winner["색상"]}; font-size:1.6rem;'>{winner["이름"]}</span> 님</h3>
        <p>종합 총점 <b>{winner["총점"]}점</b> (평균 {winner["평균"]:.1f}점)으로 압도적인 매력을 보여주고 있습니다!</p>
    </div>
""", unsafe_allow_html=True)

# 전산 테이블 양식 출력
c_rank, c_name, c_total, c_avg = st.columns(4)
c_rank.markdown("**순위**")
c_name.markdown("**이름**")
c_total.markdown("**종합 총점**")
c_avg.markdown("**평균 능력치**")
st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

for idx, rank in enumerate(ranked_results):
    cr, cn, ct, ca = st.columns(4)
    cr.write(f"🥇 {idx+1}등" if idx==0 else f"🥈 {idx+1}등" if idx==1 else f"🥉 {idx+1}등")
    cn.markdown(f"<span style='color:{rank['색상']}; font-weight:bold;'>{rank['이름']}</span>", unsafe_allow_html=True)
    ct.write(f"{rank['총점']} 점")
    ca.write(f"{rank['평균']:.1f} 점")

st.markdown("---")

# ==========================================
# [그래프 구역] 3인 오각형 레이더 차트 그리기
# ==========================================
st.markdown("### 🕸️ 3인 능력치 밸런스 비교 그래프")

# 레이더 차트를 위한 원형 각도 계산
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1] # 다각형을 닫아주기 위해 시작점 추가

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# 그래프 영문 폰트 및 기본 라벨 세팅 (한글 버그 방지를 위해 항목 영문 병기)
labels = ['Push (추진)', 'Comm (소통)', 'Crisis (위기)', 'Friendly (친화)', 'Passion (열정)']
plt.xticks(angles[:-1], labels, color='grey', size=10)

# 1. 정혜영 데이터 레이더 그리기
hy_graph = hy_scores + hy_scores[:1]
ax.plot(angles, hy_graph, linewidth=2, linestyle='solid', label='정혜영', color='#FF6B6B')
ax.fill(angles, hy_graph, '#FF6B6B', alpha=0.1)

# 2. 유수진 데이터 레이더 그리기
sj_graph = sj_scores + sj_scores[:1]
ax.plot(angles, sj_graph, linewidth=2, linestyle='solid', label='유수진', color='#4DABF7')
ax.fill(angles, sj_graph, '#4DABF7', alpha=0.1)

# 3. 이성희 데이터 레이더 그리기
sh_graph = sh_scores + sh_scores[:1]
ax.plot(angles, sh_graph, linewidth=2, linestyle='solid', label='이성희', color='#51CF66')
ax.fill(angles, sh_graph, '#51CF66', alpha=0.1)

# 그래프 옵션 세팅
plt.ylim(0, 100)
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
fig.patch.set_alpha(0.0) # 스트림릿 테마 동기화

st.pyplot(fig)