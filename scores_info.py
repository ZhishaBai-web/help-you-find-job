import json
from langchain_core.documents import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from pydantic import SecretStr
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from functools import lru_cache


def load_json_docs(file):
    """获得json切片文档"""
    if isinstance(file, str):            # 文件路径
        with open(file, "r", encoding="utf-8") as f:
            datas = json.load(f)
    else:
        datas = json.load(file)          # 文件对象
    documents = []
    for data in datas:
        doc = Document(
            page_content=str(data),
        )
        documents.append(doc)
    return documents


def get_retriever(texts,db_key,db_url,db_model):
    """存储/检索器"""
    embedding_model = OpenAIEmbeddings(
        model=db_model,
        api_key=SecretStr(db_key),
        base_url=db_url,
        dimensions=1024,
        timeout=10.0
    )
    db = FAISS.from_documents(texts, embedding_model)
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 30,
        }
    )
    return retriever


@lru_cache()
def get_model(key,url,model,temperature):
    """获得语言大模型"""
    llm = ChatOpenAI(
        model=model,
        api_key=SecretStr(key),
        base_url=url,
        temperature=temperature,
    )
    return llm


def get_job_score(key, url, model,job_info,json_profile):
    llm = get_model(key, url, model, 0)
    system_text = """
    你是一名资深职业规划专家、招聘专家和人才匹配算法专家。
    # 任务
    根据【用户JSON画像】和【当前岗位信息】，客观评估该岗位与候选人的匹配程度，并输出评分结果。
    你的职责仅限于对当前岗位进行独立评估。
    不要与其他岗位比较。
    不要考虑排名。
    不要推荐其他岗位。
    不要补充任何岗位信息或候选人信息。
    所有分析必须严格依据输入数据。
    ==================================================

    # 输入
    ## 用户职业画像
    由用户输入，包含：基本信息、教育背景、工作经历、项目经历、技能能力、专业能力、通用能力、职业目标、发展方向、求职偏好
    ==================================================

    # 当前岗位
    岗位信息：
    {job_info}
    ==================================================

    # 分析流程（必须严格执行）
    ## Step1：理解候选人
    分析候选人的：教育背景、工作经历、项目经历、行业经验、专业技能、工具技能、通用能力、管理能力、沟通能力、数据分析能力、项目推进能力、可迁移能力、职业目标、长期发展方向
    重点识别：候选人真正能够创造价值的能力，而不是仅根据职位名称或技能关键词进行判断。
    例如：
    销售经验可以迁移为：客户沟通、商务谈判、需求分析
    项目经验可以迁移为：项目管理、跨部门协作、推进能力
    运营经验可以迁移为：数据分析、用户增长、活动策划
    ==================================================
    ## Step2：理解岗位
    分析岗位：核心职责、日常工作、必备能力、加分能力、工具要求、行业要求、学历要求、工作经验要求、岗位发展空间
    不要仅依据岗位名称判断岗位。
    应依据岗位职责进行分析。
    ==================================================
    ## Step3：能力匹配分析
    判断：
    候选人的能力属于：完全匹配、部分匹配、潜力匹配、不匹配
    重点考虑：已有能力、可迁移能力、学习成本、能否快速胜任
    ==================================================
    ## Step4：职业发展分析
    分析：
    岗位是否能够：延续已有经验、提升核心竞争力、符合职业目标、提供成长空间、提高未来职业价值
    若岗位属于明显降级岗位，应降低评分。
    ==================================================
    ## Step5：硬性条件分析
    重点检查：学历、专业、工作年限、行业经验、必要证书、特殊要求
    若存在明显无法满足的要求，应降低评分。
    ==================================================

    # 评分规则（总分100）
    采用减分原则进行评分。
    初始分数为100分。
    根据能力缺口、经验缺口、职业方向偏离、硬性条件限制、岗位发展价值等因素逐项扣分。
    最终得到综合评分。
    ==================================================
    ## 1. 能力匹配（35分）
    评价：专业技能、工具技能、行业经验、通用能力、可迁移能力
    满分35。
    ==================================================
    ## 2. 工作职责匹配（25分）
    评价：候选人过去经历是否能够支撑岗位主要职责。
    满分25。
    ==================================================
    ## 3. 职业方向匹配（20分）
    评价：
    岗位是否符合：长期职业规划、职业目标、未来发展方向
    满分20。
    ==================================================
    ## 4. 背景条件匹配（10分）
    评价：学历、专业、工作经验、行业背景
    满分10。
    ==================================================
    ## 5. 岗位发展价值（10分）
    评价：
    岗位是否能够：提升能力、增加职业竞争力、提供成长空间、提升长期职业价值
    满分10。
    ==================================================
    综合得分计算方式：
    match_score =ability_match +responsibility_match +career_match +background_match +development_value
    五项得分之和必须严格等于 match_score。
    禁止根据整体印象调整总分。总分只能由五项相加得到。不得在计算完成后再次上调或下调总分。
    ==================================================
    # 评分参考
    95~100：高度匹配，可直接胜任，且符合长期发展。
    90~94：匹配度很高，仅存在少量不足。
    80~89：整体匹配，需要少量学习即可胜任。
    70~79：存在一定能力差距，但具有较好的可迁移能力。
    60~69：存在明显能力不足，仅作为备选。
    60以下：匹配度较低。
    ==================================================
    # 降分规则
    出现以下情况，应明显降低评分：
    - 岗位主要职责与候选人经历关联较弱
    - 职业方向明显不一致
    - 无法满足关键硬性要求
    - 属于明显降级岗位
    - 可迁移能力较弱
    - 成长空间有限

    不得因为：
    - 岗位名称相似
    - 技能关键词相同
    - 使用相同工具
    而直接提高评分。

    ==================================================

    # 输出要求
    所有结论必须严格依据：用户JSON画像、当前岗位信息
    不得编造任何经历、技能、岗位要求或行业背景。
    推荐理由必须具体、可验证，不得使用空泛描述。
    matching_strengths 仅列举真正匹配岗位的核心优势。
    possible_gaps 仅列举真正影响录用的能力差距，不得使用“经验不足”“能力待提升”等空泛描述。
    ==================================================
    # 输出格式
    仅输出 JSON，不输出任何解释。
    {{
      "match_score": 0,
      "ability_match": 0,
      "responsibility_match": 0,
      "career_match": 0,
      "background_match": 0,
      "development_value": 0,
      "recommend_reason": "",
      "matching_strengths": [
        ""
      ],
      "possible_gaps": [
        ""
      ],
      "development_analysis": ""
    }}
    ==================================================
    在输出 JSON 前，必须完成全部分析过程，但不要输出分析过程，仅输出最终 JSON。
    """
    human_text = """
    这是我的json画像：
    {user_profile}
    请据此给岗位打分。
    """

    prompt_Template = ChatPromptTemplate.from_messages(
        [
            ("system", system_text),
            ("human", human_text)
        ]
    )

    chain = prompt_Template | llm
    response = chain.invoke({"user_profile": json_profile, "job_info": job_info})
    return response.content

def save_to_json(jobs_info):
    with open('评分数据gpt1.json', 'w', encoding="utf-8") as f:
        json.dump(jobs_info, f, ensure_ascii=False, indent=2)

def scores_total(file, json_profile, key, url, model,log):
    if isinstance(file, str):  # 文件路径
        with open(file, "r", encoding="utf-8") as f:
            docs = json.load(f)
    else:
        docs = json.load(file)
    new_job_infos = []
    for index, job_info in enumerate(docs):
        numb = index + 1
        log(f"正在给第{numb}条岗位打分")
        response = get_job_score(key, url, model, job_info, json_profile)
        try:
            res = json.loads(response)
            new_job_info = job_info | res
            new_job_infos.append(new_job_info)
        except :
            log(f"第{numb}条岗位第一次输出失败，开始尝试第二次输出")
            response = get_job_score(key, url, model, job_info, json_profile)
            try:
                res = json.loads(response)
                new_job_info = job_info | res
                new_job_infos.append(new_job_info)
            except:
                log(f"第{numb}条岗位第二次输出失败，跳过该岗位")
                continue
    log(f"分析已完成，共分析{len(new_job_infos)}条岗位信息")
    return new_job_infos


def scores_rag(db_key,db_url,db_model,uploaded_file,json_profile,key,url,model,log):
    docs=load_json_docs(uploaded_file)
    retriever=get_retriever(docs,db_key,db_url,db_model)
    retrieved_docs=retriever.invoke(json_profile)
    new_job_infos = []
    for index, job_info in enumerate(retrieved_docs):
        job_info=job_info.page_content
        numb = index + 1
        log(f"正在给第{numb}条岗位打分")
        response=get_job_score(key, url, model,job_info,json_profile)
        try:
            res = json.loads(response)
            job_info=job_info.replace("'",'"')
            job_info = json.loads(job_info)
            new_job_info = job_info | res
            new_job_infos.append(new_job_info)
        except:
            log(f"第{numb}条岗位第一次输出失败，开始尝试第二次输出")
            response=get_job_score(key, url, model,job_info,json_profile)
            try:
                res = json.loads(response)
                job_info = job_info.replace("'", '"')
                job_info = json.loads(job_info)
                new_job_info = job_info | res
                new_job_infos.append(new_job_info)
            except:
                log(f"第{numb}条岗位第二次输出失败，跳过该岗位")
                continue
    log(f"分析已完成，共分析{len(new_job_infos)}条岗位信息")
    return new_job_infos




def train_rag():
    db_key ="sk-JrfN4hxZOKE4Zs7b6M5jYQnBsz0TsM7vGgtSyDXnIpav5Ptm"
    db_url = "https://aigc789.top/v1"
    db_model="text-embedding-3-large"
    file_path="能源大模型应用开发.json"
    key = "sk-JrfN4hxZOKE4Zs7b6M5jYQnBsz0TsM7vGgtSyDXnIpav5Ptm"
    url = "https://aigc789.top/v1"
    model="gpt-5-nano-2025-08-07"
    json_profile = '{ "basic_profile": { "career_identity": "能源系统与工艺仿真+数据/AI交叉的技术型人才（偏个人贡献者）", "career_stage": "早期-成长阶段（硕士毕业约1年+，完成科研与工程项目落地）", "one_sentence_summary": "具备综合能源系统与工艺仿真背景，能将爬虫与RAG智能体等数据/AI方法用于工程信息获取与方案优化，偏好在小团队解决复杂技术问题并做出突破。" }, "education_background": { "highest_degree": "硕士", "major_field": "动力工程（综合能源系统仿真）", "universities": [ "华北电力大学（硕士）", "东北电力大学（本科）" ], "education_summary": "硕士阶段聚焦综合能源系统仿真与优化，本科为能源与动力工程；期间发表SCI论文2篇、授权专利2项（其中实用新型第一作者、发明第二作者），通过CET-6。", "relevant_knowledge": [ "综合能源系统建模与优化（多能互补、园区能源）", "工艺流程模拟（Aspen Plus、Aspen Energy Analyzer）", "能效/经济性/环境可持续性多维评价", "超临界CO2发电、Power-to-Gas相关原理与系统设计", "Python数据分析（numpy、pandas、matplotlib、seaborn）", "爬虫与自动化（XPath、selenium、JS加密逆向）", "AI应用开发（langchain、RAG、Agent）", "科研写作与专利挖掘" ] }, "work_experience": { "total_years": "约1.5年", "experiences": [ { "company": "北京华电能源互联网研究院有限公司", "position": "科研助理", "industry": "能源电力/科研", "period": "2023-072024-07", "responsibilities": [ "参与能源系统相关课题研究与技术方案论证", "协助撰写能源电力系统领域发明专利" ], "achievements": [ "协助完成发明专利4项（已提交/授权，以协作者身份）" ], "technologies": [ "综合能源系统建模思路", "专利撰写流程与技术交底" ] }, { "company": "WOOD中国宁夏分公司", "position": "热工助理工程师", "industry": "工程设计/能源", "period": "2025-072026-01", "responsibilities": [ "按业主要求开展能源系统方案设计与论证", "参与可行性研究与基础设计文件编制" ], "achievements": [ "完成可行性研究2项、基础设计2项并交付" ], "technologies": [ "能源系统方案设计方法", "可研/初设编制流程" ] } ], "career_summary": "路径由科研走向工程实践：研究院期间积累能源系统技术研究与专利协作能力，随后在工程公司完成从需求到可研/初设的工程化交付。期间并行发展数据/AI与爬虫能力，形成“工艺仿真+数据智能”的交叉能力结构。" }, "core_competencies": [ { "name": "工艺仿真与流程优化（Aspen Plus/AEA）", "level": "高级", "evidence": "在离子液体精馏工艺研究中提出两套方案并进行严格模拟，对能效/经济/环境进行对比评估；发表SCI论文2篇。" }, { "name": "综合能源系统方案设计与评估", "level": "中高级", "evidence": "园区多能互补运行优化研究，设计3种工作模式（含超临界CO2与电制天然气），授权发明专利1项；工程端完成2项可研与2项初设。" }, { "name": "Python数据分析与AI应用开发（RAG/Agent）", "level": "中高级", "evidence": "自研爬虫+AI+数据分析一体化智能体（岗位推荐、博导匹配、公众号要点汇总）；掌握langchain、RAG、Agent、numpy/pandas。" }, { "name": "爬虫与逆向工程", "level": "中级", "evidence": "掌握XPath、selenium与JS加密逆向，完成多源信息抓取以支撑智能体与分析任务。" }, { "name": "多目标技术经济-环境评估", "level": "中高级", "evidence": "在工艺研究中同时评估能效、经济性与环境影响，形成系统性对比分析结论。" }, { "name": "项目执行与工程交付", "level": "中级", "evidence": "在工程公司按业主要求完成可研与基础设计交付，具备从需求到文档产出的执行能力。" }, { "name": "专利与科研写作", "level": "中级", "evidence": "第一作者实用新型专利1项（已授权）、第二作者发明专利1项（已授权），并协助4项发明专利；SCI论文2篇。" }, { "name": "技术传播与影响力", "level": "中级", "evidence": "自媒体累计阅读42万+、互动9400+，具备将技术内容转化为受众可理解信息的能力。" }, { "name": "英语技术阅读/写作", "level": "中级", "evidence": "SCI论文发表与CET-6通过。" } ], "experience_analysis": { "valuable_experience": [ "将离子液体精馏新工艺进行严谨建模、仿真与多维度评价，体现从概念到可比选方案的端到端能力。", "园区综合能源系统（含超临界CO2与P2G）的运行策略设计与模式划分，体现系统级建模与优化思路，并产出发明专利。", "在工程公司完成可行性研究和基础设计，探索科研成果向工程交付的转化路径，理解业主需求与合规流程。", "自研爬虫+RAG智能体提升信息收集与知识组织效率，显示跨领域技术组合与快速原型能力。", "在研究院参与专利撰写与技术交底，形成知识产权意识与方法。" ], "transferable_skills": [ "复杂系统问题分解与建模能力（可迁移至多种流程工业与能源项目）", "多目标权衡与定量评估（能效/经济/环境），适用于技术选型与决策支持", "数据获取自动化与知识工程（爬虫+RAG），可迁移至信息密集型业务", "技术文档与专利写作，适用于方案呈现与知识沉淀", "从需求到交付的项目执行能力，适用于咨询、工程与产品实施场景", "跨学科协同与快速学习能力，适合新技术引入与迭代" ] }, "technical_business_profile": { "technical_capability": "强，侧重工艺仿真与综合能源系统设计，兼具Python数据分析、爬虫与RAG/Agent开发能力，擅长多目标技术经济评估。", "business_capability": "中等偏初，能够理解业主需求并转化为可研/初设交付，对成本、能效与合规性有基本把握，具备技术方案呈现与影响力传播能力。", "management_capability": "初级，适合作为小团队/课题核心骨干承担关键技术模块，当前更偏个人贡献者角色。" }, "career_preferences": { "preferred_work": [ "解决复杂问题与技术难题", "技术创新与跨领域探索", "高自由度的研究/开发与自主安排的工作节奏", "以数据与模型驱动的设计优化与决策支持", "从信息获取到方案输出的端到端任务" ], "preferred_environment": [ "小团队、高自由度的组织氛围", "多学科交叉、开放创新的环境", "注重技术深度与实质价值产出的文化" ], "preferred_role_style": [ "核心骨干型个人贡献者", "独立分析、深入思考后解决问题", "偏技术路线而非管理路线（当前阶段）" ] }, "career_motivation": { "main_drivers": [ "技术成长与持续学习", "创造与探索空间", "自主性与高自由度", "工作兴趣匹配", "发展空间", "工作生活平衡" ] }, "career_constraints": { "avoid_roles": [ "高频重复工作", "高压力竞争环境", "强销售性质岗位", "缺乏实际意义的工作" ], "avoid_environment": [ "强KPI与高压竞争文化", "以销售业绩为主导的团队", "流程繁复、个人自主性低的大型组织（相对不偏好）" ], "limitations": [ "总体工作年限约1.5年，完整项目全周期与大规模工程化实践仍需积累", "AI/数据产品的生产级工程化与落地经验有待进一步验证（目前以项目原型为主）", "工作地点偏好：信息不足，需要进一步确认（问卷第13题未提供有效地点信息）" ] }, "professional_profile_summary": "用户是具备综合能源系统与工艺仿真优势、并能将数据/AI方法（爬虫、RAG/Agent）应用于工程信息化与决策支持的交叉型工程人才。其竞争力在于将模型与数据结合，完成从信息获取、仿真分析到技术经济-环境多维评估的闭环；偏好小团队高自由度环境，愿作为核心骨干攻坚复杂技术问题。短板在于工程化规模与生产级AI落地经验尚需积累。适合的发展方向包括：工艺/能源系统仿真与优化工程师、综合能源系统设计与优化工程师、能源数字化/工业AI应用工程师、工艺数据科学家/工业软件应用工程师、碳管理/能效评估咨询等，这些方向兼顾其既有能力、创新偏好与长期成长潜力。" }'
    new_job_infos=scores_rag(db_key,db_url,db_model,file_path,json_profile,key,url,model)
    save_to_json(new_job_infos)

def train_tatol():
    file_path = "能源大模型应用开发.json"
    json_profile = '{ "basic_profile": { "career_identity": "能源系统与工艺仿真+数据/AI交叉的技术型人才（偏个人贡献者）", "career_stage": "早期-成长阶段（硕士毕业约1年+，完成科研与工程项目落地）", "one_sentence_summary": "具备综合能源系统与工艺仿真背景，能将爬虫与RAG智能体等数据/AI方法用于工程信息获取与方案优化，偏好在小团队解决复杂技术问题并做出突破。" }, "education_background": { "highest_degree": "硕士", "major_field": "动力工程（综合能源系统仿真）", "universities": [ "华北电力大学（硕士）", "东北电力大学（本科）" ], "education_summary": "硕士阶段聚焦综合能源系统仿真与优化，本科为能源与动力工程；期间发表SCI论文2篇、授权专利2项（其中实用新型第一作者、发明第二作者），通过CET-6。", "relevant_knowledge": [ "综合能源系统建模与优化（多能互补、园区能源）", "工艺流程模拟（Aspen Plus、Aspen Energy Analyzer）", "能效/经济性/环境可持续性多维评价", "超临界CO2发电、Power-to-Gas相关原理与系统设计", "Python数据分析（numpy、pandas、matplotlib、seaborn）", "爬虫与自动化（XPath、selenium、JS加密逆向）", "AI应用开发（langchain、RAG、Agent）", "科研写作与专利挖掘" ] }, "work_experience": { "total_years": "约1.5年", "experiences": [ { "company": "北京华电能源互联网研究院有限公司", "position": "科研助理", "industry": "能源电力/科研", "period": "2023-072024-07", "responsibilities": [ "参与能源系统相关课题研究与技术方案论证", "协助撰写能源电力系统领域发明专利" ], "achievements": [ "协助完成发明专利4项（已提交/授权，以协作者身份）" ], "technologies": [ "综合能源系统建模思路", "专利撰写流程与技术交底" ] }, { "company": "WOOD中国宁夏分公司", "position": "热工助理工程师", "industry": "工程设计/能源", "period": "2025-072026-01", "responsibilities": [ "按业主要求开展能源系统方案设计与论证", "参与可行性研究与基础设计文件编制" ], "achievements": [ "完成可行性研究2项、基础设计2项并交付" ], "technologies": [ "能源系统方案设计方法", "可研/初设编制流程" ] } ], "career_summary": "路径由科研走向工程实践：研究院期间积累能源系统技术研究与专利协作能力，随后在工程公司完成从需求到可研/初设的工程化交付。期间并行发展数据/AI与爬虫能力，形成“工艺仿真+数据智能”的交叉能力结构。" }, "core_competencies": [ { "name": "工艺仿真与流程优化（Aspen Plus/AEA）", "level": "高级", "evidence": "在离子液体精馏工艺研究中提出两套方案并进行严格模拟，对能效/经济/环境进行对比评估；发表SCI论文2篇。" }, { "name": "综合能源系统方案设计与评估", "level": "中高级", "evidence": "园区多能互补运行优化研究，设计3种工作模式（含超临界CO2与电制天然气），授权发明专利1项；工程端完成2项可研与2项初设。" }, { "name": "Python数据分析与AI应用开发（RAG/Agent）", "level": "中高级", "evidence": "自研爬虫+AI+数据分析一体化智能体（岗位推荐、博导匹配、公众号要点汇总）；掌握langchain、RAG、Agent、numpy/pandas。" }, { "name": "爬虫与逆向工程", "level": "中级", "evidence": "掌握XPath、selenium与JS加密逆向，完成多源信息抓取以支撑智能体与分析任务。" }, { "name": "多目标技术经济-环境评估", "level": "中高级", "evidence": "在工艺研究中同时评估能效、经济性与环境影响，形成系统性对比分析结论。" }, { "name": "项目执行与工程交付", "level": "中级", "evidence": "在工程公司按业主要求完成可研与基础设计交付，具备从需求到文档产出的执行能力。" }, { "name": "专利与科研写作", "level": "中级", "evidence": "第一作者实用新型专利1项（已授权）、第二作者发明专利1项（已授权），并协助4项发明专利；SCI论文2篇。" }, { "name": "技术传播与影响力", "level": "中级", "evidence": "自媒体累计阅读42万+、互动9400+，具备将技术内容转化为受众可理解信息的能力。" }, { "name": "英语技术阅读/写作", "level": "中级", "evidence": "SCI论文发表与CET-6通过。" } ], "experience_analysis": { "valuable_experience": [ "将离子液体精馏新工艺进行严谨建模、仿真与多维度评价，体现从概念到可比选方案的端到端能力。", "园区综合能源系统（含超临界CO2与P2G）的运行策略设计与模式划分，体现系统级建模与优化思路，并产出发明专利。", "在工程公司完成可行性研究和基础设计，探索科研成果向工程交付的转化路径，理解业主需求与合规流程。", "自研爬虫+RAG智能体提升信息收集与知识组织效率，显示跨领域技术组合与快速原型能力。", "在研究院参与专利撰写与技术交底，形成知识产权意识与方法。" ], "transferable_skills": [ "复杂系统问题分解与建模能力（可迁移至多种流程工业与能源项目）", "多目标权衡与定量评估（能效/经济/环境），适用于技术选型与决策支持", "数据获取自动化与知识工程（爬虫+RAG），可迁移至信息密集型业务", "技术文档与专利写作，适用于方案呈现与知识沉淀", "从需求到交付的项目执行能力，适用于咨询、工程与产品实施场景", "跨学科协同与快速学习能力，适合新技术引入与迭代" ] }, "technical_business_profile": { "technical_capability": "强，侧重工艺仿真与综合能源系统设计，兼具Python数据分析、爬虫与RAG/Agent开发能力，擅长多目标技术经济评估。", "business_capability": "中等偏初，能够理解业主需求并转化为可研/初设交付，对成本、能效与合规性有基本把握，具备技术方案呈现与影响力传播能力。", "management_capability": "初级，适合作为小团队/课题核心骨干承担关键技术模块，当前更偏个人贡献者角色。" }, "career_preferences": { "preferred_work": [ "解决复杂问题与技术难题", "技术创新与跨领域探索", "高自由度的研究/开发与自主安排的工作节奏", "以数据与模型驱动的设计优化与决策支持", "从信息获取到方案输出的端到端任务" ], "preferred_environment": [ "小团队、高自由度的组织氛围", "多学科交叉、开放创新的环境", "注重技术深度与实质价值产出的文化" ], "preferred_role_style": [ "核心骨干型个人贡献者", "独立分析、深入思考后解决问题", "偏技术路线而非管理路线（当前阶段）" ] }, "career_motivation": { "main_drivers": [ "技术成长与持续学习", "创造与探索空间", "自主性与高自由度", "工作兴趣匹配", "发展空间", "工作生活平衡" ] }, "career_constraints": { "avoid_roles": [ "高频重复工作", "高压力竞争环境", "强销售性质岗位", "缺乏实际意义的工作" ], "avoid_environment": [ "强KPI与高压竞争文化", "以销售业绩为主导的团队", "流程繁复、个人自主性低的大型组织（相对不偏好）" ], "limitations": [ "总体工作年限约1.5年，完整项目全周期与大规模工程化实践仍需积累", "AI/数据产品的生产级工程化与落地经验有待进一步验证（目前以项目原型为主）", "工作地点偏好：信息不足，需要进一步确认（问卷第13题未提供有效地点信息）" ] }, "professional_profile_summary": "用户是具备综合能源系统与工艺仿真优势、并能将数据/AI方法（爬虫、RAG/Agent）应用于工程信息化与决策支持的交叉型工程人才。其竞争力在于将模型与数据结合，完成从信息获取、仿真分析到技术经济-环境多维评估的闭环；偏好小团队高自由度环境，愿作为核心骨干攻坚复杂技术问题。短板在于工程化规模与生产级AI落地经验尚需积累。适合的发展方向包括：工艺/能源系统仿真与优化工程师、综合能源系统设计与优化工程师、能源数字化/工业AI应用工程师、工艺数据科学家/工业软件应用工程师、碳管理/能效评估咨询等，这些方向兼顾其既有能力、创新偏好与长期成长潜力。" }'
    # key ="sk-9913e2c88c09477fa5492318c4ba6768"
    # url="https://api.deepseek.com"
    # model="deepseek-v4-flash"
    key = "sk-JrfN4hxZOKE4Zs7b6M5jYQnBsz0TsM7vGgtSyDXnIpav5Ptm"
    url = "https://aigc789.top/v1"
    model="gpt-5-nano-2025-08-07"
    new_job_infos=scores_total(file_path, json_profile, key, url, model)
    save_to_json(new_job_infos)


if __name__ == "__main__":
    train_tatol()

