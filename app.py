import streamlit as st

st.set_page_config(page_title="My App", layout="wide")

st.title("メインWebアプリ")
st.write("これは app.py がメインです")

name = st.text_input("名前を入力")
if name:
    st.success(f"こんにちは、{name} さん")

