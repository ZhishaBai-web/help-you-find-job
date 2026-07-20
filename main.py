import streamlit as st
from get_short_resume_info import get_resume_info1
from get_short_resume_info import get_resume_info2
from get_short_resume_info import get_resume_info3
from get_short_resume_info import get_resume_info4
from get_short_resume_info import get_resume_info5
from get_short_resume_info import get_resume_info6

if "file_hash" not in st.session_state:
    st.session_state.file_hash = None
if "resume_content" not in st.session_state:
    st.session_state.resume_content = None
if "resume_refine" not in st.session_state:
    st.session_state.resume_refine = None
if "json_portrait" not in st.session_state:
    st.session_state.json_portrait = None
if "user_portrait" not in st.session_state:
    st.session_state.user_portrait = None
if "search_key" not in st.session_state:
    st.session_state.search_key = None
if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("AI 帮你找工作 💡")
uploaded_file=st.file_uploader("请上传您的PDF简历",type=["pdf"])
file_bytes=False
if uploaded_file:
    file_bytes = uploaded_file.read()
    current_hash = f"{uploaded_file.name}"
    if current_hash != st.session_state.file_hash:
        st.write(f"检测到新简历：{uploaded_file.name}")
        st.session_state.file_hash = current_hash
        st.session_state.resume_content = None
        st.session_state.resume_refine = None
        st.session_state.json_portrait = None
        st.session_state.user_portrait = None
        st.session_state.search_key = None

else:
    st.write(f"您未上传简历")
    resume_content=False
st.divider()

st.write("## 麻烦您再回答15个小问题")
class1,class2,class3,class4,class5= st.tabs(["职业目标", "工作方式偏好","组织环境偏好","行业和方向偏好","现实约束"])
with class1:
    st.header("🎯 第一部分：职业目标")
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
    st.header("⚙️ 第二部分：工作方式偏好")
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
    st.header("🏢 第三部分：组织环境偏好")
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
    st.header("🚀 第四部分：行业和方向偏好")
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
    st.header("🛑 第五部分：现实约束")
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
col1,col2,col3=st.columns([1.2,1,1])
with col2:
    submit=st.button("回答完成，更新画像")

submit_next=False
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
        st.success("🎉 所有必答题数据已更新，用户头像将重新生成！")
        submit_next=True
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
    st.session_state.search_key = None

st.divider()
st.divider()
st.write("## 结果输出")
tab1, tab2, tab3, tab4 = st.tabs(["简历文本", "简历精炼","用户画像","检索词推荐"])
with tab1:
    if file_bytes and st.session_state.resume_content == None:
        st.session_state.resume_content = get_resume_info1(file_bytes)
        st.write(st.session_state.resume_content)
    elif st.session_state.resume_content:
        st.write(st.session_state.resume_content)
    else:
        st.write("简历未上传")
with tab2:
    if st.session_state.resume_content and st.session_state.resume_refine == None:
        with st.spinner("简历正在精炼，请稍等..."):
            st.session_state.resume_refine = get_resume_info2(st.session_state.resume_content)
            st.write(st.session_state.resume_refine)
    elif st.session_state.resume_refine:
        st.write(st.session_state.resume_refine)
    else:
        st.write("简历未上传")
with tab3:
    if st.session_state.resume_refine and st.session_state.json_portrait == None and user_profile_string:
        with st.spinner("用户画像正在生成，请稍等..."):
            st.session_state.json_portrait = get_resume_info3(st.session_state.resume_content,user_profile_string)
            st.session_state.user_portrait = get_resume_info5(st.session_state.json_portrait)
            st.write(st.session_state.user_portrait)
    elif st.session_state.json_portrait:
        st.write(st.session_state.user_portrait)
    else:
        st.write("简历未上传或15个小问题未答完")
with tab4:
    if st.session_state.json_portrait and st.session_state.search_key == None:
        with st.spinner("检索词正在生成，请稍等..."):
            st.session_state.search_key = get_resume_info4(st.session_state.json_portrait)
            st.write(st.session_state.search_key)
    elif st.session_state.json_portrait:
        st.write(st.session_state.search_key)
    else:
        st.write("简历未上传或15个小问题未答完")
st.divider()
st.divider()

st.write("## 让我们随便聊聊")

if st.session_state["messages"] == []:
    st.session_state["messages"]=[{"role":"ai","content":"您好，我是您的AI助手，让我们开始聊天吧！"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

question=st.chat_input()

if question:
    st.session_state["messages"].append({"role":"human","content":question})
    st.chat_message("human").write(question)

    with st.spinner("AI正在思考，请稍等..."):
            response = get_resume_info6(question,st.session_state.user_portrait)

    msg={"role":"ai","content":response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)


