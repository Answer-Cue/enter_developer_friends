import streamlit as st
import pandas as pd
from urllib.parse import quote
st.set_page_config(page_title="My App", layout="wide")

st.title("メインWebアプリ")
st.write("これは app.py がメインです")

name = st.text_input("名前を入力")
if name:
    st.success(f"こんにちは、{name} さん")


SHEET_ID = "17gBzDn7B6eIsNm6gY21dYg6a9_-TSIC3NWuZ06rzWAY"
SHEET_NAME = "アクセス記録"  # ← 日本語OK

encoded_sheet_name = quote(SHEET_NAME)

url = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq"
    f"?tqx=out:csv&sheet={encoded_sheet_name}"
)

df = pd.read_csv(url)
st.dataframe(df)







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
    
    st.write("status:", r.status_code)
    st.write("text:", r.text)

    res = r.json()

    if res["status"] == "ok":
        st.success(f"{res['action']} 完了")
    else:
        st.error(res["message"])

