import streamlit as st
import pandas as pd
import requests
from urllib.parse import quote

st.set_page_config(layout="wide")
st.title("スプレッドシート管理")

# ----------------------------
# シークレット
# ----------------------------
SHEET_ID     = st.secrets["SHEET_ID"]
GAS_ENDPOINT = st.secrets["GAS_ENDPOINT"]

# ----------------------------
# スプレッドシート表示
# ----------------------------
st.header("スプレッドシート表示")

def load_sheet(sheet_name: str) -> pd.DataFrame:
    encoded = quote(sheet_name)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded}"
    return pd.read_csv(url)

col1, col2 = st.columns(2)
allow_placeholder = col1.empty()
log_placeholder   = col2.empty()

def show_tables():
    df_allow = load_sheet("許可リスト")
    df_log   = load_sheet("アクセス記録")
    allow_placeholder.dataframe(df_allow, width='stretch')
    log_placeholder.dataframe(df_log, width='stretch')

show_tables()

# ----------------------------
# 識別コード管理フォーム
# ----------------------------
st.header("識別コード管理フォーム")
action_map = {"追加": "add", "編集": "edit", "消去": "delete"}

with st.form("manage_code"):
    action_jp = st.selectbox("操作", ["追加", "編集", "消去"])
    code      = st.text_input("識別コード")
    url_input = st.text_input("URL (追加/編集時のみ)")

    submitted = st.form_submit_button("実行")
    if submitted:
        payload = {"action": action_map[action_jp], "code": code, "url": url_input}
        try:
            r = requests.post(GAS_ENDPOINT, data=payload, timeout=10)
            try:
                res = r.json()
                if res.get("status") == "ok":
                    st.success(f"{action_jp} 成功")
                    show_tables()
                else:
                    st.error(f"{action_jp} 失敗: {res.get('message')}")
            except:
                st.success(f"{action_jp} リクエスト送信完了")
                show_tables()
        except Exception as e:
            st.error(f"GAS通信エラー: {e}")
