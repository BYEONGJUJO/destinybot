import streamlit as st
import datetime
from openai import OpenAI

# OpenAI API 키 가져오기 (Streamlit Secrets 사용)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit 설정
st.set_page_config(page_title="너 자신을 알라", page_icon="💫", layout="centered")
st.title("🔮 성향 + 운명 분석 자판기")
st.markdown("MBTI, 혈액형, 생년월일을 입력하면 성격, 연애 스타일, 직업, 재테크, 운동, 동물상, 띠, 별자리를 분석해드려요!")

# 사용자 입력
mbti = st.text_input("MBTI를 입력하세요 (예: INFJ)", max_chars=4)
blood = st.text_input("혈액형을 입력하세요 (예: A, B, AB, O)", max_chars=2)
birthdate = st.date_input("생년월일을 선택하세요", value=datetime.date(2000, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())

# 띠 계산 함수
def get_chinese_zodiac(year):
    animals = ["원숭이", "닭", "개", "돼지", "쥐", "소", "호랑이", "토끼", "용", "뱀", "말", "양"]
    return animals[year % 12]

# 별자리 계산 함수
def get_zodiac(month, day):
    zodiac_signs = [
        (120, "염소자리"), (219, "물병자리"), (321, "물고기자리"), (420, "양자리"),
        (521, "황소자리"), (621, "쌍둥이자리"), (722, "게자리"), (823, "사자자리"),
        (923, "처녀자리"), (1023, "천칭자리"), (1122, "전갈자리"), (1222, "사수자리"), (1231, "염소자리")
    ]
    date = month * 100 + day
    for zodiac_date, zodiac_name in zodiac_signs:
        if date <= zodiac_date:
            return zodiac_name
    return "염소자리"

# 분석 버튼
if st.button("🔍 분석 시작"):
    if not mbti or not blood:
        st.warning("MBTI와 혈액형을 모두 입력해 주세요.")
    else:
        with st.spinner("AI가 분석 중입니다..."):
            try:
                year = birthdate.year
                month = birthdate.month
                day = birthdate.day

                chinese_zodiac = get_chinese_zodiac(year)
                western_zodiac = get_zodiac(month, day)

                prompt = (
                    "당신은 MBTI, 혈액형, 생년월일 기반 성격 분석 전문가입니다. 아래 정보를 기반으로 아래 10가지를 한국어로 자세히 분석해 주세요:\n"
                    "1. 성격\n2. 연애 스타일\n3. 직업 추천\n4. 재테크 성향\n5. 운동 추천\n6. 어울리는 동물상\n7. 띠 (12간지)\n8. 별자리 (양력 기준)\n9. 오늘의 운세\n10. 총평\n"
                    f"MBTI: {mbti.upper()}, 혈액형: {blood.upper()}, 생년월일: {year}-{month}-{day}, 띠: {chinese_zodiac}, 별자리: {western_zodiac}"
                )

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "당신은 운명 분석 전문가입니다."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=1.0,
                    max_tokens=1024
                )

                answer = response.choices[0].message.content

                with st.container():
                    st.markdown("### 💡 분석 결과")
                    for section in answer.split("\n"):
                        if section.strip():
                            st.markdown(f"✅ {section.strip()}")

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
