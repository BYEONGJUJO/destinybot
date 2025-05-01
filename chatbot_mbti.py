import streamlit as st
import openai
import os
from dotenv import load_dotenv
from datetime import datetime

# .env 파일 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 띠 계산 함수
def get_zodiac(year):
    zodiacs = ['원숭이', '닭', '개', '돼지', '쥐', '소', '호랑이', '토끼', '용', '뱀', '말', '양']
    return zodiacs[year % 12]

# 별자리 계산 함수
def get_constellation(month, day):
    constellations = [
        (120, "염소자리"), (219, "물병자리"), (321, "물고기자리"), (420, "양자리"),
        (521, "황소자리"), (621, "쌍둥이자리"), (722, "게자리"), (823, "사자자리"),
        (923, "처녀자리"), (1023, "천칭자리"), (1122, "전갈자리"), (1222, "사수자리"), (1231, "염소자리")
    ]
    date = month * 100 + day
    for end_date, sign in constellations:
        if date <= end_date:
            return sign
    return "염소자리"

# 카드 스타일 마크다운 함수
def display_card(title, content):
    st.markdown(f"""
    <div style='border-radius: 12px; padding: 16px; background-color: #f9f9f9; box-shadow: 2px 2px 8px rgba(0,0,0,0.05); margin-bottom: 16px;'>
        <h4 style='color: #4A90E2;'>{title}</h4>
        <p style='font-size: 16px;'>{content}</p>
    </div>
    """, unsafe_allow_html=True)

# Streamlit 설정
st.set_page_config(page_title="MBTI + 혈액형 + 생년월일 분석 챗봇", page_icon="🧠", layout="centered")
st.title("🧬 MBTI + 혈액형 + 생년월일 분석 챗봇")
st.markdown("MBTI, 혈액형, 생년월일을 입력하면 성격, 연애 스타일, 직업, 재테크, 운동, 동물상, 띠, 별자리까지 알려드려요!")

# 사용자 입력
mbti_input = st.text_input("MBTI를 입력하세요 (예: INFJ)", max_chars=4)
blood_input = st.text_input("혈액형을 입력하세요 (예: A, B, AB, O)", max_chars=2)
birth_input = st.text_input("생년월일을 입력하세요 (예: 1995-08-17)", max_chars=10)

# 버튼 누르면 실행
if st.button("분석 시작하기"):
    if not mbti_input or not blood_input or not birth_input:
        st.warning("MBTI, 혈액형, 생년월일을 모두 입력해 주세요.")
    else:
        try:
            # 생년월일 처리
            birth_date = datetime.strptime(birth_input, "%Y-%m-%d")
            year = birth_date.year
            month = birth_date.month
            day = birth_date.day

            zodiac = get_zodiac(year)
            constellation = get_constellation(month, day)

            with st.spinner("GPT-4가 분석 중입니다... ⏳"):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": """당신은 혈액형, 성격, MBTI, 생년월일, 띠, 별자리를 분석하는 전문가입니다. 
사용자가 입력한 정보를 기반으로 다음 항목을 한국어로 항목별로 자세히 설명해 주세요 (제목을 명확히 써주세요):
- 성격 설명
- 연애 스타일
- 추천 직업
- 재테크 스타일
- 적합한 운동
- 닮은 동물상
- 띠 해석
- 별자리 성향"""
                        },
                        {
                            "role": "user",
                            "content": f"MBTI: {mbti_input.upper()}, 혈액형: {blood_input.upper()}, 생년월일: {birth_input} (띠: {zodiac}, 별자리: {constellation})"
                        }
                    ],
                    temperature=1.0,
                    max_tokens=1500,
                    top_p=1.0
                )
                full_text = response.choices[0].message.content

                # 항목별로 분리 (제목 기준으로 파싱)
                sections = full_text.split("\n")
                current_title = ""
                current_content = ""
                for line in sections:
                    if any(keyword in line for keyword in ["성격", "연애", "직업", "재테크", "운동", "동물", "띠", "별자리"]):
                        if current_title:
                            display_card(current_title, current_content.strip())
                        current_title = line.strip()
                        current_content = ""
                    else:
                        current_content += line + "\n"
                if current_title:
                    display_card(current_title, current_content.strip())

        except ValueError:
            st.error("생년월일 형식이 올바르지 않습니다. 예: 1995-08-17 형식으로 입력해 주세요.")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
