import streamlit as st
import pandas as pd
from urllib.parse import quote
import requests

# ----------------------------
# シークレットから取得
# ----------------------------
SHEET_ID      = st.secrets["SHEET_ID"]
GAS_ENDPOINT  = st.secrets["GAS_ENDPOINT"]

# ----------------------------
# シート読み込み関数
# ----------------------------
def load_sheet(sheet_name: str) -> pd.DataFrame:
    encoded = quote(sheet_name)
    url = (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq"
        f"?tqx=out:csv&sheet={encoded}"
    )
    return pd.read_csv(url)

# ----------------------------
# 上段：シート内容表示
# ----------------------------
st.title("スプレッドシート管理")

tab1, tab2 = st.tabs(["許可リスト", "アクセス記録"])

with tab1:
    df_allow = load_sheet("許可リスト")
    st.dataframe(df_allow, width='stretch')  # 新仕様に変更

with tab2:
    df_log = load_sheet("アクセス記録")
    st.dataframe(df_log, width='stretch')    # 新仕様に変更

# ----------------------------
# 下段：識別コード管理フォーム
# ----------------------------
st.header("識別コード管理")

# GASが理解するアクションコード
action_map = {
    "追加": "add",
    "編集": "edit",
    "消去": "delete"
}

with st.form("manage_code"):
    action_jp = st.selectbox("操作", ["追加", "編集", "消去"])
    code      = st.text_input("識別コード")
    url       = st.text_input("URL (追加/編集時のみ)")

    submitted = st.form_submit_button("実行")
    if submitted:
        gas_action = action_map[action_jp]  # 日本語→GAS向けコードに変換

        payload = {
            "action": gas_action,
            "code": code,
            "url": url
        }

        try:
            r = requests.post(GAS_ENDPOINT, data=payload, timeout=10)
            try:
                res = r.json()
                if res.get("status") == "ok":
                    st.success(f"{action_jp} 成功")
                else:
                    st.error(f"{action_jp} 失敗: {res.get('message')}")
            except:
                # JSON でない場合でも成功メッセージ表示
                st.success(f"{action_jp} リクエスト送信完了")
        except Exception as e:
            st.error(f"通信エラー: {e}")




