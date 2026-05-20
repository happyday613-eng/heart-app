import streamlit as st
import random

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="🎰 대박 기원! 로또 번호 생성기",
    page_icon="🎰",
    layout="centered"
)

# 로또 공 모양을 예쁘게 만들기 위한 CSS 디자인 스타일 주입
st.markdown("""
    <style>
    h1 { text-align: center; color: #333333; font-size: 2rem !important; }
    .ball-container { display: flex; justify-content: center; gap: 15px; margin: 25px 0; flex-wrap: wrap; }
    .lotto-ball {
        width: 55px; height: 55px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 1.4rem; color: white;
        box-shadow: 2px 3px 5px rgba(0,0,0,0.2);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
    }
    /* 실제 로또 번호대별 공식 색상 매칭 */
    .range-yellow { background: radial-gradient(circle at 30% 30%, #fbc02d, #f57f17); color: black !important; text-shadow: none !important; }
    .range-blue   { background: radial-gradient(circle at 30% 30%, #29b6f6, #0288d1); }
    .range-red    { background: radial-gradient(circle at 30% 30%, #ef5350, #d32f2f); }
    .range-grey   { background: radial-gradient(circle at 30% 30%, #aaaaaa, #777777); }
    .range-green  { background: radial-gradient(circle at 30% 30%, #66bb6a, #388e3c); }
    
    .stButton>button { width: 100%; height: 50px; font-size: 1.2rem !important; font-weight: bold; background-color: #ff9800 !important; color: white !important; border: none; }
    .stButton>button:hover { background-color: #e65100 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🎰 인생역전! AI 로또 자동 생성기")
st.write("아래 버튼을 누르면 기운이 좋은 6개의 행운 번호가 중복 없이 즉시 추출됩니다.")
st.markdown("---")

# 2. 번호 생성 버튼 배치
if st.button("🔮 행운의 번호 자동 생성하기"):
    
    # 1부터 45까지의 숫자 중 중복 없이 6개 뽑아서 정렬 (로또 공식 룰)
    lotto_numbers = sorted(random.sample(range(1, 46), 6))
    
    # 예쁜 공 모양으로 화면에 배치하기 위한 HTML 구조 시작
    ball_html = '<div class="ball-container">'
    
    for num in lotto_numbers:
        # 번호 구역별 색상 클래스 지정
        if 1 <= num <= 10:
            color_class = "range-yellow"
        elif 11 <= num <= 20:
            color_class = "range-blue"
        elif 21 <= num <= 30:
            color_class = "range-red"
        elif 31 <= num <= 40:
            color_class = "range-grey"
        else:
            color_class = "range-green"
            
        ball_html += f'<div class="lotto-ball {color_class}">{num}</div>'
        
    ball_html += '</div>'
    
    # 화면에 로또 공 뿌리기
    st.markdown(ball_html, unsafe_allow_html=True)
    
    # 대박 기원 축하 문구 및 스트림릿 효과
    st.success(f"🎉 오늘의 추천 번호: {', '.join(map(str, lotto_numbers))} 입니다!")
    st.balloons() # 화면에 풍선이 팡 터지는 효과 추가
    
else:
    # 버튼을 누르기 전 대기 화면 상태
    st.info("💡 위의 주황색 버튼을 눌러 행운의 숫자를 확인해 보세요!")