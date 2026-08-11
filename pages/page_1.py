import streamlit as st
from scrapy_info import get_url
from scrapy_info import get_job_information
import json

# =============================================================================
# 页面配置
# =============================================================================
st.set_page_config(
    page_title="爬虫喵",
    page_icon="🐱",
    layout="wide"
)

# =============================================================================
# 全局 CSS 样式注入：马卡龙猫咪科技风主题
# 包含设计令牌、字体、动画、玻璃拟态卡片、Radio 选择卡片、
# 按钮流光动画、终端日志窗、数据宝箱、响应式布局
# =============================================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Quicksand:wght@400;500;600;700&family=ZCOOL+KuaiLe&display=swap" rel="stylesheet">

<style>
/* =====================================================================
   设计令牌（Design Tokens）
   ===================================================================== */
:root {
    --sakura-pink: #ffb7d5;
    --sky-blue: #a8d8ff;
    --lavender-purple: #d9c2ff;
    --mint-green: #b8f2d9;
    --cream-white: #fffaf5;
    --tech-blue: #5865f2;
    --tech-blue-light: #8fa7ff;
    --text-primary: #2d3748;
    --text-secondary: #718096;
    --card-bg: rgba(255, 255, 255, 0.72);
    --shadow-soft: 0 8px 32px rgba(88, 101, 242, 0.10);
    --shadow-hover: 0 14px 44px rgba(88, 101, 242, 0.16);
    --shadow-button: 0 6px 24px rgba(255, 111, 165, 0.30);
    --radius-xl: 28px;
    --radius-lg: 22px;
    --radius-md: 16px;
    --radius-sm: 12px;
    --transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

/* =====================================================================
   基础字体
   ===================================================================== */
* {
    .stApp {
    font-family: 'Noto Sans SC', 'Quicksand', sans-serif;
}
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
    50% { transform: translateY(-18px) rotate(3deg); }
}

@keyframes floatReverse {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(18px) rotate(-3deg); }
}

@keyframes pawWiggle {
    0%, 100% { transform: rotate(-8deg) scale(1); }
    50% { transform: rotate(8deg) scale(1.1); }
}

@keyframes pawPrint {
    0% { opacity: 0; transform: translateY(10px) scale(0.5); }
    60% { opacity: 1; transform: translateY(-5px) scale(1.1); }
    100% { opacity: 0.6; transform: translateY(0px) scale(1); }
}

@keyframes dataNodePulse {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.5); }
}

@keyframes dataLine {
    0% { width: 0%; opacity: 0; }
    30% { opacity: 0.8; }
    100% { width: 100%; opacity: 0.3; }
}

@keyframes searchPulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(88, 101, 242, 0.3); }
    50% { box-shadow: 0 0 0 15px rgba(88, 101, 242, 0); }
}

@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 200%; }
}

@keyframes fadeInUp {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes twinkle {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 1; }
}

@keyframes slideInRight {
    0% { opacity: 0; transform: translateX(-30px); }
    100% { opacity: 1; transform: translateX(0); }
}

/* =====================================================================
   页面背景：柔和马卡龙渐变呼吸动画
   ===================================================================== */
.stApp {
    background: linear-gradient(135deg, #fff7fb 0%, #f1f8ff 25%, #e6f3ff 50%, #fff7fb 100%);
    background-size: 400% 400%;
    animation: gradientShift 20s ease infinite;
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
   漂浮装饰色块（背景层）
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
    filter: blur(80px);
    opacity: 0.28;
}

.blob-pink  { width: 300px; height: 300px; background: var(--sakura-pink);   top: 5%;  left: -5%;  animation: float 12s ease-in-out infinite; }
.blob-blue  { width: 260px; height: 260px; background: var(--sky-blue);       top: 30%; right: -6%;  animation: floatReverse 10s ease-in-out infinite; animation-delay: 1s; }
.blob-purple{ width: 220px; height: 220px; background: var(--lavender-purple);bottom: 10%; left: 10%; animation: float 14s ease-in-out infinite; animation-delay: 3s; }
.blob-mint  { width: 200px; height: 200px; background: var(--mint-green);     bottom: 25%; right: 15%; animation: floatReverse 11s ease-in-out infinite; animation-delay: 2s; }

/* =====================================================================
   标题层级字体
   ===================================================================== */
h1 {
    font-family: 'Noto Sans SC', sans-serif !important;
    background: linear-gradient(135deg, #ff6fa5 0%, #8fa7ff 50%, #5865f2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem !important;
    font-weight: 700 !important;
    text-align: center;
    margin-bottom: 0.3rem !important;
    letter-spacing: 2px;
}

h2 {
    font-family: 'Noto Sans SC', sans-serif !important;
    color: var(--tech-blue);
    font-size: 1.5rem !important;
    font-weight: 600 !important;
}

h3 {
    font-family: 'Quicksand', 'Noto Sans SC', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text-primary);
}

/* =====================================================================
   Hero 区域：猫咪主题首页
   ===================================================================== */
.hero-wrapper {
    position: relative;
    text-align: center;
    padding: 2.5rem 1.5rem 2rem 1.5rem;
    margin-bottom: 1.5rem;
    background: var(--card-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-soft);
    overflow: hidden;
}

/* Hero 内的数据轨迹装饰线 */
.hero-data-trail {
    position: absolute;
    top: 50%;
    left: 5%;
    width: 90%;
    height: 2px;
    background: linear-gradient(90deg,
        transparent,
        rgba(168, 216, 255, 0.5) 20%,
        rgba(255, 183, 213, 0.5) 40%,
        rgba(88, 101, 242, 0.4) 60%,
        rgba(217, 194, 255, 0.5) 80%,
        transparent
    );
    animation: dataLine 3s ease-out forwards;
    opacity: 0.3;
    pointer-events: none;
}

/* 数据节点：漂浮在 Hero 区域的装饰小圆点 */
.hero-data-node {
    position: absolute;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    pointer-events: none;
    animation: dataNodePulse 2.5s ease-in-out infinite;
}

.node-1 { top: 18%; left: 12%; background: var(--sakura-pink);   animation-delay: 0s;   width: 6px; height: 6px; }
.node-2 { top: 25%; right: 15%; background: var(--sky-blue);     animation-delay: 0.5s; }
.node-3 { top: 60%; left: 8%;  background: var(--lavender-purple);animation-delay: 1s;   width: 7px; height: 7px; }
.node-4 { top: 55%; right: 10%; background: var(--mint-green);   animation-delay: 1.5s; width: 5px; height: 5px; }
.node-5 { top: 35%; left: 50%; background: var(--tech-blue);     animation-delay: 0.8s; width: 6px; height: 6px; }
.node-6 { top: 70%; left: 25%; background: var(--sakura-pink);   animation-delay: 2s;   width: 5px; height: 5px; }
.node-7 { top: 15%; right: 35%; background: var(--sky-blue);     animation-delay: 1.2s; width: 7px; height: 7px; }

/* Hero 搜索脉冲圈 */
.hero-search-pulse {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: 2px solid rgba(88, 101, 242, 0.2);
    animation: searchPulse 3s ease-in-out infinite;
    pointer-events: none;
}

/* 猫咪爪印漂浮 */
.hero-paw {
    position: absolute;
    font-size: 1.5rem;
    pointer-events: none;
    animation: pawPrint 4s ease-in-out infinite;
    opacity: 0.5;
}

.paw-1 { top: 12%; left: 22%; animation-delay: 0s; }
.paw-2 { top: 20%; right: 20%; animation-delay: 1.2s; }
.paw-3 { top: 65%; left: 15%; animation-delay: 2.4s; }

/* Hero 副标题 */
.hero-subtitle {
    text-align: center;
    color: var(--text-secondary);
    font-size: 1.05rem;
    font-weight: 400;
    margin-top: 0.3rem;
    margin-bottom: 1rem;
    letter-spacing: 0.5px;
}

/* =====================================================================
   玻璃拟态卡片
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
    transform: translateY(-2px);
}

/* 卡片标题 */
.card-header {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, rgba(255, 111, 165, 0.10) 0%, rgba(88, 101, 242, 0.10) 100%);
    padding: 0.5rem 1.2rem;
    border-radius: 50px;
    margin-bottom: 1.2rem;
    color: var(--tech-blue);
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: 0.5px;
}

/* =====================================================================
   Radio 选择卡片：将默认 Radio 改造成小型选择卡片
   ===================================================================== */

/* Radio 组容器：flex 横向排列 */
[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 10px !important;
}

/* 每个 Radio 选项：卡片样式 */
[data-testid="stRadio"] label {
    background: rgba(255, 255, 255, 0.65) !important;
    border: 2px solid rgba(168, 216, 255, 0.30) !important;
    border-radius: 20px !important;
    padding: 10px 20px !important;
    transition: var(--transition) !important;
    cursor: pointer !important;
    margin: 0 !important;
    font-weight: 500 !important;
    color: var(--text-primary) !important;
    font-size: 0.92rem !important;
}

/* Radio 圆形按钮缩小并美化 */
[data-testid="stRadio"] label > div:first-child > div {
    width: 16px !important;
    height: 16px !important;
    border-color: var(--sky-blue) !important;
}

/* Hover 效果 */
[data-testid="stRadio"] label:hover {
    background: rgba(168, 216, 255, 0.22) !important;
    border-color: var(--tech-blue) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 24px rgba(88, 101, 242, 0.14) !important;
}

/* 选中状态：渐变背景 */
[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, rgba(168, 216, 255, 0.45), rgba(217, 194, 255, 0.45)) !important;
    border-color: var(--tech-blue) !important;
    box-shadow: 0 2px 12px rgba(88, 101, 242, 0.22) !important;
    font-weight: 700 !important;
}

/* Radio 标签文字 */
[data-testid="stRadio"] label p {
    font-size: 0.92rem !important;
    font-weight: inherit !important;
}

/* Radio 间隔标签样式 */
.radio-label-icon {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-weight: 600;
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-bottom: 0.3rem;
}

/* =====================================================================
   文本输入框样式
   ===================================================================== */
.stTextInput div[data-baseweb="base-input"],
.stTextArea div[data-baseweb="textarea"],
div[data-testid="stTextInput"] > div,
div[data-testid="stTextArea"] > div {
    background-color: #ffffff !important;
    background: #ffffff !important;
    border: 1px solid rgba(168, 216, 255, 0.5) !important;
    border-radius: 14px !important;
}

/* 2. 覆盖内部真正用于输入的 input 和 textarea */
.stTextInput input,
.stTextArea textarea {
    background-color: #ffffff !important;
    background: #ffffff !important;
    color: #2d3748 !important;
}

/* 3. 选中/获得焦点时保持纯白背景，加亮边框 */
.stTextInput div[data-baseweb="base-input"]:focus-within,
.stTextArea div[data-baseweb="textarea"]:focus-within {
    background-color: #ffffff !important;
    border-color: #5865f2 !important;
    box-shadow: 0 0 0 3px rgba(88, 101, 242, 0.15) !important;
}
/* =====================================================================
   按钮样式：渐变 + 流光 + 悬浮动画
   ===================================================================== */
.stButton > button {
    background: linear-gradient(135deg, #ff6fa5 0%, #8fa7ff 50%, #5865f2 100%) !important;
    background-size: 200% 200% !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    height: 52px !important;
    padding: 0 2.8rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 6px 24px rgba(255, 111, 165, 0.30) !important;
    transition: var(--transition) !important;
    animation: gradientShift 4s ease infinite !important;
    position: relative !important;
    overflow: hidden !important;
}

/* 流光动画 */
.stButton > button::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 60%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.35), transparent);
    transform: skewX(-25deg);
    animation: shimmer 2.5s ease-in-out infinite;
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.03) !important;
    box-shadow: 0 12px 32px rgba(255, 111, 165, 0.40) !important;
}

.stButton > button:active {
    transform: translateY(0) scale(0.97) !important;
}

/* =====================================================================
   终端日志窗口：浅色 terminal 风格
   ===================================================================== */
.terminal-window {
    background: rgba(255, 255, 255, 0.78);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(168, 216, 255, 0.35);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    margin: 1rem 0 1.5rem 0;
    box-shadow: var(--shadow-soft);
}

.terminal-window [data-testid="stText"] {
    font-family: 'Courier New', 'Source Code Pro', 'Consolas', monospace !important;
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
   数据宝箱卡片
   ===================================================================== */
.treasure-card {
    border: 2px solid rgba(255, 183, 213, 0.4) !important;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.80), rgba(255, 240, 247, 0.70)) !important;
    animation: fadeInUp 0.7s ease-out !important;
}

.treasure-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--tech-blue);
    margin-bottom: 1.2rem;
}

.treasure-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.treasure-stat-item {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(168, 216, 255, 0.25);
    border-radius: 50px;
    padding: 0.5rem 1.2rem;
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text-primary);
}

.treasure-stat-value {
    font-weight: 700;
    color: var(--tech-blue);
    font-size: 1.1rem;
}

/* =====================================================================
   URL 展示区域
   ===================================================================== */
.url-display {
    background: rgba(168, 216, 255, 0.12) !important;
    border: 1px solid rgba(168, 216, 255, 0.25) !important;
    border-radius: 12px !important;
    padding: 0.7rem 1rem !important;
    font-size: 0.85rem !important;
    color: var(--text-secondary) !important;
    word-break: break-all !important;
    font-family: 'Courier New', monospace !important;
    margin: 0.5rem 0 0.8rem 0 !important;
}

/* =====================================================================
   提示信息 / 状态徽章
   ===================================================================== */
.stAlert {
    border-radius: var(--radius-md) !important;
    border: none !important;
    box-shadow: var(--shadow-soft) !important;
}

/* 成功消息 */
div[data-testid="stAlert"][kind="success"] {
    background: rgba(184, 242, 217, 0.3) !important;
    border: 1px solid rgba(184, 242, 217, 0.6) !important;
}

/* 错误消息 */
div[data-testid="stAlert"][kind="error"] {
    background: rgba(255, 183, 213, 0.25) !important;
    border: 1px solid rgba(255, 183, 213, 0.5) !important;
}

/* =====================================================================
   分隔线
   ===================================================================== */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(88, 101, 242, 0.15), transparent) !important;
    margin: 1.5rem 0 !important;
}

/* =====================================================================
   下载按钮覆盖样式
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
/* 修复 stStatus 图标与文字重叠问题 */
[data-testid="stStatus"] [data-testid="stIcon"] {
    font-family: inherit !important; /* 允许图标字体正常工作 */
    margin-right: 0.5rem !important;
}

[data-testid="stStatus"] summary {
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}
/* =====================================================================
   响应式适配
   ===================================================================== */
@media (max-width: 768px) {
    h1 {
        font-size: 2rem !important;
    }
    .hero-wrapper {
        padding: 1.5rem 1rem 1.2rem 1rem;
    }
    .glass-card {
        padding: 1.2rem 1rem;
    }
    .stButton > button {
        height: 46px !important;
        padding: 0 1.8rem !important;
        font-size: 0.95rem !important;
    }
    [data-testid="stRadio"] label {
        padding: 8px 14px !important;
        font-size: 0.85rem !important;
    }
    .treasure-stats {
        flex-direction: column;
        gap: 0.6rem;
    }
}

@media (max-width: 480px) {
    .block-container {
        padding: 0.8rem 0.5rem !important;
    }
    h1 {
        font-size: 1.6rem !important;
    }
    .card-header {
        font-size: 1.1rem !important;
    }
    .stButton > button {
        height: 44px !important;
        padding: 0 1.5rem !important;
        font-size: 0.9rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 背景漂浮装饰色块
# =============================================================================
st.markdown("""
<div class="floating-decorations">
    <div class="floating-blob blob-pink"></div>
    <div class="floating-blob blob-blue"></div>
    <div class="floating-blob blob-purple"></div>
    <div class="floating-blob blob-mint"></div>
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
# 🎨 Hero 区域：猫咪 AI 求职助手主题首页
# =============================================================================
st.markdown('</div>', unsafe_allow_html=True)
st.title("爬虫喵 · 漏网之喵")
st.markdown(
    '<p class="hero-subtitle">🐱 有恃无恐，随心而喵；不拘喵规，萌混过关 </p>',
    unsafe_allow_html=True
)
st.markdown('<p class="hero-subtitle"></p>', unsafe_allow_html=True)

# =============================================================================
# 🐾 Card 1: 搜索中心
# =============================================================================
st.markdown('<div class="card-header"> 🔎 检索中心</div>', unsafe_allow_html=True)

selected_query = st.text_input(
    "请输入岗位检索词",
    key="search_query_input",
    placeholder="例如：Python工程师、产品经理、UI设计师..."
)

st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# ⚙️ Card 2: 捕猎参数配置
# =============================================================================
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card-header">⚙️ 参数配置</div>', unsafe_allow_html=True)

# ---- 第一行：城市、类型、薪资、经验、学历、规模 ----
col1, col2, col3,col4, col5, col6 = st.columns([1,1,1.1,1.1,1,1.1])
with col1:
    st.markdown('<span class="radio-label-icon">🏙️ 城市期望</span>', unsafe_allow_html=True)
    selected_city = st.radio(
        "城市期望",
        ["北京", "上海", "广州", "深圳", "杭州"],
        key="city_radio",
        label_visibility="collapsed"
    )
with col2:
    st.markdown('<span class="radio-label-icon">💼 类型期望</span>', unsafe_allow_html=True)
    selected_jobtype = st.radio(
        "类型期望",
        ["不限", "实习", "兼职", "全职"],
        key="jobtype_radio",
        label_visibility="collapsed"
    )
with col3:
    st.markdown('<span class="radio-label-icon">💰 薪资期望</span>', unsafe_allow_html=True)
    selected_salary = st.radio(
        "薪资期望",
        ["不限", "3-5K", "5-10K", "10-20K"],
        key="salary_radio",
        label_visibility="collapsed"
    )
with col4:
    st.markdown('<span class="radio-label-icon">🎓 经验期望</span>', unsafe_allow_html=True)
    selected_experience = st.radio(
        "经验期望",
        ["不限", "在校生", "应届生", "经验不限"],
        key="experience_radio",
        label_visibility="collapsed"
    )
with col5:
    st.markdown('<span class="radio-label-icon">📚 学历期望</span>', unsafe_allow_html=True)
    selected_degree = st.radio(
        "学历期望",
        ["不限", "大专", "本科", "硕士"],
        key="degree_radio",
        label_visibility="collapsed"
    )
with col6:
    st.markdown('<span class="radio-label-icon">🏢 规模期望</span>', unsafe_allow_html=True)
    selected_scale = st.radio(
        "规模期望",
        ["不限", "0-20人","20-99人","100-499人"],
        key="scale_radio",
        label_visibility="collapsed"
    )

st.divider()

st.markdown('</div>', unsafe_allow_html=True)
# =============================================================================
# 🚀 Card 3: 猫爪采集中心
# =============================================================================
st.markdown('<div class="card-header"> 🕸️ 采集中心</div>', unsafe_allow_html=True)

# 生成目标 URL
url = get_url(
    selected_city, selected_jobtype, selected_salary,
    selected_experience, selected_degree, selected_scale,
    selected_query
)

st.markdown("🔗 目标采集网址：")
st.markdown(f'<div class="url-display">{url}</div>', unsafe_allow_html=True)

selected_url = st.text_area(
    "若以上网址并非您要爬取的网址，请在此输入正确网址：",
    key="custom_url_input",
    placeholder="域名需以：https://www.zhipin.com/web/geek/jobs 开头，且必须要有检索词内容"
)
exe_path= st.text_area(
    "请填写浏览器的绝对路径（可选择edg.exe 或 Chrome.exe）：",
    key="custom_exe_input",
    placeholder="例如：C:\Program Files\Google\Chrome\Application\chrome.exe"
)

# 提交按钮居中
btn_col1, btn_col2, btn_col3 = st.columns([1.2, 1, 1])
with btn_col2:
    submit = st.button("开始采集 🐾", key="start_crawl_button")

st.divider()
st.divider()


# =============================================================================
# 🐾 爬取逻辑（保留原有业务逻辑，仅优化文案与视觉）
# =============================================================================
scrapy=False
if submit:
    if exe_path:
        scrapy=True
    else:
        scrapy=False
        st.error("请填写浏览器的绝对路径喵~")

if scrapy:
    # 若用户输入了自定义 URL，则替换
    if selected_url:
        url = selected_url

    # 终端风格日志窗口
    with st.status("🐾 正在寻找岗位猎物...", expanded=True) as status:
        placeholder = st.empty()
        logs = []

        def log(message):
            """实时日志回调：将爬虫进度消息追加到终端窗口"""
            logs.append(message)
            placeholder.text("\n".join(logs))

        try:
            jobs_info = get_job_information(url,log,exe_path)
            status.update(label="捕猎完成喵！", state="complete", expanded=True)
            st.success("🎉 爬取工作已完成，记得下载岗位数据喵。")
            download = True
        except Exception:
            st.error("😭 这次没有找到目标喵，请检查路径或条件是否正确。")
            status.update(label="捕猎失败喵~", state="error", expanded=True)
            download = False

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # 📦 Card 4: 数据宝箱（仅在爬取成功后显示）
    # =========================================================================
    st.divider()
    if download:
        st.markdown('<div class="card-header">📦 数据宝箱</div>', unsafe_allow_html=True)
        # 统计岗位数量
        if isinstance(jobs_info, list):
            job_count = len(jobs_info)
        elif isinstance(jobs_info, dict):
            job_count = len(jobs_info)
        else:
            job_count = "—"

        # 统计信息展示
        st.markdown(f"""
        <div class="treasure-stats">
            <div class="treasure-stat-item">
                🎯 本次发现：<span class="treasure-stat-value">{job_count}</span> 个岗位
            </div>
            <div class="treasure-stat-item">
                🌐 来源：招聘网站
            </div>
            <div class="treasure-stat-item">
                📋 格式：JSON
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 序列化 JSON 数据
        json_data = json.dumps(
            jobs_info,
            ensure_ascii=False,
            indent=4
        )

        # 下载按钮
        st.download_button(
            label="📥 下载岗位数据",
            data=json_data,
            file_name="职位信息.json",
            mime="application/json",
            key="download_jobs_button"
        )

        st.markdown('</div>', unsafe_allow_html=True)