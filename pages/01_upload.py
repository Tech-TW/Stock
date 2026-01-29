import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import chardet

st.set_page_config(page_title="Upload Data", page_icon="📥", layout="wide")

st.title("📥 Import Data")
st.markdown("請選擇資料來源：本機檔案上傳 或 雲端連結匯入。")

# 使用 Tabs 分離邏輯，介面更清爽
tab1, tab2 = st.tabs(["📂 Upload File (CSV/Excel)", "☁️ Import from URL"])

# ========= 快取讀檔函式 =========
@st.cache_data(show_spinner=False)
def load_data_from_bytes(file_bytes, filename):
    """通用讀檔邏輯：根據副檔名自動判斷解析方式"""
    try:
        if filename.lower().endswith(".csv"):
            # 自動偵測編碼
            enc = chardet.detect(file_bytes).get("encoding") or "utf-8"
            return pd.read_csv(BytesIO(file_bytes), encoding=enc)
        else:
            # Excel
            return pd.read_excel(BytesIO(file_bytes))
    except Exception as e:
        raise ValueError(f"解析失敗: {e}")

# ========= Tab 1: 本機上傳 =========
with tab1:
    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        type=["csv", "xlsx", "xls"],
        help="支援 CSV 與 Excel 格式"
    )

    if uploaded_file is not None:
        try:
            with st.spinner("讀取檔案中..."):
                # 讀取 bytes
                bytes_data = uploaded_file.getvalue()
                df = load_data_from_bytes(bytes_data, uploaded_file.name)
                
                # 成功處理
                st.session_state["uploaded_df"] = df
                st.toast(f"成功載入: {uploaded_file.name}", icon="✅")
                st.success(f"File **{uploaded_file.name}** uploaded successfully!")
        except Exception as e:
            st.error(f"Error reading file: {e}")

# ========= Tab 2: URL 匯入 =========
with tab2:
    st.info("💡 提示：適用於 GitHub Raw 連結或公開的雲端檔案連結。")
    url = st.text_input("Paste file URL", placeholder="https://raw.githubusercontent.com/...")
    
    if st.button("🚀 Fetch Data", use_container_width=True):
        if not url:
            st.warning("請輸入 URL")
        else:
            try:
                with st.spinner("下載並解析中..."):
                    r = requests.get(url, timeout=30)
                    r.raise_for_status()
                    
                    # 嘗試從 URL 推斷檔名，若無則預設為 csv
                    filename = url.split("/")[-1]
                    if "." not in filename: 
                        filename = "data.csv"
                        
                    df = load_data_from_bytes(r.content, filename)
                    
                    st.session_state["uploaded_df"] = df
                    st.toast("雲端檔案載入成功！", icon="🎉")
                    st.success(f"Fetched from URL successfully! ({len(df)} rows)")
                    
            except Exception as e:
                st.error(f"Failed to fetch or parse URL: {e}")

# ========= 資料預覽區 (共用) =========
st.divider()

if "uploaded_df" in st.session_state and st.session_state["uploaded_df"] is not None:
    df_current = st.session_state["uploaded_df"]
    
    st.subheader("📊 Data Preview")
    
    # 簡單的資料品質檢查
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.write(f"**Dimensions:** {df_current.shape[0]} rows × {df_current.shape[1]} columns")
    with col_info2:
        missing_count = df_current.isnull().sum().sum()
        if missing_count > 0:
            st.warning(f"⚠️ 偵測到 {missing_count} 個缺值 (NaN)")
        else:
            st.success("✅ 無缺值 (Clean Data)")

    st.dataframe(df_current.head(50), use_container_width=True)
    
    # 引導下一步
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p>資料確認無誤後，請點擊左側側邊欄的 <b>Analyze</b> 進行分析。</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.caption("尚未載入任何資料 (No data loaded)")
