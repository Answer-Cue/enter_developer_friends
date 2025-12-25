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



GAS_URL = "https://script.google.com/macros/s/AKfycbw5uEkTQ7mih2FRED8j1uLW8WNWqoiFBKERgdG_5EZCvLeI8OmAEa5Rm0zMAFG9n9Ey/exec"

params = {
    "mode": "update",
    "code": "ABC123",                  # A列の識別コード
    "url": "https://example.com/new"   # 書き換えたいURL
}

res = requests.get(GAS_URL, params=params)

st.write(res.status_code)
st.write(res.text)
