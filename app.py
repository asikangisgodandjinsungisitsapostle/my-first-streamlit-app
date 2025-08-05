# chatbot_app.py

import streamlit as st
from openai import OpenAI
import time

# OpenAI 클라이언트 설정
client = OpenAI(
    api_key="up_iMp7NmZLtB90gnGOv2nzbgMPOXQYV",  # 실제로는 환경변수로 관리 권장
    base_url="https://api.upstage.ai/v1"
)

# Streamlit 설정
st.set_page_config(page_title="마음상담 챗봇", layout="centered")
st.title("🎓 학생 심리상담 챗봇")
st.markdown("불안하거나 고민이 있을 때, 편하게 이야기해보세요.")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "당신은 학생을 공감하고 위로하는 친절한 심리상담사입니다."}
    ]

# 채팅 기록 출력
for msg in st.session_state.messages[1:]:  # system 메시지는 표시 안 함
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
user_input = st.chat_input("지금 어떤 생각이 드시나요?")

if user_input:
    # 사용자 메시지 저장 및 출력
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 어시스턴트 영역 출력 예약
    with st.chat_message("assistant"):
        response_area = st.empty()
        full_response = ""

        # Solar Pro2 스트리밍 호출
        stream = client.chat.completions.create(
            model="solar-pro2",
            messages=st.session_state.messages,
            stream=True,
        )

        # 스트리밍 응답 처리
        for chunk in stream:
            if chunk.choices[0].delta.content:
                word = chunk.choices[0].delta.content
                full_response += word
                response_area.markdown(full_response)

        # 응답 저장
        st.session_state.messages.append({"role": "assistant", "content": full_response})
