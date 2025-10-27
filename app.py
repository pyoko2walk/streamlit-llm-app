import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

load_dotenv()

st.set_page_config(page_title="専門家に聞いてみよう", layout="wide")

st.title("専門家に聞いてみよう")
st.write("""
このアプリでは、あなたの質問に対して選択した専門家の立場からAIが回答します。  
以下の手順で使ってください：
1. 専門家の種類を選択します  
2. 質問を入力して「送信」ボタンを押します  
3. 回答が下に表示されます
""")

expert_type = st.radio(
    "専門家の種類を選んでください：",
    ("心理学者", "経済学者", "料理研究家")
)

user_input = st.text_area("質問を入力してください：", height=150)

def get_llm_response(expert: str, question: str) -> str:
    """選択した専門家の視点から質問に回答する"""
    system_messages = {
        "心理学者": "あなたは優秀な心理学者です。感情や行動の心理的背景を丁寧に説明してください。専門外の質問に対しては他の専門家に聞くよう促してください。",
        "経済学者": "あなたは一流の経済学者です。経済理論や市場の観点から論理的に説明してください。専門外の質問に対しては他の専門家に聞くよう促してください。",
        "料理研究家": "あなたは人気の料理研究家です。家庭でも実践できるコツを交えながら回答してください。専門外の質問に対しては他の専門家に聞くよう促してください。"
    }

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

    messages = [
        SystemMessage(content=system_messages[expert]),
        HumanMessage(content=question)
    ]

    result = llm(messages)
    return result.content

if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("AIが考えています..."):
            answer = get_llm_response(expert_type, user_input)
        st.success("回答が生成されました：")
        st.write(answer)

# 以下はメモ書きです
# cd streamlit-llm-app
# env\scripts\activate.bat
# pip freeze > requirements.txt
# streamlit run app.py (python app.py ではない)