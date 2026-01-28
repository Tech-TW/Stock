import streamlit as st

st.set_page_config(page_title="Portfolio Analyzer", page_icon="📊", layout="wide")

# --- Minimal CSS (高級感關鍵：卡片、間距、按鈕) ---
st.markdown("""
<style>
/* Hide Streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Page padding */
.block-container {padding-top: 2.2rem; padding-bottom: 2.2rem;}

/* Fancy hero card */
.hero {
  border: 1px solid rgba(255,255,255,0.08);
  background: radial-gradient(1200px circle at 10% 10%, rgba(124,58,237,0.25), transparent 55%),
              radial-gradient(900px circle at 90% 30%, rgba(59,130,246,0.18), transparent 60%),
              rgba(17,26,46,0.55);
  border-radius: 20px;
  padding: 28px 28px;
}
.hero h1 {margin: 0; font-size: 34px; letter-spacing: -0.3px;}
.hero p  {margin: 8px 0 0 0; color: rgba(229,231,235,0.78); font-size: 15px; line-height: 1.6;}

/* Card */
.card {
  border: 1px solid rgba(255,255,255,0.08);
  background: rgba(17,26,46,0.55);
  border-radius: 18px;
  padding: 18px 18px;
}
.card h3 {margin: 0 0 8px 0; font-size: 16px;}
.muted {color: rgba(229,231,235,0.70); font-size: 13px; line-height: 1.6;}
</style>
""", unsafe_allow_html=True)

# --- Hero ---
st.markdown("""
<div class="hero">
  <h1>📊 Portfolio Analyzer</h1>
  <p>Institutional-grade portfolio analytics for your trades.<br/>
     Upload → Validate → Analyze → Export. Fast, consistent, and reproducible.</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- Session status (用卡片/指標取代 dataframe) ---
df = st.session_state.get("uploaded_df", None)
has_df = df is not None

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Data Loaded", "Yes" if has_df else "No")
with c2:
    st.metric("Rows", f"{len(df):,}" if has_df else "-")
with c3:
    st.metric("Columns", f"{df.shape[1]:,}" if has_df else "-")
with c4:
    st.metric("Preview", "Ready" if has_df else "Upload first")

st.write("")

# --- Action cards ---
left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.markdown("""<div class="card"><h3>Next steps</h3>
    <div class="muted">
    1) Go to <b>Upload</b> and import CSV/Excel or paste a GitHub raw link.<br/>
    2) Then open <b>Analyze</b> for charts, risk metrics, and report export.
    </div></div>""", unsafe_allow_html=True)

    st.write("")
    b1, b2 = st.columns(2)
    with b1:
        st.page_link("pages/01_upload.py", label="⬆️ Go to Upload", use_container_width=True)
    with b2:
        st.page_link("pages/02_analyze.py", label="🚀 Go to Analyze", use_container_width=True)

with right:
    st.markdown("""<div class="card"><h3>What you’ll get</h3>
    <div class="muted">
    • Holdings & performance summary<br/>
    • Realized / unrealized P&amp;L<br/>
    • FX-aware cost basis<br/>
    • Exportable Excel report
    </div></div>""", unsafe_allow_html=True)

# --- Debug 放到 sidebar（專業感提升很大） ---
with st.sidebar:
    st.subheader("Status")
    st.write("Uploaded:", "✅" if has_df else "❌")

    with st.expander("Env / Debug info", expanded=False):
        try:
            import sys, platform, pathlib
            st.write("Python:", sys.version)
            st.write("Platform:", platform.platform())
            st.write("CWD:", pathlib.Path().resolve())
            st.success("Core OK")
        except Exception as e:
            st.error(f"Import error: {e}")
