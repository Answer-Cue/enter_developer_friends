import streamlit as st
from PIL import Image
import pyzbar.pyzbar as pyzbar
import re
import pandas as pd
import requests
from urllib.parse import quote

st.title("QR読み取り＋スプレッドシート管理")

# ----------------------------
# シークレット
# ----------------------------
SHEET_ID     = st.secrets["SHEET_ID"]
GAS_ENDPOINT = st.secrets["GAS_ENDPOINT"]

# ----------------------------
# データ保持
# ----------------------------
if "qr_records" not in st.session_state:
    st.session_state.qr_records = []

# ----------------------------
# QR読み取り
# ----------------------------
st.header("QRコード読み取り")
img_file = st.camera_input("QRコードを撮影")

if img_file is not None:
    img = Image.open(img_file)
    st.image(img, caption="撮影画像", use_column_width=True)

    decoded_objects = pyzbar.decode(img)
    if decoded_objects:
        for obj in decoded_objects:
            qr_data = obj.data.decode("utf-8")
            match_code = re.search(r"[?&]p=([^&]+)", qr_data)
            code = match_code.group(1) if match_code else ""
            match_date = re.search(r"[?&]date=([\d-]+)", qr_data)
            date = match_date.group(1) if match_date else ""
            st.session_state.qr_records.append({
                "識別コード": code,
                "日付": date,
                "URL": qr_data
            })

# ----------------------------
# 表として表示
# ----------------------------
if st.session_state.qr_records:
    st.subheader("読み取り結果一覧")
    df_qr = pd.DataFrame(st.session_state.qr_records)
    edited_df = st.data_editor(df_qr, num_rows="dynamic")
    st.session_state.qr_records = edited_df.to_dict("records")

# ----------------------------
# スプレッドシート管理
# ----------------------------
st.header("スプレッドシート管理")

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

st.header("識別コード管理フォーム")
action_map = {"追加": "add", "編集": "edit", "消去": "delete"}

with st.form("manage_code"):
    action_jp = st.selectbox("操作", ["追加", "編集", "消去"])
    # QR読み取り結果から初期値選択可能
    code_list = [r["識別コード"] for r in st.session_state.qr_records]
    code = st.selectbox("識別コード", options=code_list if code_list else [""])
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

