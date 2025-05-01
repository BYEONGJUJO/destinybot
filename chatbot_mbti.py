import streamlit as st
from openai import OpenAI
from datetime import datetime

# Streamlit Secrets에서 API 키 불러오기
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# 페이지 설정
st.set_page_config(page_title="운명의 MBTI 챗봇", page_icon="🔮", layout="centered")
st.title("🔮 운명의 MBTI 챗봇")
st.markdown("MBTI, 혈액형, 생년월일을 입력하면 당신의 **성격, 연애 스타일, 직업, 재테크, 운동, 동물상, 띠, 별자리**까지 알려드려요!")

# 사용자 입력
mbti = st.text_input("MBTI를 입력하세요 (예: INFJ)", max_chars=4)
blood = st.text_input("혈액형을 입력하세요 (예: A, B, AB, O)", max_chars=3)
birthdate = st.date_input("생년월일을 입력하세요", format="YYYY-MM-DD")

# 띠 계산 함수
def get_zodiac(year):
    zodiacs = ['원숭이', '닭', '개', '돼지', '쥐', '소', '호랑이', '토끼', '용', '뱀', '말', '양']
    return zodiacs[year % 12]

# 별자리 계산 함수
def get_constellation(month, day):
    constellations = [
        ("염소자리", (1, 20)), ("물병자리", (2, 19)), ("물고기자리", (3, 20)),
        ("양자리", (4, 20)), ("황소자리", (5, 21)), ("쌍둥이자리", (6, 21)),
        ("게자리", (7, 23)), ("사자자리", (8, 23)), ("처녀자리", (9, 23)),
        ("천칭자리", (10, 23)), ("전갈자리", (11, 23)), ("사수자리", (12, 24)),
        ("염소자리", (12, 31))  # 끝 처리
    ]
    for name, (m, d) in constellations:
        if (month, day) <= (m, d):
            return name
    return "염소자리"

# 분석 버튼
if st.button("🔍 분석 시작"):
    if not mbti or not blood:
        st.warning("MBTI와 혈액형을 모두 입력해 주세요.")
    else:
        with st.spinner("AI가 분석 중입니다..."):

            # 띠와 별자리 계산
            year = birthdate.year
            zodiac = get_zodiac(year)
            constellation = get_constellation(birthdate.month, birthdate.day)

            prompt = (
                "당신은 MBTI, 혈액형, 띠, 별자리 기반의 성격 분석 전문가입니다.\n"
                "다음 정보를 바탕으로 아래 항목들을 한국어로 간결하게 설명해 주세요:\n"
                f"- MBTI: {mbti.upper()}\n"
                f"- 혈액형: {blood.upper()}\n"
                f"- 띠: {zodiac}\n"
                f"- 별자리: {constellation}\n\n"
                "분석 항목:\n"
                "1. 성격\n2. 연애 스타일\n3. 추천 직업\n4. 재테크 스타일\n5. 적합한 운동\n6. 동물상"
            )

            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "너는 성격 분석 전문가야."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=1.0,
                    max_tokens=1024,
                    top_p=1.0
                )

                answer = response.choices[0].message.content

                # 결과 카드 형식 출력
                st.markdown("### 🧠 분석 결과")
                for section in answer.split("\n"):
                    if section.strip():
                        st.markdown(f"#### {section.strip()}")

            except Exception as e:
                st.error(f"오류 발생: {e}")
