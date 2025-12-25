import streamlit as st
import requests

ENDPOINT = st.secrets["GAS_ENDPOINT"]

st.title("識別コード管理")

action = st.selectbox("操作", ["add", "update", "delete"])
code = st.text_input("識別コード")
url = st.text_input("URL（delete時は不要）")

if st.button("実行"):
    payload = {
        "action": action,
        "code": code,
        "url": url
    }

    r = requests.post(ENDPOINT, data=payload, timeout=10)
    
    st.write("raw:", r.text)
    
    try:
        res = r.json()
    except Exception as e:
        st.error("JSONではありません")
        st.stop()
    
    if res["status"] == "ok":
        st.success("成功")



