import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit 설정
st.set_page_config(page_title="MBTI + 혈액형 분석 챗봇", page_icon="🧠", layout="centered")
st.title("🧬 MBTI + 혈액형 분석 챗봇")
st.markdown("MBTI, 혈액형, 생년월일을 입력하면 당신의 성격, 연애 스타일, 직업 추천 등을 알려드립니다.")

# 사용자 입력
mbti = st.text_input("MBTI를 입력하세요 (예: INFJ)", max_chars=4)
blood = st.text_input("혈액형을 입력하세요 (예: A, B, AB, O)", max_chars=2)
birthdate = st.date_input("생년월일을 선택하세요")

# 버튼 클릭 시 분석 수행
if st.button("분석 시작하기"):
    if not mbti or not blood or not birthdate:
        st.warning("모든 정보를 입력해 주세요.")
    else:
        with st.spinner("GPT-4가 분석 중입니다..."):
            try:
                chat_response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "당신은 MBTI, 혈액형, 생년월일 분석 전문가입니다. 사용자의 정보를 바탕으로 성격, 연애 스타일, 직업, 재테크 조언, 추천 운동, 닮은 동물상, 띠와 별자리까지 자세히 설명해주세요. 한국어로 응답하세요."},
                        {"role": "user", "content": f"MBTI: {mbti}, 혈액형: {blood}, 생년월일: {birthdate}"}
                    ],
                    temperature=1.0,
                    max_tokens=1024
                )
                answer = chat_response.choices[0].message.content

                # 카드 형태 출력
                st.markdown("### 💬 분석 결과")
                with st.container():
                    st.markdown(f"""
                    <div style="background-color:#f0f2f6; padding:20px; border-radius:10px;">
                        <p style="font-size:16px;">{answer}</p>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"에러 발생: {e}")
