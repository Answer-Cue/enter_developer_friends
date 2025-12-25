import streamlit as st
from PIL import Image
import pyzbar.pyzbar as pyzbar
import re

st.title("QRコード読み取りアプリ")

st.write("カメラで QRコードを撮影すると、URL内の識別コード(p=)と日付を取得します。")

# カメラ入力
img_file = st.camera_input("QRコードを撮影")

if img_file is not None:
    img = Image.open(img_file)
    st.image(img, caption="撮影画像", use_column_width=True)

    # QRコード解析
    decoded_objects = pyzbar.decode(img)

    if decoded_objects:
        for obj in decoded_objects:
            qr_data = obj.data.decode("utf-8")
            st.write("読み取り結果:", qr_data)

            # URL内の p=xxxx を抽出
            match_code = re.search(r"[?&]p=([^&]+)", qr_data)
            if match_code:
                code = match_code.group(1)
                st.success(f"識別コード: {code}")
            else:
                st.warning("識別コード(p=)が見つかりませんでした")

            # URL内の日付を抽出 (例: ?date=2025-12-25)
            match_date = re.search(r"[?&]date=([\d-]+)", qr_data)
            if match_date:
                date = match_date.group(1)
                st.info(f"日付: {date}")
            else:
                st.info("日付が見つかりませんでした")
    else:
        st.warning("QRコードが検出できませんでした")
