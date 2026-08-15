import streamlit as st
import pandas as pd
import numpy as np
from tools_info import get_top50_df
from tools_info import concat_files
from tools_info import get_analysis_df
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import seaborn as sns
import os


# 1. 尝试动态加载同目录下的 msyh.ttc 字体（直接通过 fname 设置，绕过 Linux 对 .ttc 的 rcParams 赋值 Bug）
font_path = "msyh.ttc"
custom_font = None

if os.path.exists(font_path):
    try:
        # 显式注册字体文件
        fm.fontManager.addfont(font_path)
        font_prop = fm.FontProperties(fname=font_path)
        custom_font = font_prop.get_name()
    except Exception:
        pass

# 2. 构建跨平台字体优先级列表（按系统顺序自动降级匹配）
font_list = []
if custom_font:
    font_list.append(custom_font)

# 补充跨平台默认字体
font_list.extend([
    "Microsoft YaHei",    # Windows 微软雅黑
    "SimHei",             # Windows 黑体
    "PingFang SC",        # Mac 苹方
    "Noto Sans CJK SC",   # Streamlit Cloud (Linux packages.txt 安装的字体)
    "DejaVu Sans"         # 兜底英文
])

# 3. 设置 Matplotlib 字体配置
plt.rcParams["font.sans-serif"] = font_list
plt.rcParams["axes.unicode_minus"] = False


if "new_file" not in st.session_state:
    st.session_state.new_file = False
if "top50_df" not in st.session_state:
    st.session_state.top50_df = False
if "total_df" not in st.session_state:
    st.session_state.total_df = False



st.set_page_config(
    page_title="工具喵",
    page_icon="🐱",
    layout="wide"
)

# =============================================================================
# 全局 CSS 样式注入（单次注入，与 main_1.py / page_1.py / page_2.py 视觉系统完全一致）
# 包含：设计令牌、字体、关键帧动画、背景渐变、漂浮装饰、
#       玻璃拟态卡片、section-header 胶囊标题、Radio 选择卡片、
#       输入框（修正双重边框）、文件上传区、按钮流光动画、
#       终端日志窗、Tabs 胶囊导航、Alert 美化、响应式布局
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
    background: linear-gradient(135deg, #fff7fb 0%, #f1f8ff 25%, #e6f3ff 50%, #fff7fb 100%);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    color: var(--text-primary);
}

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

/* 子分区标题（略小） */
.section-header-sm {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, rgba(255, 111, 165, 0.10) 0%, rgba(88, 101, 242, 0.10) 100%);
    padding: 0.45rem 1rem;
    border-radius: 50px;
    margin-bottom: 0.8rem;
    color: var(--tech-blue);
    font-weight: 700;
    font-size: 1.1rem;
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
   与 page_1.py / page_2.py 方案一致，过渡时间 0.3s
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
   Tabs 胶囊式导航 —— 与 main_1.py 完全一致
   ===================================================================== */
.stTabs [role="tablist"] {
    background: rgba(255, 255, 255, 0.5) !important;
    border-radius: 50px !important;
    padding: 6px !important;
    gap: 6px !important;
    border: 1px solid rgba(88, 101, 242, 0.1) !important;
}

.stTabs [role="tab"] {
    font-family: 'Quicksand', 'Noto Sans SC', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: var(--text-secondary) !important;
    border-radius: 50px !important;
    padding: 0.6rem 1.2rem !important;
    transition: var(--transition) !important;
    border: none !important;
    border-bottom: none !important;
}

.stTabs [role="tab"]:hover {
    color: var(--tech-blue) !important;
    background: rgba(88, 101, 242, 0.08) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--tech-blue) 0%, #8fa7ff 100%) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(88, 101, 242, 0.25) !important;
    border: none !important;
}

[data-baseweb="tab-highlight-tile"],
[data-baseweb="tab-border"],
[data-baseweb="tab-highlight"] {
    clip-path: inset(100%) !important;
    background: transparent !important;
    border: none !important;
    visibility: hidden !important;
}

[data-baseweb="tab-list"],
.stTabs [role="tablist"] {
    border-bottom: none !important;
    background: rgba(255, 255, 255, 0.5) !important;
}

.stTabs [role="tab"] {
    border: none !important;
    border-bottom: none !important;
}

.stTabs [aria-selected="true"] {
    border: none !important;
    border-bottom: none !important;
    background: linear-gradient(135deg, var(--tech-blue) 0%, #8fa7ff 100%) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(88, 101, 242, 0.25) !important;
}

/* =====================================================================
   Expander 展开面板美化
   ===================================================================== */
[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.6) !important;
    border: 1px solid rgba(168, 216, 255, 0.3) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: var(--shadow-soft) !important;
}

/* =====================================================================
   Metric 指标卡片美化
   ===================================================================== */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.7) !important;
    border: 1px solid rgba(168, 216, 255, 0.25) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.8rem 1rem !important;
    box-shadow: 0 2px 8px rgba(88, 101, 242, 0.06) !important;
    transition: var(--transition) !important;
}

[data-testid="stMetric"]:hover {
    border-color: var(--tech-blue) !important;
    box-shadow: 0 4px 16px rgba(88, 101, 242, 0.12) !important;
    transform: translateY(-2px) !important;
}

[data-testid="stMetricValue"] {
    color: var(--tech-blue) !important;
    font-weight: 700 !important;
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

div[data-testid="stAlert"][kind="info"] {
    background: rgba(168, 216, 255, 0.25) !important;
    border: 1px solid rgba(168, 216, 255, 0.5) !important;
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
   Subheader 样式覆盖
   ===================================================================== */
.stSubheader {
    color: var(--tech-blue) !important;
    font-weight: 700 !important;
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
    .section-header-sm { font-size: 1rem !important; }
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
# 侧边栏样式追加（卡片化与徽章美化）
# =============================================================================
st.markdown("""
<style>
/* 侧边栏整体背景与边框 */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.65) !important;
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.8) !important;
}

</style>
""", unsafe_allow_html=True)
# =============================================================================
# 🎨 Hero 区域：工具喵标题
# =============================================================================
st.title("工具喵 · 米奇喵喵屋")
st.markdown(
    '<p style="text-align:center;color:#718096;font-size:1.05rem;margin-top:0.3rem;margin-bottom:1rem;">'
    '🐱 海纳百川，有喵乃大；翻箱倒柜，喵艺俱全 </p>',
    unsafe_allow_html=True
)
# =============================================================================
# 🧩 Card 1: 合并工具
# =============================================================================
st.markdown('')
st.markdown('<div class="section-header">🧩 合并工具</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "请选择一个或多个 JSON 文件", type=["json"], accept_multiple_files=True
)

hr_select = st.radio("是否开启HR活跃度筛选", ["开启 HR 活跃度筛选", "不开启 HR 活跃度筛选"],label_visibility="collapsed")

col1, col2, col3 = st.columns([1.5, 1, 1])
with col2:
    submit1 = st.button("开始合并 🐾")

if submit1:
    if not uploaded_files:
        st.write("请上传需要合并的文件")
    else:
        st.session_state.new_file, words = concat_files(uploaded_files, hr_select)
        json_bytes = st.session_state.new_file.to_json(orient="records", force_ascii=False, indent=2)
        st.write(words)

        st.download_button(
            label="📥 下载岗位数据(JSON)",
            data=json_bytes,
            file_name="合并结果.json",
            mime="application/json",
            use_container_width=True
        )

st.divider()
# =============================================================================
# 🗺️ Card 2: 可视化工具
# =============================================================================
st.markdown('<div class="section-header">🗺️ 可视化工具</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("请上传分析喵输出的 JSON 文件", type=["json"])

st.divider()

# ---- 最值得关注的 Top 50 岗位 ----
st.markdown('<div class="section-header-sm">🏆 最值得关注的 Top 50 岗位</div>', unsafe_allow_html=True)

if not uploaded_file:
    st.write("文件上传后才能开始分析哦。")

if uploaded_file:
    try:
        st.session_state.top50_df = get_top50_df(uploaded_file)
        uploaded_file.seek(0)
        st.session_state.total_df = get_analysis_df(uploaded_file)

        columns_info = [
            "职位名称",
            "公司名称",
            "所在行业",
            "最低薪资",
            "最高薪资",
            "总得分",
            "HR活跃时间",
            "投递网址"
        ]

        st.dataframe(
            st.session_state.top50_df,
            hide_index=False,
            column_order=columns_info,
            use_container_width=True
        )

        with st.expander("关于表格数据的说明"):
            st.markdown("##### 1. 信息说明")
            st.markdown("""
            - 公司名称、公司成立日期、公司规模、所在行业、公司介绍、职位名称、薪资、时长要求、岗位地址、学历要求、岗位介绍、投递网址、HR活跃时间，该类信息为招聘网址原有信息；
            - 最低薪资、最高薪资由薪资转换而得，转换过程中，假定每月工作21.75天，每天工作8小时；
            - 总得分、能力得分、职责得分、发展得分、背景得分、潜力得分、推荐理由、匹配优势、待提升项、发展建议，该类信息为 AI 信息，其内容的准确性受 AI 模型影响；
            """)

            st.markdown("##### 2. 评分说明")
            st.markdown("""
            - 能力评分：满分35分，评价：专业技能、工具技能、行业经验、通用能力、可迁移能力；
            - 职责评分：满分25分，评价：过去经历是否能够支撑岗位的主要职责；
            - 发展评分：满分20分，评价：岗位是否符合长期职业规划、职业目标、未来发展方向；
            - 背景评分：满分10分，评价：学历、专业、工作经验、行业背景；
            - 潜力评分：满分10分，评价：岗位是否能够提升能力、增加职业竞争力、提供成长空间、提升长期职业价值；
            - 总评分：能力评分+职责评分+发展评分+背景评分+潜力评分。
            """)
            st.markdown("##### 3. 评分参考")
            st.markdown("""
            - 95~100分：高度匹配，可直接胜任，且符合长期发展。
            - 90~94分：匹配度很高，仅存在少量不足。
            - 80~89分：整体匹配，需要少量学习即可胜任。
            - 70~79分：存在一定能力差距，但具有较好的可迁移能力。
            - 60~69分：存在明显能力不足，仅作为备选。
            - 60分以下：匹配度较低。
            """)
    except Exception:
        st.error("请检查文件的内部格式是否正确。")

# ---- 单岗位分析 ----
st.divider()
st.markdown('<div class="section-header-sm">🔩 单岗位分析</div>', unsafe_allow_html=True)

column1, column2, column3 = st.columns([1.3, 1.3, 1])
with column1:
    company_name = st.text_input("", placeholder="请填写公司名称：", label_visibility="collapsed")
with column2:
    job_name = st.text_input("", placeholder="请填写岗位名称：", label_visibility="collapsed")
with column3:
    submit2 = st.button("开始查询 🐾")

single_info = False
if submit2:
    if not company_name:
        st.write("请填写公司名称")
    if not job_name:
        st.write("请填写岗位名称")
    if company_name and job_name:
        single_info = True

if single_info:
    tab1, tab2 = st.tabs(["📋 岗位基本信息", "🎯 岗位匹配维度"])
    try:
        job = st.session_state.top50_df[
            (st.session_state.top50_df["公司名称"] == company_name)
            & (st.session_state.top50_df["职位名称"] == job_name)
        ].iloc[0]
        with tab1:
            col1, col2, col3, col4 = st.columns([1,1.5,1.5,1])
            with col1:
                st.metric("总得分", job['总得分'])
            with col2:
                st.metric("薪资", job["薪资"])
            with col3:
                st.metric("经验要求", job["经验要求"])
            with col4:
                st.metric("学历要求", job["学历要求"])

            st.write(f"公司： {job['公司名称']}")
            st.write(f"职位： {job['职位名称']}")
            st.write(f"行业：{job['所在行业']}")
            st.write(f"地点： {job['岗位地址']}")
            st.markdown(f"""{job['岗位介绍']}""")
            st.markdown("#### 💡 AI 推荐理由")
            st.info(job["推荐理由"])

        with tab2:
            col1, col2 = st.columns([1, 1])
            with col1:

                score_data = pd.Series({
                    "能力得分": job["能力得分"],
                    "职责得分": job["职责得分"],
                    "发展得分": job["发展得分"],
                    "背景得分": job["背景得分"],
                    "潜力得分": job["潜力得分"]
                })
                labels = list(score_data.index)
                values = list(score_data.values)
                values.extend(values[:1])
                angles = np.linspace(0, 2 * np.pi, len(values))
                value = [35, 25, 20, 10, 10, 35]
                fig, ax = plt.subplots(
                    figsize=(6, 6), dpi=300,
                    subplot_kw={"polar": True}
                )
                ax.plot(angles, values, linewidth=2, label="得分线")
                ax.plot(angles, value, linewidth=2, label="满分线")
                ax.fill(angles, values, alpha=0.2)
                ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), frameon=True)
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(labels)
                ax.tick_params(pad=15)
                fig.patch.set_facecolor('none')  # 设置画布背景透明
                ax.set_facecolor('none')  # 设置雷达图极坐标区域背景透明
                for angle, val in zip(angles, values):
                    ax.text(
                        angle,
                        val + (max(values) * 0.05),
                        f"{val}",
                        ha="center",
                        va="center",
                        fontsize=9,
                        color="#333333",
                        fontweight="bold",
                    )
                ax.set_ylim(0, 35)
                st.pyplot(fig)
                plt.close(fig)

            with col2:
                st.markdown("##### ✅ 匹配优势")
                strengths = job["匹配优势"]
                if isinstance(strengths, list):
                    for item in strengths:
                        st.markdown(f"- {item}")
                else:
                    st.write(strengths)
                st.markdown("##### ⚠️ 待提升项")
                gaps = job["待提升项"]
                if isinstance(gaps, list):
                    for item in gaps:
                        st.markdown(f"- {item}")
                else:
                    st.write(gaps)

            st.markdown("#### 🚀 发展价值")
            st.success(job["发展建议"])
    except:
        with tab1:
            st.error("请检查，公司名或岗位名称是否输入正确")
        with tab2:
            st.error("请检查，公司名或岗位名称是否输入正确")
st.markdown('</div>', unsafe_allow_html=True)

st.divider()
# =============================================================================
# 📈 Card 3: 全岗位分析（终端风格）
# =============================================================================
st.markdown('<div class="section-header-sm">📈 全岗位分析</div>', unsafe_allow_html=True)
with st.status("分析准备中...", expanded=True) as status:
    if uploaded_file:
        try:
            total_df = st.session_state.total_df
            col1, col2, col3, col4 = st.columns([1.2, 1.3, 1.3, 1])
            with col1:
                st.metric("岗位总数", len(total_df))
            with col2:
                st.metric("平均匹配度", f"{total_df['总得分'].mean():.1f}")
            with col3:
                st.metric("最高匹配度", f"{total_df['总得分'].max():.0f}")
            with col4:
                high_match_count = (total_df["总得分"] >= 80).sum()
                st.metric("高匹配岗位( > 80分)", f"{high_match_count} 个")


            fig, ax = plt.subplots(2, 2, figsize=(16, 14))
            plt.subplots_adjust(hspace=0.3, wspace=0.23)
            fig.patch.set_facecolor('none')  # 设置画布背景透明
            ax[0,0].set_facecolor('none')  # 设置雷达图极坐标区域背景透明
            ax[0, 1].set_facecolor('none')
            ax[1, 0].set_facecolor('none')
            ax[1, 1].set_facecolor('none')
            sns.histplot(
                data=total_df,
                x="总得分",
                bins=np.arange(total_df["总得分"].min(), total_df["总得分"].max() + 5, 5),
                kde=True,
                ax=ax[0, 0]
            )
            mean_score = total_df["总得分"].mean()
            ax[0, 0].axvline(
                mean_score,
                linestyle="--",
                color="orange",
                label=f"平均匹配度：{mean_score:.1f}"
            )
            ax[0, 0].set_xlabel("匹配分数",fontsize=13)
            ax[0, 0].set_ylabel("岗位数量",fontsize=13)
            ax[0, 0].set_title("图1 岗位匹配分数分布",fontsize=17, y=-0.2)
            ax[0, 0].legend()

            score_cols = ["能力得分", "职责得分", "发展得分", "背景得分", "潜力得分"]
            avg_scores = total_df[score_cols].mean()
            sns.barplot(
                x=avg_scores.index,
                y=avg_scores.values,
                ax=ax[0, 1]
            )
            ax[0, 1].set_ylim(0, 35)
            ax[0, 1].set_xlabel("")
            ax[0, 1].tick_params(axis='x', labelsize=13)
            ax[0, 1].set_ylabel("平均得分",fontsize=13)
            ax[0, 1].set_title("图2 各匹配维度平均得分",fontsize=17, y=-0.17)
            for i, value in enumerate(avg_scores.values):
                ax[0, 1].text(
                    i,
                    value + 0.5,
                    f"{value:.1f}",
                    ha="center",
                    fontweight="bold"
                )

            total_df["平均薪资"] = (total_df["最低薪资"] + total_df["最高薪资"]) / 2
            col1, col2 = st.columns(2)
            sns.scatterplot(
                data=total_df,
                x="总得分",
                y="平均薪资",
                hue=total_df["公司规模"],
                alpha=0.6,
                s=60,
                ax=ax[1, 0]
            )
            ax[1, 0].set_ylim(3000, 12000)
            ax[1, 0].set_xlabel("总匹配得分",fontsize=13)
            ax[1, 0].set_ylabel("平均月薪（元）",fontsize=13)
            ax[1, 0].set_title("图3 薪资与岗位匹配度关系",fontsize=17, y=-0.2)

            industry_count = total_df["所在行业"].value_counts().head(10)
            sns.barplot(
                x=industry_count.values,
                y=industry_count.index,
                ax=ax[1, 1]
            )
            ax[1, 1].set_xlabel("岗位数量",fontsize=13)
            ax[1, 1].set_ylabel("")
            ax[1, 1].set_title("图4 岗位数量 Top 10 行业",fontsize=17, y=-0.2)

            st.pyplot(fig)
            plt.close(fig)
            status.update(label="全岗位分析完成喵！", state="complete", expanded=True)
        except Exception:
            status.update(label="全岗位分析失败喵~", state="complete", expanded=True)
            st.error("请检查文件的内部格式是否正确。")
    else:
        st.markdown("请检查分析文件是否上传")
