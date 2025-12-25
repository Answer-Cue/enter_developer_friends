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

st.title("URL 更新")

code = st.text_input("識別コード")
url = st.text_input("URL")

if st.button("送信"):
    r = requests.post(
        st.secrets["GAS_ENDPOINT"],
        data={"code": code, "url": url},
        timeout=10
    )

    if r.status_code == 200:
        st.success("送信完了")
    else:
        st.error("失敗")
