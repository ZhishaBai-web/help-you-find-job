from DrissionPage import Chromium, ChromiumOptions
import time
from random import randint
import re
import json


def get_detail_info(browser,job):
    """获得岗位详细页信息：公司介绍、公司成立日期、岗位介绍、岗位地址、投递网址、HR活跃时间、经验要求"""
    encryptJobId = job['encryptJobId']
    apply_url = f"https://www.zhipin.com/job_detail/{encryptJobId}.html"        # 获取投递网址
    #print(apply_url)
    tab2 = browser.new_tab()
    tab2.get(url=apply_url)
    # print(tab2.html)

    brand_des_ele = tab2.ele('xpath://div[@class="job-sec-text fold-text"]')    # 获取公司介绍
    if brand_des_ele:
        brand_des = brand_des_ele.text
    else:
        brand_des = "缺失"

    brand_time_ele = tab2.ele('xpath://li[@class="res-time"]')                  # 获取公司成立日期
    if brand_time_ele:
        brand_time = brand_time_ele.text
        brand_time = re.findall("成立日期(.*)",brand_time)[0]
    else:
        brand_time = "缺失"

    job_des_ele = tab2.ele('xpath://div[@class="job-sec-text"]')                # 获取岗位介绍
    if job_des_ele:
        job_des = job_des_ele.text.replace("boss","").replace("来自BOSS","").replace("直聘","")
        job_des = job_des.replace("BOSS","").replace("kanzhun","")

    else:
        job_des = "缺失"

    job_address_ele = tab2.ele('xpath://div[@class ="location-address"]')       # 获取岗位地址
    if job_address_ele:
        job_address = job_address_ele.text
    else:
        job_address = "缺失"

    job_time_ele = tab2.ele('xpath://span[@class ="boss-active-time"]')         # 获取HR活跃时间
    if job_time_ele:
        job_time = job_time_ele.text
    else:
        job_time = "缺失"

    job_experience_ele = tab2.ele('xpath://span[@class ="text-desc text-experiece"]')         # 获取经验要求
    if job_experience_ele:
        job_experience = job_experience_ele.text
    else:
        job_experience = "缺失"

    time.sleep(randint(2,3))
    tab2.close()
    return brand_des, brand_time, job_des, apply_url, job_address,job_time,job_experience


def get_simple_info(job):
    """岗位的简单信息：公司名称、公司规模、公司所处行业、岗位名称、岗位薪资、学历要求、时长要求"""
    brandName = job['brandName']
    brandScale = job['brandScaleName']
    Industry = job['brandIndustry']
    job_name = job['jobName']
    salary = job['salaryDesc']
    degree = job['jobDegree']
    leastMonth = job['leastMonthDesc']
    return brandName, brandScale, Industry, job_name, salary, degree, leastMonth


def get_total_info(browser,job):
    """单个岗位的完整信息"""
    brandName, brandScale, Industry, job_name, salary, degree, leastMonth = get_simple_info(job)
    brand_des, brand_time, job_des, apply_url, job_address, job_time,job_experience = get_detail_info(browser, job)
    job_info = {
        "公司名称": brandName,
        "公司成立日期": brand_time,
        "公司规模": brandScale,
        "所在行业": Industry,
        "公司介绍": brand_des,
        "职位名称": job_name,
        "薪资": salary,
        "时长要求": leastMonth,
        "岗位地址": job_address,
        "学历要求": degree,
        "岗位介绍": job_des,
        "投递网址": apply_url,
        "HR活跃时间": job_time,
        "经验要求":job_experience
    }
    return job_info


def save_to_json(jobs_info,name):
    with open(f'{name}.json', 'w', encoding="utf-8") as f:
        json.dump(jobs_info,f,ensure_ascii = False, indent = 2)



def get_url(user_city,user_jobtype,user_salary,user_experience,user_degree,user_scale,user_query):
    city={"北京":"city=101010100","上海":"city=101020100","广州":"city=101280100","深圳":"city=101280600","杭州":"city=101210100"}
    jobtype={"不限":"","实习":"&jobType=1902","兼职":"&jobType=1903","全职":"&jobType=1901"}
    salary={"不限":"","3-5K":"&salary=403","5-10K":"&salary=404","10-20K":"&salary=405"}
    experience={"不限":"","在校生":"&experience=108","应届生":"&experience=102","经验不限":"&experience=101"}
    degree={"不限":"","大专":"&degree=202","本科":"&degree=203","硕士":"&degree=204"}
    scale={"不限":"","0-20人":"&scale=301","20-99人":"&scale=302","100-499人":"&scale=303"}
    if user_query:
        user_query=f"&query={user_query}"
    url="https://www.zhipin.com/web/geek/jobs?"+city[user_city]+jobtype[user_jobtype]+salary[user_salary]+experience[user_experience]+degree[user_degree]+scale[user_scale]+user_query
    return url

def get_job_information(url,log,exe_path):
    co = ChromiumOptions().set_browser_path(fr"{exe_path}")
    browser = Chromium(addr_or_opts=co)
    tab1 = browser.latest_tab
    tab1.listen.start("joblist")
    tab1.get(url)

    jobs_info=[]
    for page in range(1,50):
        log(f"正在采集第{page}页，当前已爬取岗位数: {len(jobs_info)}")
        resp = tab1.listen.wait(timeout=5)
        if not resp:
            log(f"【提示】超时未捕获到新数据包，说明当前可能已无更多数据，岗位采集结束。")
            log(f"已爬取岗位数: {len(jobs_info)}")
            break
        json_data=resp.response.body
        job_list=json_data['zpData']['jobList']
        for job in job_list:
            job_info = get_total_info(browser,job)
            jobs_info.append(job_info)
            log(f"{job_info['公司名称']}的{job_info['职位名称']}岗位爬取成功")
        tab1.scroll.to_bottom()
    return jobs_info
    #save_to_json(jobs_info,user_query)

def job_get():
    user_city = "北京"
    user_jobtype = "不限"
    user_salary = "不限"
    user_experience = "不限"
    user_degree = "不限"
    user_scale = "不限"
    user_query = "大模型"

    url=get_url(user_city, user_jobtype, user_salary, user_experience, user_degree, user_scale, user_query)
    get_job_information(url,user_query)

if __name__ == "__main__":
    job_get()