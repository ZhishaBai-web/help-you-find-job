import streamlit as st
from scores_info import scores_total
from scores_info import scores_rag
import json
import pandas as pd
import io


if "new_job_infos" not in st.session_state:
    st.session_state.new_job_infos = None


# =============================================================================
# 全局 CSS 样式注入（单次注入，与 main_1.py 视觉系统完全一致）
# 包含：设计令牌、字体、关键帧动画、背景渐变、漂浮装饰、
#       玻璃拟态卡片、section-header 胶囊标题、Radio 选择卡片、
#       输入框（修正双重边框）、文件上传区、按钮流光动画、
#       终端日志窗、侧边栏毛玻璃、状态徽章、响应式布局
# =============================================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Quicksand:wght@400;500;600;700&family=ZCOOL+KuaiLe&display=swap" rel="stylesheet">

<style>
/* =====================================================================
   设计令牌（Design Tokens）—— 与 main_1.py 完全一致
   ===================================================================== */
:root {
    --macaron-pink: #ffb7d5;
    --macaron-blue: #a8d8ff;
    --macaron-purple: #d9c2ff;
    --macaron-mint: #b8f2d9;
    --macaron-yellow: #ffeaa7;
    --tech-blue: #5865f2;
    --tech-blue-dark: #404eed;
    --text-primary: #2d3748;
    --text-secondary: #718096;
    --card-bg: rgba(255, 255, 255, 0.78);
    --shadow-soft: 0 8px 32px rgba(88, 101, 242, 0.12);
    --shadow-hover: 0 12px 40px rgba(88, 101, 242, 0.18);
    --radius-xl: 28px;
    --radius-lg: 24px;
    --radius-md: 16px;
    --radius-sm: 12px;
    --transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

/* =====================================================================
   基础字体
   ===================================================================== */
.stApp {
    font-family: 'Noto Sans SC', 'Quicksand', sans-serif !important;
}

/* =====================================================================
   关键帧动画
   ===================================================================== */
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(5deg); }
}

@keyframes floatReverse {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(20px) rotate(-5deg); }
}

@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 200%; }
}

@keyframes fadeInUp {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* =====================================================================
   页面背景：柔和马卡龙渐变呼吸动画（15s 周期，与主页面呼应）
   ===================================================================== */
.stApp {
    background: linear-gradient(135deg, #fff7fb 0%, #f1f8ff 25%, #e6f3ff 50% ,#fff7fb 100%);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    color: var(--text-primary);
}

/* 隐藏 Streamlit 默认顶部 header */
header[data-testid="stHeader"] {
    background: transparent !important;
}

.main .block-container {
    padding-top: 1.5rem !important;
    position: relative;
    z-index: 1;
}

/* =====================================================================
   漂浮装饰色块（背景层，4 个漂浮 blob 分布四角）
   ===================================================================== */
.floating-decorations {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

.floating-blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(70px);
    opacity: 0.32;
}

.blob-1 { width: 320px; height: 320px; background: var(--macaron-pink);  top: 8%;  left: -6%;  animation: float 10s ease-in-out infinite; }
.blob-2 { width: 280px; height: 280px; background: var(--macaron-blue);  top: 38%; right: -6%;  animation: floatReverse 10s ease-in-out infinite; animation-delay: 2s; }
.blob-3 { width: 240px; height: 240px; background: var(--macaron-purple);bottom:12%; left: 12%;  animation: float 14s ease-in-out infinite; animation-delay: 4s; }
.blob-4 { width: 200px; height: 200px; background: var(--macaron-mint);  bottom:28%;right: 18%;  animation: floatReverse 11s ease-in-out infinite; animation-delay: 1s; }

/* =====================================================================
   标题层级字体 —— 与 main_1.py 保持一致
   ===================================================================== */
h1 {
    font-family:  'Noto Sans SC', cursive !important;
    background: linear-gradient(135deg, #ff6fa5 0%, #5865f2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    text-align: center;
    margin-bottom: 0.5rem !important;
    letter-spacing: 1px;
}

h2 {
    font-family: 'Noto Sans SC', sans-serif !important;
    color: var(--tech-blue);
    font-size: 1.6rem !important;
    margin-top: 1.2rem !important;
    margin-bottom: 1rem !important;
    font-weight: 600 !important;
}

h3, h4, h5, h6 {
    font-family: 'Quicksand', 'Noto Sans SC', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text-primary);
}

/* =====================================================================
   分区标题 pill（section-header）—— 与 main_1.py 完全一致
   ===================================================================== */
.section-header {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    background: linear-gradient(135deg, rgba(255, 111, 165, 0.12) 0%, rgba(88, 101, 242, 0.12) 100%);
    padding: 0.6rem 1.2rem;
    border-radius: 50px;
    margin-bottom: 1.2rem;
    color: var(--tech-blue);
    font-weight: 700;
    font-size: 1.4rem;
}

/* =====================================================================
   玻璃拟态卡片 —— 与 main_1.py 完全一致
   ===================================================================== */
.glass-card {
    background: var(--card-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: var(--radius-lg);
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow-soft);
    transition: var(--transition);
    animation: fadeInUp 0.6s ease-out;
}

.glass-card:hover {
    box-shadow: var(--shadow-hover);
    transform: translateY(-3px);
}

/* =====================================================================
   Radio 选择卡片：横向 flex 布局、玻璃态、hover 上移、选中渐变
   与 page_1.py 方案一致，过渡时间 0.3s
   ===================================================================== */
[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 10px !important;
}

[data-testid="stRadio"] label {
    background: rgba(255, 255, 255, 0.65) !important;
    border: 2px solid rgba(168, 216, 255, 0.30) !important;
    border-radius: 20px !important;
    padding: 10px 20px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    margin: 0 !important;
    font-weight: 500 !important;
    color: var(--text-primary) !important;
    font-size: 0.92rem !important;
}

[data-testid="stRadio"] label > div:first-child > div {
    width: 16px !important;
    height: 16px !important;
    border-color: var(--macaron-blue) !important;
}

[data-testid="stRadio"] label:hover {
    background: rgba(168, 216, 255, 0.22) !important;
    border-color: var(--tech-blue) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 24px rgba(88, 101, 242, 0.14) !important;
}

[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, rgba(168, 216, 255, 0.45), rgba(217, 194, 255, 0.45)) !important;
    border-color: var(--tech-blue) !important;
    box-shadow: 0 2px 12px rgba(88, 101, 242, 0.22) !important;
    font-weight: 700 !important;
}

[data-testid="stRadio"] label p {
    font-size: 0.92rem !important;
    font-weight: inherit !important;
}

/* =====================================================================
   输入框样式修正：消除双重边框与内框紫光冲突
   外壳 14px 圆角 + 纯白背景 + 1px #e0e0e0 边框
   Focus 时仅外层高亮，内框保持白色
   ===================================================================== */
.stTextInput div[data-baseweb="base-input"],
.stTextArea div[data-baseweb="textarea"] {
    background-color: #ffffff !important;
    background: #ffffff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 14px !important;
}

.stTextInput input,
.stTextArea textarea {
    background-color: #ffffff !important;
    background: #ffffff !important;
    color: #2d3748 !important;
}

.stTextInput div[data-baseweb="base-input"]:focus-within,
.stTextArea div[data-baseweb="textarea"]:focus-within {
    background-color: #ffffff !important;
    border-color: #5865f2 !important;
    box-shadow: 0 0 0 3px rgba(88, 101, 242, 0.15) !important;
}

/* =====================================================================
   文件上传区样式修正：虚线卡片 + hover 主题色
   ===================================================================== */
[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.6) !important;
    border: 2px dashed #cccccc !important;
    border-radius: var(--radius-md) !important;
    padding: 1.5rem !important;
    transition: var(--transition) !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--tech-blue) !important;
    background: rgba(255, 255, 255, 0.85) !important;
    box-shadow: 0 0 0 4px rgba(88, 101, 242, 0.1) !important;
}

[data-testid="stFileUploader"] section button {
    background: linear-gradient(135deg, var(--macaron-pink) 0%, var(--macaron-blue) 100%) !important;
    color: white !important;
    border-radius: 50px !important;
    border: none !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    transition: var(--transition) !important;
    font-size: 14px !important;
}

[data-testid="stFileUploaderFile"] button,
[data-testid="stFileUploaderDeleteBtn"] {
    display: none !important;
}

/* =====================================================================
   按钮样式：渐变 + 流光斜切扫过 + 悬浮放大
   高度 50px / 字重 500 / 字号 16px / shimmer 0.8s / hover 0.2s
   ===================================================================== */
.stButton > button {
    background: linear-gradient(135deg, #ff6fa5 0%, #8fa7ff 50%, #5865f2 100%) !important;
    background-size: 200% 200% !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    height: 50px !important;
    padding: 0 2.5rem !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    text-align: center !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 6px 20px rgba(88, 101, 242, 0.25) !important;
    transition: all 0.2s ease !important;
    animation: gradientShift 4s ease infinite !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    transform: skewX(-25deg);
    animation: shimmer 0.8s ease-in-out infinite;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 10px 28px rgba(88, 101, 242, 0.35) !important;
}

.stButton > button:active {
    transform: translateY(0) scale(0.98) !important;
}

/* =====================================================================
   终端日志窗口：半透明玻璃卡片 + 等宽终端字体
   背景透明度 0.7，字体 Consolas / Monaco / monospace
   ===================================================================== */
.terminal-window {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(168, 216, 255, 0.35);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    margin: 1rem 0 1.5rem 0;
    box-shadow: var(--shadow-soft);
}

.terminal-window [data-testid="stText"] {
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
    color: #4a7fd4 !important;
    font-size: 0.88rem !important;
    background: rgba(168, 216, 255, 0.06) !important;
    padding: 1rem 1.2rem !important;
    border-radius: 12px !important;
    line-height: 1.7 !important;
    border: 1px solid rgba(168, 216, 255, 0.15) !important;
}

/* Status 组件美化 */
[data-testid="stStatus"] {
    background: transparent !important;
    border: none !important;
}

[data-testid="stStatus"] > div:first-child {
    background: rgba(255, 255, 255, 0.7) !important;
    border: 1px solid rgba(168, 216, 255, 0.3) !important;
    border-radius: 16px !important;
    padding: 0.8rem 1.2rem !important;
}

/* =====================================================================
   下载按钮样式：马卡龙渐变 + 悬浮效果
   ===================================================================== */
.stDownloadButton > button {
    background: linear-gradient(135deg, #b8f2d9 0%, #a8d8ff 50%, #d9c2ff 100%) !important;
    background-size: 200% 200% !important;
    color: var(--text-primary) !important;
    border: 1.5px solid rgba(88, 101, 242, 0.2) !important;
    border-radius: 50px !important;
    height: 50px !important;
    padding: 0 2.5rem !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 16px rgba(88, 101, 242, 0.12) !important;
    transition: var(--transition) !important;
    animation: gradientShift 5s ease infinite !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 10px 28px rgba(88, 101, 242, 0.22) !important;
    border-color: var(--tech-blue) !important;
}

/* =====================================================================
   侧边栏：毛玻璃背景 + 胶囊标题
   ===================================================================== */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.65) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.8) !important;
}

.sidebar-title {
    font-family: 'ZCOOL KuaiLe', 'Noto Sans SC', sans-serif !important;
    color: var(--tech-blue);
    font-size: 1.2rem;
    margin-top: 0.5rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 0.4rem;
}

/* =====================================================================
   状态徽章：半透明胶囊样式
   ===================================================================== */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.78rem;
    padding: 0.25rem 0.6rem;
    border-radius: 20px;
    font-weight: 600;
    margin-top: -0.4rem;
    margin-bottom: 0.6rem;
}

.status-success {
    background: rgba(184, 242, 217, 0.4);
    color: #1e7e51;
    border: 1px solid rgba(184, 242, 217, 0.8);
}

.status-warning {
    background: rgba(255, 234, 167, 0.4);
    color: #9e7300;
    border: 1px solid rgba(255, 234, 167, 0.8);
}

.status-info {
    background: rgba(168, 216, 255, 0.35);
    color: #2b6cb0;
    border: 1px solid rgba(168, 216, 255, 0.6);
}

/* =====================================================================
   上传状态标签
   ===================================================================== */
.upload-status {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(88, 101, 242, 0.08);
    color: var(--tech-blue);
    padding: 0.5rem 1rem;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 600;
    margin: 0.5rem 0;
}

/* =====================================================================
   提示信息 / Alert
   ===================================================================== */
.stAlert {
    border-radius: var(--radius-md) !important;
    border: none !important;
    box-shadow: var(--shadow-soft) !important;
}

div[data-testid="stAlert"][kind="success"] {
    background: rgba(184, 242, 217, 0.3) !important;
    border: 1px solid rgba(184, 242, 217, 0.6) !important;
}

div[data-testid="stAlert"][kind="error"] {
    background: rgba(255, 183, 213, 0.25) !important;
    border: 1px solid rgba(255, 183, 213, 0.5) !important;
}

/* =====================================================================
   分隔线：渐变发光细线，替换默认 st.divider()
   ===================================================================== */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(88, 101, 242, 0.2), transparent) !important;
    margin: 2rem 0 !important;
}

/* =====================================================================
   加载动画
   ===================================================================== */
.stSpinner > div {
    border-color: var(--tech-blue) transparent transparent transparent !important;
}

/* =====================================================================
   响应式适配
   ===================================================================== */
@media (max-width: 768px) {
    h1 { font-size: 2rem !important; }
    .glass-card { padding: 1.2rem; }
    .section-header { font-size: 1.2rem !important; }
    .stButton > button {
        height: 46px !important;
        padding: 0 1.5rem !important;
        font-size: 14px !important;
    }
    [data-testid="stRadio"] label {
        padding: 8px 14px !important;
        font-size: 0.85rem !important;
    }
}

@media (max-width: 480px) {
    .block-container { padding: 1rem 0.8rem !important; }
    h2 { font-size: 1.3rem !important; }
    .section-header { font-size: 1.1rem !important; }
}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 背景漂浮装饰色块
# =============================================================================
st.markdown("""
<div class="floating-decorations">
    <div class="floating-blob blob-1"></div>
    <div class="floating-blob blob-2"></div>
    <div class="floating-blob blob-3"></div>
    <div class="floating-blob blob-4"></div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# 页面配置
# =============================================================================
st.set_page_config(
    page_title="分析喵",
    page_icon="🐱",
    layout="wide"
)
# =============================================================================
# 侧边栏：API 授权配置 + 向量库配置（玻璃卡片 + 状态徽章）
# =============================================================================
with st.sidebar:
    # ---- 模块 1：API 授权配置 ----
    st.markdown('<div class="sidebar-title">🔑 API 授权配置</div>', unsafe_allow_html=True)

    key = st.text_input("API Key：", type="password", placeholder="请输入您的 Key")
    if key:
        st.markdown('<div class="status-badge status-success">✓ Key 已配置</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-warning">! Key 待输入</div>', unsafe_allow_html=True)

    url = st.text_input("API URL：", placeholder="请输入 API 地址")
    if url:
        st.markdown('<div class="status-badge status-success">✓ URL 已配置</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-warning">! URL 待输入</div>', unsafe_allow_html=True)

    model = st.text_input("岗位分析模型：", value="gpt-5-nano-2025-08-07", placeholder="请输入 岗位分析 模型")
    if model:
        st.markdown(f'<div class="status-badge status-info">{model}</div>', unsafe_allow_html=True)

    st.divider()

    # ---- 模块 2：向量 API 授权配置（选配） ----
    st.markdown('<div class="sidebar-title">🔑 向量 API 授权配置（选配）</div>', unsafe_allow_html=True)

    db_key = st.text_input("向量库API Key：", type="password", placeholder="请输入向量库 Key（若RAG未开启，则无需填写）")
    if db_key:
        st.markdown('<div class="status-badge status-success">✓ 向量库 Key 已配置</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-warning">! 向量库 Key 待输入</div>', unsafe_allow_html=True)

    db_url = st.text_input("向量库 API URL：", placeholder="请输入向量库 API 地址（若RAG未开启，则无需填写）")
    if db_url:
        st.markdown('<div class="status-badge status-success">✓ 向量库 URL 已配置</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-warning">! 向量库 URL 待输入</div>', unsafe_allow_html=True)

    db_model = st.text_input("向量库模型：", value="text-embedding-3-large", placeholder="请输入 向量库 模型")
    if db_model:
        st.markdown(f'<div class="status-badge status-info">{db_model}</div>', unsafe_allow_html=True)


# =============================================================================
# 🎨 Hero 区域：分析喵标题
# =============================================================================
st.title("分析喵 · 猫谋远虑")
st.markdown(
    '<p style="text-align:center;color:#718096;font-size:1.05rem;margin-top:0.3rem;margin-bottom:1rem;">'
    '🐱 让分析喵帮您给岗位打分，喵算如神 喵 ~</p>',
    unsafe_allow_html=True
)

# =============================================================================
# 🐾 Card 1: 岗位与画像输入
# =============================================================================
st.markdown('<div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">💺 岗位信息</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("请上传爬虫喵捕获的岗位信息", type=["json"])

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">🖼️ 画像信息</div>', unsafe_allow_html=True)
json_profile = st.text_area("JSON画像",placeholder="请将工作喵输出的JSON画像内容复制到此处",label_visibility="collapsed")


# =============================================================================
# ⚙️ Card 2: 分析模式配置
# =============================================================================
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">⚙️ 分析模式</div>', unsafe_allow_html=True)

analysis_choice = st.radio("分析选择",
                           ["普通分析（对全部岗位进行评分，无需配置向量库）",
                            "Rag分析（仅分析匹配度最高的 Top50 岗位，需要配置向量库）"],
                           label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1.3, 1, 1])
with col2:
    submit = st.button("配置完成 🐾")

st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 配置校验逻辑（保留原有业务逻辑，不做任何修改）
# =============================================================================
submit_next = False
if submit:
    errors = []
    if not key:
        errors.append("- API Key")
    if not url:
        errors.append("- API URL")
    if not uploaded_file:
        errors.append("- 岗位 JSON 文件")
    if not json_profile.strip():
        errors.append("- JSON 画像")
    if "Rag分析" in analysis_choice:
        if not db_key:
            errors.append("- 向量库 API Key ")
        if not db_url:
            errors.append("- 向量库 API URL ")
        if not db_model:
            errors.append("- 向量库模型")
        if uploaded_file:
            content = uploaded_file.getvalue().decode("utf-8")
            datas = json.loads(content)

    if errors:
        st.error(
            "请先检测以下配置：\n\n" + "\n".join(errors),
            icon="🚨"
        )
        submit_next = False
    if not errors:
        st.success("🎉 所有配置已完成，分析风暴启动喵！")
        st.session_state.new_job_infos = None
        submit_next = True

# =============================================================================
# 渐变分隔线
# =============================================================================
st.markdown('<hr>', unsafe_allow_html=True)
# =============================================================================
# 🌀 风暴分析区（终端风格日志窗口）
# =============================================================================
st.markdown('<div class="section-header">🌀 风暴分析区</div>', unsafe_allow_html=True)


download = False
with st.status("🌪️ 正在启动分析引擎...", expanded=True) as status:

    if submit_next and st.session_state.new_job_infos == None:
        placeholder = st.empty()
        logs = []

        def log(message):
            """实时日志回调：将分析进度消息追加到终端窗口"""
            logs.append(message)
            # 使用 code 格式渲染多行终端文本，格式更美观，且多行渲染更稳定
            placeholder.text("\n".join(logs))

        if "Rag分析" not in analysis_choice:
            try:
                st.session_state.new_job_infos = scores_total(uploaded_file, json_profile, key, url, model, log)
                status.update(label="🎉 分析完成喵！", state="complete", expanded=True)
                st.success("🎉 分析已完成，记得下载分析数据喵。")
                download = True
            except Exception:
                st.error("😭 分析出错了，请检查key、url、分析模型是否配置正确。")
                status.update(label="😭 分析失败喵~", state="error", expanded=True)
                download = False
        if "Rag分析" in analysis_choice:
            # try:
                st.session_state.new_job_infos = scores_rag(db_key, db_url, db_model, uploaded_file, json_profile, key, url, model, log)
                status.update(label="🎉 分析完成喵！", state="complete", expanded=True)
                st.success("🎉 分析已完成，记得下载分析数据喵。")
                download = True
            # except Exception:
            #     st.error("😭 模型出错了，请检查key、url、分析模型是否配置正确。")
            #     status.update(label="😭 分析失败喵~", state="error", expanded=True)
            #     download = False
    else:
        st.write("🦉 分析风暴尚未准备就绪，请配置完成所有信息，并点击「配置完成」按钮。")

st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 📦 分析结果下载区（玻璃卡片）
# =============================================================================


if st.session_state.new_job_infos:
    colu1, colu2 = st.columns([1, 1])
    with colu1:
        json_data = json.dumps(
            st.session_state.new_job_infos,
            ensure_ascii=False,
            indent=4
        )

        st.download_button(
            label="📥 下载岗位数据(JSON)",
            data=json_data,
            file_name="职位信息.json",
            mime="application/json",
            use_container_width=True
        )

    with colu2:
        df = pd.DataFrame(st.session_state.new_job_infos)
        df = df.rename(
            columns={
                "match_score": "总得分",
                "ability_match": "能力得分",
                "responsibility_match": "职责得分",
                "career_match": "发展得分",
                "background_match": "背景得分",
                "development_value": "潜力得分",
                "recommend_reason": "推荐理由",
                "matching_strengths": "匹配优势",
                "possible_gaps": "待提升项",
                "development_analysis": "发展建议",
            }
        )

        for col in df.columns:
            df[col] = df[col].apply(
                lambda x:
                "\n".join(map(str, x)) if isinstance(x, list)
                else json.dumps(x, ensure_ascii=False, indent=2)
                if isinstance(x, dict)
                else x
            )

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        st.download_button(
            label="📥 下载岗位匹配结果(Excel)",
            data=buffer.getvalue(),
            file_name="岗位匹配结果.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)