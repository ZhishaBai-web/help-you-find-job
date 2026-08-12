import streamlit as st
from resume_portrait_keywords_ai import get_resume_text2
from resume_portrait_keywords_ai import get_resume_refine
from resume_portrait_keywords_ai import get_json_portrait
from resume_portrait_keywords_ai import get_report
from resume_portrait_keywords_ai import get_keywork
from resume_portrait_keywords_ai import get_ai_response



# =============================================================================
# 全局样式注入：马卡龙科技感主题
# 包含字体、动画、玻璃拟态卡片、表单、按钮、标签页、聊天区域等视觉样式
# =============================================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Quicksand:wght@400;500;600;700&family=ZCOOL+KuaiLe&display=swap" rel="stylesheet">

<style>
/* ========== 设计令牌（Design Tokens） ========== */
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
    --bg-warm: #fff7fb;
    --bg-cool: #f1f8ff;
    --card-bg: rgba(255, 255, 255, 0.78);
    --shadow-soft: 0 8px 32px rgba(88, 101, 242, 0.12);
    --shadow-hover: 0 12px 40px rgba(88, 101, 242, 0.18);
    --radius-lg: 24px;
    --radius-md: 16px;
    --radius-sm: 12px;
    --transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ========== 基础字体与全局过渡 ========== */
* {
    font-family: 'Noto Sans SC', 'Quicksand', sans-serif ;
}

/* ========== 关键帧动画 ========== */
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


/* ========== 页面背景：柔和马卡龙渐变呼吸动画 ========== */
.stApp {
    background: linear-gradient(135deg, #fff7fb 0%, #f1f8ff 25%, #e6f3ff 50%, #fff7fb 100%);
    background-size: 400% 400%;
    animation: gradientShift 18s ease infinite;
    color: var(--text-primary);
}

/* ========== 漂浮装饰色块（背景层） ========== */
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
    animation: float 10s ease-in-out infinite;
}

.blob-1 { width: 320px; height: 320px; background: var(--macaron-pink); top: 8%; left: -6%; animation-delay: 0s; }
.blob-2 { width: 280px; height: 280px; background: var(--macaron-blue); top: 38%; right: -6%; animation-delay: 2s; animation-name: floatReverse; }
.blob-3 { width: 240px; height: 240px; background: var(--macaron-purple); bottom: 12%; left: 12%; animation-delay: 4s; }
.blob-4 { width: 200px; height: 200px; background: var(--macaron-mint); bottom: 28%; right: 18%; animation-delay: 1s; animation-name: floatReverse; }

/* 确保内容层位于装饰色块之上 */
.block-container {
    position: relative;
    z-index: 1;
}

/* ========== 标题层级字体 ========== */
h1 {
    font-family: 'Noto Sans SC', sans-serif !important;
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


/* ========== 玻璃拟态卡片 ========== */
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
}

.glass-card:hover {
    box-shadow: var(--shadow-hover);
    transform: translateY(-3px);
}


/* ========== 分区标题 pill ========== */
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

/* ========== 文件上传区样式修正 ========== */
[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.6) !important;
    border: 2px dashed rgba(88, 101, 242, 0.3) !important;
    border-radius: var(--radius-md) !important;
    padding: 1.5rem !important;
    transition: var(--transition) !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--tech-blue) !important;
    background: rgba(255, 255, 255, 0.85) !important;
    box-shadow: 0 0 0 4px rgba(88, 101, 242, 0.1) !important;
}

/* 仅对“未选择文件时”的主上传按钮生效 */
[data-testid="stFileUploader"] section button {
    background: linear-gradient(135deg, var(--macaron-pink) 0%, var(--macaron-blue) 100%) !important;
    color: white !important;
    border-radius: 50px !important;
    border: none !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    transition: var(--transition) !important;
    position: relative !important;
    font-size: 14px !important;
}


/* 💥 核心修复：隐藏已上传文件列表卡片内部被误伤的小按钮/二次上传按钮 */
[data-testid="stFileUploaderFile"] button,
[data-testid="stFileUploaderDeleteBtn"] {
    display: none !important;
}

/* ========== 按钮：渐变+流光+悬浮动画 ========== */
.stButton > button {
    background: linear-gradient(135deg, #ff6fa5 0%, #8fa7ff 50%, #5865f2 100%);
    background-size: 200% 200%;
    color: white;
    border: none;
    border-radius: 50px;
    height: 50px;
    padding: 0 2.5rem;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    box-shadow: 0 6px 20px rgba(88, 101, 242, 0.25);
    transition: var(--transition);
    animation: gradientShift 4s ease infinite;
    position: relative;
    overflow: hidden;
}

.stButton > button::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: 0.5s;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 10px 28px rgba(88, 101, 242, 0.35);
}

.stButton > button:hover::after {
    left: 100%;
}

.stButton > button:active {
    transform: translateY(0) scale(0.98);
}

/* ========== 标签页：胶囊式导航 ========== */
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
    padding: 0.6rem 1.2rem 0.6rem 1.2rem !important;
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

原因在于你的代码中同时存在两套互相冲突的样式规则：

一套是在 .stChatInputContainer textarea 上加了边框和圆角；

另一套是在 [data-testid="stChatInput"] 外层容器上也加了 border: 1.5px solid ... 以及 box-shadow。

当内层背景变成纯白且内缩时，外层容器自带的那个带紫色边框/阴影的盒子就被“套”在外面，形成双重边框和紫光。

🛠️ 修改后的完整 CSS 代码
请直接使用以下清洗整合后的代码，完全替换你提供的这段 CSS 即可：

CSS
/* ========== 聊天区域 ========== */
.chat-container {
    background: var(--card-bg);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow-soft);
}

/* 取消底部固定吸附，改为页面内普通流式布局 */
[data-testid="stBottom"] {
    position: relative !important;
    bottom: auto !important;
    background: transparent !important;
    padding: 0 !important;
}

.stChatInputContainer {
    position: relative !important;
    margin-top: 1rem !important;
    background: transparent !important;
}

/* 💥 外层外壳：承载纯白背景、圆角和外层细边框 💥 */
[data-testid="stChatInput"],
div[class*="stChatInputContainer"] {
    background-color: #ffffff !important;
    border: 1.5px solid rgba(88, 101, 242, 0.2) !important;
    border-radius: 20px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
}

/* 💥 中间层与背景层：透出纯白，干掉所有中间层边框 💥 */
[data-testid="stChatInput"] *,
div[data-baseweb="input"],
div[data-baseweb="base-input"] {
    background-color: transparent !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* 💥 核心：彻底抹除最内层 textarea 的蓝色内框与 Focus 边框 💥 */
.stChatInputContainer textarea,
[data-testid="stChatInput"] textarea {
    background-color: transparent !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    padding: 0.8rem 1.2rem !important;
}

/* 聚焦（点击输入）时，只高亮最外层的大框，内部无任何变动 */
[data-testid="stChatInput"]:focus-within {
    border-color: var(--tech-blue) !important;
    box-shadow: 0 0 0 3px rgba(88, 101, 242, 0.12) !important;
}

.stChatMessage {
    background: transparent !important;
    padding: 0.8rem 0 !important;
}

.stChatMessage [data-testid="chatMessageContent"] {
    border-radius: 20px;
    padding: 1rem 1.2rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
    border: 1px solid rgba(88, 101, 242, 0.08);
}

/* AI 消息气泡 */
.stChatMessage[data-testid="chatMessage"][name="ai"] [data-testid="chatMessageContent"] {
    background: linear-gradient(135deg, #fff0f7 0%, #f1f8ff 100%);
    border: 1px solid rgba(255, 111, 165, 0.15);
}

/* 用户消息气泡 */
.stChatMessage[data-testid="chatMessage"][name="human"] [data-testid="chatMessageContent"] {
    background: linear-gradient(135deg, #f1f8ff 0%, #e8ecff 100%);
    border: 1px solid rgba(88, 101, 242, 0.15);
}

/* ========== 加载动画与分隔线 ========== */
.stSpinner > div {
    border-color: var(--tech-blue) transparent transparent transparent !important;
}

hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(88, 101, 242, 0.2), transparent) !important;
    margin: 2rem 0 !important;
}

/* ========== 结果内容区 ========== */
.result-content {
    background: rgba(255, 255, 255, 0.6);
    border-radius: var(--radius-md);
    padding: 1.2rem;
    border: 1px solid rgba(88, 101, 242, 0.08);
    line-height: 1.7;
}
/* ========== 强行抹除 Tabs 标签页底部红线/指示线 ========== */

/* 1. 核心：通过 clip-path 裁切掉高亮下划线，彻底抹除视觉渲染 */
[data-baseweb="tab-highlight-tile"],
[data-baseweb="tab-border"],
[data-baseweb="tab-highlight"] {
    clip-path: inset(100%) !important;
    background: transparent !important;
    border: none !important;
    visibility: hidden !important;
}

/* 2. 覆盖所有通用 BaseWeb Tab 下方可能出现的 Border 线条 */
[data-baseweb="tab-list"],
.stTabs [role="tablist"] {
    border-bottom: none !important;
    background: rgba(255, 255, 255, 0.5) !important;
}

.stTabs [role="tab"] {
    border: none !important;
    border-bottom: none !important;
}

/* 3. 避免选中的 Tab 产生任何模拟的底部 Box-Shadow 线条 */
.stTabs [aria-selected="true"] {
    border: none !important;
    border-bottom: none !important;
    background: linear-gradient(135deg, var(--tech-blue) 0%, #8fa7ff 100%) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(88, 101, 242, 0.25) !important;
}

/* ========== 1. 消除顶部白条 ========== */
/* 隐藏 Streamlit 默认顶部 header 的白底背景，并设为透明 */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* 消除主内容区域顶部默认的空白边距 (padding-top) */
.main .block-container {
    padding-top: 2rem !important; /* 根据需要可调整为 0rem 或 1rem */
}


/* ========== 2. 消除底部聊天框白条 ========== */
/* 核心：将底部聊天输入框外层的固定容器背景设为透明 */
[data-testid="stBottom"] {
    background: transparent !important;
}

/* 如果使用的是旧版 Streamlit，补充覆盖底部 wrapper 的背景 */
div[data-testid="stBottom"] > div {
    background: transparent !important;
}

/* ========== 响应式适配 ========== */
@media (max-width: 768px) {
    h1 { font-size: 2rem !important; }
    .hero-card { padding: 1.5rem 1rem; }
    .glass-card { padding: 1.2rem; }
    .stTabs [role="tab"] {
        font-size: 0.85rem !important;
        padding: 0.5rem 0.8rem !important;
    }
    .stButton > button {
        height: 46px;
        padding: 0 1.5rem;
        font-size: 0.9rem;
    }
}

@media (max-width: 480px) {
    .block-container { padding: 1rem 0.8rem; }
    h2 { font-size: 1.3rem !important; }
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

/* 侧边栏标题：居中样式 */
.sidebar-title {
    font-family: 'ZCOOL KuaiLe', sans-serif !important;
    color: var(--tech-blue);
    font-size: 1.2rem;
    margin-top: 0.5rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: center; /* 水平居中 */
    text-align: center;      /* 文字居中 */
    gap: 0.4rem;
}

/* 状态标签 / 徽章 */
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
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 选项款颜色
# =============================================================================
st.markdown("""
<style>
/* ========== 彻底修改选项框/下拉框背景与圆角，使其保持一致 ========== */

/* 1. 统一单选框（stSelectbox）与多选框（stMultiSelect）的外层容器圆角、背景和边框 */
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stMultiSelect"] > div > div,
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid rgba(88, 101, 242, 0.2) !important;
    border-radius: 8px !important; /* 👈 统一两者的圆角大小（可按需调整为 6px、8px、12px 等） */
}

</style>
""", unsafe_allow_html=True)

# =============================================================================
# Session State 初始化
# =============================================================================

if "file_name" not in st.session_state:
    st.session_state.file_name = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
if "resume_refine" not in st.session_state:
    st.session_state.resume_refine = None
if "json_portrait" not in st.session_state:
    st.session_state.json_portrait = None
if "user_report" not in st.session_state:
    st.session_state.user_report = None
if "keywork" not in st.session_state:
    st.session_state.keywork = None
if "messages" not in st.session_state:
    st.session_state.messages = []

if "key" not in st.session_state:
    st.session_state.key = None
if "url" not in st.session_state:
    st.session_state.url = None
if "refine_llm" not in st.session_state:
    st.session_state.refine_llm = None
if "portrait_llm" not in st.session_state:
    st.session_state.portrait_llm = None
if "report_llm" not in st.session_state:
    st.session_state.report_llm = None
if "keywork_llm" not in st.session_state:
    st.session_state.keywork_llm = None
if "ai_llm" not in st.session_state:
    st.session_state.ai_llm = None
# =============================================================================
# 侧边栏信息
# =============================================================================
st.set_page_config(
    page_title="工作喵",
    page_icon="🐱",
    layout="wide"
)


with st.sidebar:
    st.markdown('<div class="sidebar-title">🔑 API 授权配置</div>', unsafe_allow_html=True)

    key = st.text_input("API Key：", type="password", placeholder="请输入您的 Key")
    if key:
        st.markdown('<div class="status-badge status-success">✓ Key 已配置</div>', unsafe_allow_html=True)
        if key != st.session_state.key:
            st.session_state.key = key
            st.session_state.resume_refine = None
            st.session_state.json_portrait = None
            st.session_state.user_report = None
            st.session_state.keywork = None
    else:
        st.markdown('<div class="status-badge status-warning">! Key 待输入</div>', unsafe_allow_html=True)

    # 2. URL 输入区
    url = st.text_input("API URL：", placeholder="请输入 API 地址")
    if url:
        st.markdown('<div class="status-badge status-success">✓ URL 已配置</div>', unsafe_allow_html=True)
        if url != st.session_state.url:
            st.session_state.url = url
            st.session_state.resume_refine = None
            st.session_state.json_portrait = None
            st.session_state.user_report = None
            st.session_state.keywork = None
    else:
        st.markdown('<div class="status-badge status-warning">! URL 待输入</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="sidebar-title">🤖 驱动模型设置</div>', unsafe_allow_html=True)

    # 3. 各阶段模型选择
    refine_llm = st.text_input("简历精炼模型：", value="gpt-5-mini-2025-08-07",placeholder="请输入 简历精炼 模型")
    if refine_llm:
        st.markdown(f'<div class="status-badge status-info">{refine_llm}</div>', unsafe_allow_html=True)
        if refine_llm != st.session_state.refine_llm:
            st.session_state.refine_llm = refine_llm
            st.session_state.resume_refine = None
            st.session_state.json_portrait = None
            st.session_state.user_report = None
            st.session_state.keywork = None

    portrait_llm = st.text_input("画像生成模型：", value="gpt-5-2025-08-07",placeholder="请输入 画像生成 模型")
    if portrait_llm:
        st.markdown(f'<div class="status-badge status-info">{portrait_llm}</div>', unsafe_allow_html=True)
        if portrait_llm != st.session_state.portrait_llm:
            st.session_state.portrait_llm = portrait_llm
            st.session_state.resume_refine = None
            st.session_state.json_portrait = None
            st.session_state.user_report = None
            st.session_state.keywork = None

    report_llm = st.text_input("报告生成模型：", value="gpt-5-nano-2025-08-07",placeholder="请输入 报告生成 模型")
    if report_llm:
        st.markdown(f'<div class="status-badge status-info">{report_llm}</div>', unsafe_allow_html=True)
        if report_llm != st.session_state.report_llm:
            st.session_state.report_llm = report_llm
            st.session_state.resume_refine = None
            st.session_state.json_portrait = None
            st.session_state.user_report = None
            st.session_state.keywork = None

    keywork_llm = st.text_input("检索词生成模型：", value="gpt-5-nano-2025-08-07", placeholder="请输入 检索词生成 模型")
    if keywork_llm:
        st.markdown(f'<div class="status-badge status-info"> {keywork_llm}</div>', unsafe_allow_html=True)
        if keywork_llm != st.session_state.keywork_llm:
            st.session_state.keywork_llm = keywork_llm
            st.session_state.resume_refine = None
            st.session_state.json_portrait = None
            st.session_state.user_report = None
            st.session_state.keywork = None

    ai_llm = st.text_input("AI 聊天模型：", value="gpt-5-nano-2025-08-07",placeholder="请输入 AI聊天 模型")
    if ai_llm:
        st.markdown(f'<div class="status-badge status-info">💬 {ai_llm}</div>', unsafe_allow_html=True)
        if ai_llm != st.session_state.ai_llm:
            st.session_state.ai_llm = ai_llm

# =============================================================================
# 顶部 Hero 区：标题 + 简历上传
# =============================================================================

st.title("工作喵 · AI 求职助手")
st.markdown(
    '<p style="text-align:center;color:#718096;font-size:1.05rem;margin-top:0.3rem;margin-bottom:1rem;">'
    '🐱 全世界喵咪，联合起来！ </p>',
    unsafe_allow_html=True
)
st.markdown('<p class="hero-subtitle"></p>', unsafe_allow_html=True)

st.markdown('<div class="section-header"> 💾 简历上传 </div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("上传pdf简历，让工作喵帮您发现职业潜力 ✨", type=["pdf"])
file_bytes = False
if uploaded_file:
    file_bytes = uploaded_file.read()
    file_name = f"{uploaded_file.name}"
    st.markdown(f'<div class="upload-status">🐾 检查到简历：{uploaded_file.name}</div>', unsafe_allow_html=True)
    if file_name != st.session_state.file_name:
        st.session_state.file_name = file_name
        st.session_state.resume_text = None
        st.session_state.resume_refine = None
        st.session_state.json_portrait = None
        st.session_state.user_report = None
        st.session_state.keywork = None
else:
    resume_text = False

st.markdown('</div>', unsafe_allow_html=True)
st.divider()


# =============================================================================
# 问卷区：15 个小问题（保留原有逻辑）
# =============================================================================
st.markdown('<div class="section-header"> ↔️ 偏好选择</div>', unsafe_allow_html=True)

class1, class2, class3, class4, class5 = st.tabs(["🎯 职业星图","⚙️ 工作人格","🏢 理想环境","🚀 未来方向","🌈 现实边界"])

with class1:
    answer1 = st.selectbox(
        "问题1：未来3-5年，你希望自己的职业状态更接近哪一种？",
        ["成为某个领域的专业人才",
         "成为负责重要项目或团队的负责人",
         "成为连接技术、业务和资源的综合型人才",
         "探索创业或商业机会",
         "成为研究型人才（学术、科研方向）",
         "目前没有明确目标，希望通过分析寻找方向"],
        index=None
    )
    answer2 = st.multiselect(
        "问题2：你目前最希望从工作中获得什么？（最多选择3项）",
        ["持续学习和能力提升", "更高收入", "稳定的发展环境",
         "更大的自主权", "社会价值和影响力", "职业身份和认可", "更多创造和探索机会"],
        max_selections=3
    )
    answer3 = st.selectbox(
        "问题3：如果未来长期从事一种类型的工作，你更倾向？",
        ["深入研究一个专业领域", "解决复杂问题和挑战",
         "推动项目落地和产生实际价值", "与人沟通、协调资源", "发现机会并创造新的方向"],
        index=None
    )

with class2:
    answer4 = st.selectbox(
        "问题4：你更喜欢怎样解决问题？",
        ["独立分析，深入思考后解决",
         "与团队讨论，共同找到方案",
         "快速行动，通过实践不断调整",
         "制定计划，按照流程推进"],
        index=None
    )
    answer5 = st.selectbox(
        "问题5：你更享受哪类工作成果？",
        ["创造新的知识或方法", "完成复杂任务和技术突破",
         "做出实际产品或业务成果", "帮助别人解决问题",
         "建立体系、管理资源"],
        index=None
    )
    answer6 = st.selectbox(
        "问题6：你的理想工作节奏更接近？",
        ["稳定、有明确规划", "稳定但持续成长",
         "快速变化、充满挑战", "高自由度、自主安排"],
        index=None
    )

with class3:
    answer7 = st.selectbox(
        "问题7：你更喜欢什么类型的组织环境？",
        ["大平台，资源丰富、流程成熟", "中型成长企业，机会较多",
         "小团队，高自由度", "创新创业环境，变化快速", "专业研究机构"],
        index=None
    )
    answer8 = st.selectbox(
        "问题8：你希望自己在组织中的角色更偏向？",
        ["专业执行者", "核心骨干", "项目负责人", "跨部门协调者", "管理者"],
        index=None
    )
    answer9 = st.selectbox(
        "问题9：你更喜欢？",
        ["明确职责，专注自己的领域", "多领域交叉，解决综合问题",
         "从0到1探索新事情", "持续优化已有体系"],
        index=None
    )

with class4:
    answer10 = st.selectbox(
        "问题10：选择未来发展方向时，你更看重？",
        ["与已有专业背景高度相关", "利用已有优势进入新领域",
         "完全转向新的兴趣方向", "哪个方向发展机会大就考虑哪个方向"],
        index=None
    )
    answer11 = st.selectbox(
        "问题11：你更愿意在哪类问题中发挥价值？",
        ["技术创新问题", "商业经营问题", "社会公共问题",
         "行业效率提升问题", "人与组织发展问题"],
        index=None
    )
    answer12 = st.selectbox(
        "问题12：你希望未来的职业标签更接近?",
        ["某个领域专家", "综合型人才", "创新者", "管理者", "解决方案提供者"],
        index=None
    )

with class5:
    answer13 = st.multiselect(
        "问题13：你的工作地点偏好是什么？（可多选）",
        ["接受异地工作", "接受海外机会", "接受长期出差", "只考虑本地/不接受出差"]
    )
    answer14 = st.multiselect(
        "问题14：选择工作机会时，你更看重？（多选，先选的最重要）",
        ["薪资水平", "发展空间", "工作稳定性", "工作兴趣", "公司品牌", "工作生活平衡"]
    )
    answer15 = st.multiselect(
        "问题15：你明确不希望从事哪些类型的工作？",
        ["高频重复工作", "长期独立研究", "大量沟通协调", "高频出差", "强销售性质", "高压力竞争环境"]
    )
    answer16 = st.text_area("其他明确不希望从事的工作类型？（选填）", placeholder="例如：离家太远、没有加班费等...")

st.markdown('</div>', unsafe_allow_html=True)

# 提交按钮
col1, col2, col3 = st.columns([1.15, 1, 1])
with col2:
    submit = st.button("回答完成 🐾")
st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# 问卷校验与画像字符串生成（保留原有逻辑）
# =============================================================================
submit_next = False
if submit:
    answers_dict = {
        "问题1": answer1, "问题2": answer2, "问题3": answer3,
        "问题4": answer4, "问题5": answer5, "问题6": answer6,
        "问题7": answer7, "问题8": answer8, "问题9": answer9,
        "问题10": answer10, "问题11": answer11, "问题12": answer12,
        "问题13": answer13, "问题14": answer14, "问题15": answer15
    }
    unanswered = []
    for q_name, q_val in answers_dict.items():
        if q_val is None or len(q_val) == 0:
            unanswered.append(q_name)
    if unanswered:
        st.error(f"⚠️ 您还有必答题未完成，请检查以下题目：\n\n**{', '.join(unanswered)}**")
    else:
        st.success("🎉 所有必答题数据已更新，请等待分析结果生成！")
        submit_next = True

user_profile_string = False
if submit_next:
    a2_str = ",".join(answer2)
    a13_str = ",".join(answer3)
    a14_str = ",".join(answer14)
    a15_str = ",".join(answer15)
    a16_str = answer16.strip() if answer16 else "无"
    user_profile_string = f"""
    === 用户职业倾向评估问卷结果 ===
    【第一部分：职业目标】
    问题1：未来3-5年，你希望自己的职业状态更接近哪一种？回答：{answer1}
    问题2：你目前最希望从工作中获得什么？（最多选择3项）回答：{a2_str}
    问题3：如果未来长期从事一种类型的工作，你更倾向？回答：{answer3}
    【第二部分：工作方式偏好】
    问题4：你更喜欢怎样解决问题？回答：{answer4}
    问题5：你更享受哪类工作成果？回答：{answer5}
    问题6：你的理想工作节奏更接近？回答：{answer6}
    【第三部分：组织环境偏好】
    问题7：你更喜欢什么类型的组织环境？回答：{answer7}
    问题8：你希望自己在组织中的角色更偏向？回答：{answer8}
    问题9：你更喜欢？回答：{answer9}
    【第四部分：行业和方向偏好】
    问题10：选择未来发展方向时，你更看重？回答：{answer10}
    问题11：你更愿意在哪类问题中发挥价值？回答：{answer11}
    问题12：你希望未来的职业标签更接近？回答：{answer12}
    【第五部分：现实约束】
    问题13：你的工作地点偏好是什么？（可多选）回答：{a13_str}
    问题14：选择工作机会时，你更看重？（多选，先选的最重要）回答：{a14_str}
    问题15：你明确不希望从事哪些类型的工作？回答：{a15_str}
    其他明确不希望从事的工作类型？（选填）回答：{a16_str}
    =================================
    """
    st.session_state.json_portrait = None
    st.session_state.keywork = None

st.divider()


# =============================================================================
# 结果输出区：简历文本 / 简历精炼 / 用户画像 / 检索词推荐
# =============================================================================
st.markdown('<div class="section-header"> 📊 分析结果 </div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4,tab5 = st.tabs(["📝 简历扫码","⚗️ 简历精馏","🖼️ JSON 画像","📑 职场报告","🔍 岗位检索词"])

with tab1:
    if file_bytes and st.session_state.resume_text is None:
        with st.spinner("简历正在扫码，请稍等..."):
            st.session_state.resume_text = get_resume_text2(file_bytes)
            st.write(st.session_state.resume_text)
            st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.resume_text:
        st.write(st.session_state.resume_text)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="upload-status">📎 简历未上传</div>', unsafe_allow_html=True)

with tab2:
    if st.session_state.resume_text and st.session_state.resume_refine is None and user_profile_string:
        with st.spinner("简历正在精炼，请稍等..."):
            if st.session_state.resume_text=="扫描结果为空，请重新上传 pdf。注意：pdf 需为具有文本块的 pdf，而非只有图片块。":
                st.session_state.resume_refine = "简历扫描结果为空，精馏失败。"
                st.session_state.json_portrait = "简历扫描结果为空，Json 画像生成失败。"
                st.session_state.user_report ="简历扫描结果为空，职场画像生成失败。"
                st.session_state.keywork ="简历扫描结果为空，岗位检索词生成失败。"
            else:
                try:
                    st.session_state.resume_refine = get_resume_refine(st.session_state.resume_text,key,url,refine_llm)
                except:
                    st.session_state.resume_refine = "请检查key、url、简历精炼模型是否输入正确。"
                    st.session_state.json_portrait = "请检查key、url、简历精炼模型是否输入正确。"
                    st.session_state.user_report = "请检查key、url、简历精炼模型是否输入正确。"
                    st.session_state.keywork = "请检查key、url、简历精炼模型是否输入正确。"
            st.write(st.session_state.resume_refine)
            st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.resume_refine:
        st.write(st.session_state.resume_refine)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="upload-status">📎 简历未上传 or 15 个小问题未答完</div>', unsafe_allow_html=True)

with tab3:
    if st.session_state.resume_refine and st.session_state.json_portrait is None and user_profile_string:
        with st.spinner("JSON 画像正在生成，请稍等..."):
            try:
                st.session_state.json_portrait = get_json_portrait(st.session_state.resume_refine, user_profile_string,key,url,portrait_llm)
            except:
                st.session_state.json_portrait="请检查key、url、画像生成模型是否输入正确。"
                st.session_state.user_report = "请检查key、url、画像生成模型是否输入正确。"
                st.session_state.keywork = "请检查key、url、画像生成模型是否输入正确。"
            st.write(st.session_state.json_portrait)
            st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.json_portrait:
        st.write(st.session_state.json_portrait)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="upload-status">📎 简历未上传 or 15 个小问题未答完</div>', unsafe_allow_html=True)

with tab4:
    if st.session_state.resume_refine and st.session_state.user_report is None and user_profile_string:
        with st.spinner("职场报告正在生成，请稍等..."):
            try:
                st.session_state.user_report = get_report(st.session_state.json_portrait,key,url,report_llm)
            except:
                st.session_state.user_report = "请检查key、url、报告生成模型是否输入正确。"
                st.session_state.keywork = "请检查key、url、报告生成模型是否输入正确。"
            st.write(st.session_state.user_report)
            st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.user_report:
        st.write(st.session_state.user_report)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="upload-status">📎 简历未上传 or 15 个小问题未答完</div>', unsafe_allow_html=True)

with tab5:
    if st.session_state.json_portrait and st.session_state.keywork is None:
        with st.spinner("检索词正在生成，请稍等..."):
            try:
                st.session_state.keywork = get_keywork(st.session_state.json_portrait,key,url,keywork_llm)
            except:
                st.session_state.keywork = "请检查key、url、检索词生成模型是否输入正确。"
            st.write(st.session_state.keywork)
            st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.json_portrait:
        st.write(st.session_state.keywork)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="upload-status">📎 简历未上传 or 15 个小问题未答完</div>', unsafe_allow_html=True)

st.divider()


# =============================================================================
# 聊天喵区：AI 对话交互
# =============================================================================
st.markdown('<div class="section-header">💬 聊天喵</div>', unsafe_allow_html=True)


if st.session_state["messages"] == []:
    st.session_state["messages"] = [
        {"role": "ai", "content": "您好，我是聊天喵，让我们开始聊天喵~（由于猫粮短缺，可别指望本喵有记忆哦！）"}
    ]

for message in st.session_state["messages"]:
    st.chat_message(message["role"], avatar="🐱" if message["role"] == "ai" else "😏").write(message["content"])

question = st.chat_input()

if question:
    st.session_state["messages"].append({"role": "human", "content": question})
    st.chat_message("human", avatar="😏").write(question)

    with st.spinner("聊天喵正在思考，请稍等..."):
        try:
            response = get_ai_response(question, st.session_state.user_report,key, url,ai_llm)
        except:
            response = "请检查key、url、ai聊天模型是否输入正确喵。"
    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai", avatar="🐱").write(response)

st.markdown('</div>', unsafe_allow_html=True)
