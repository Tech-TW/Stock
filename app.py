import streamlit as st
import pandas as pd
import sys
import platform

# 1. Page Config (必須是第一行執行)
st.set_page_config(
    page_title="Portfolio Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 自定義 CSS (讓介面變漂亮)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stCard {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    .big-font {
        font-size: 1.2rem !important;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 標題區
st.title("📊 Portfolio Analyzer")
st.markdown("<p class='big-font'>專業級投資組合分析與回測系統</p>", unsafe_allow_html=True)
st.divider()

# 4. 狀態檢查與導覽
if "uploaded_df" not in st.session_state or st.session_state["uploaded_df"] is None:
    # --- 尚未上傳資料的畫面 ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 👋 歡迎使用")
        st.info("目前尚未偵測到數據，請依照下列步驟操作：")
        
        step_cols = st.columns(2)
        with step_cols[0]:
            st.markdown("""
            #### 1️⃣ 上傳資料
            前往 **Upload** 頁面，上傳你的交易紀錄 (CSV/Excel) 或貼上 GitHub Raw 連結。
            """)
        with step_cols[1]:
            st.markdown("""
            #### 2️⃣ 執行分析
            資料載入後，前往 **Analyze** 頁面查看績效圖表、持倉分析與月報表。
            """)
            
    with col2:
        st.markdown("### 🛠️ 系統狀態")
        with st.expander("System Info", expanded=True):
            st.write(f"**Python:** {sys.version.split()[0]}")
            st.write(f"**Pandas:** {pd.__version__}")
            st.write(f"**Platform:** {platform.system()}")
            st.caption("All dependencies loaded.")

else:
    # --- 已有資料的儀表板 (Dashboard Preview) ---
    df = st.session_state["uploaded_df"]
    
    st.success("✅ 資料已載入就緒！請前往 **Analyze** 頁面開始分析。")
    
    # 數據概觀卡片
    st.markdown("### 📁 資料集概觀 (Dataset Overview)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("總筆數 (Rows)", f"{len(df):,}")
    m2.metric("欄位數 (Columns)", f"{len(df.columns)}")
    m3.metric("起始日期", str(df.iloc[:,0].min())[:10] if not df.empty else "-") # 假設第一欄是日期
    m4.metric("記憶體用量", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")

    # 預覽區域
    with st.expander("🔍 查看詳細數據內容 (Data Preview)", expanded=True):
        st.dataframe(df.head(100), use_container_width=True)
        
    # 清除資料按鈕
    if st.button("🗑️ 清除目前資料 (Reset)", type="secondary"):
        st.session_state["uploaded_df"] = None
        st.rerun()
