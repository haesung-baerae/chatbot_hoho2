import streamlit as st
from openai import OpenAI
import random

# 🎈 Streamlit UI 설정
st.title("💬 오늘의 호호")
st.write(
"""
지친 마음을 살짝 어루만져 주고,  
하루에 한 번, 따뜻한 말 한마디로  
당신을 ‘호호~’ 웃게 해주는 챗봇이에요.

고민이 있을 땐 털어놓고,  
의욕이 필요할 땐 말 걸어보세요.  
언제나 곁에서 다정하게 들어줄게요.
"""
)
# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "안녕하세요, 저는 '오늘의 호호'예요 😊\n지금 마음은 어떤가요? 편하게 이야기해 주세요."
        })
    # 💬 이전 대화 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 🎲 랜덤 입력 문구
    input_prompts = [
        "마음 속 이야기를 들려줄래요?",
        "오늘 어떤 일이 있었나요?",
        "속마음, 살짝 털어놔볼까요?",
        "호호~ 하고 싶은 말이 있다면?",
        "고민이나 마음속 말을 써보세요"
    ]
    selected_prompt = random.choice(input_prompts)

    # 입력 받기
    prompt = st.chat_input(selected_prompt)

    if prompt:

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        system_prompt = """
        너는 '오늘의 호호'라는 이름의 챗봇이야.
        사람들의 고민을 따뜻하게 들어주고, 다정하고 친근한 말투로 공감과 위로를 건네주는 역할이야.
        또한, 힘이 필요한 사람에게는 부드럽게 동기부여를 해주고, 긍정적인 에너지를 전달해줘.
        너의 말투는 마치 친한 친구처럼 다정하고, 부담 없이 편안한 느낌을 줘야 해.
        딱딱하거나 차가운 말투는 절대 쓰지 말고, 조언이 필요할 땐 부드럽게 이끌어줘.
        너의 목표는 사용자가 '호호~' 웃을 수 있도록 따뜻한 말을 전해주는 거야.
        """
        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt}
            ] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
