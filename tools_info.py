import pandas as pd
import json
import numpy as np
import re


def get_data(files):
    """获得合并后的字典列表"""
    datas=[]
    for file in files:
        if isinstance(file, str):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                datas.extend(data)
        else:
            data = json.load(file)
            datas.extend(data)
    return datas

def concat_files(files,hr_select):
    """获得去重/筛选后的字典列表"""
    datas=get_data(files)
    datas=pd.DataFrame(datas)
    datas_rows=len(datas)
    new_datas=datas.drop_duplicates(subset=['公司名称','职位名称','薪资'])
    new_datas_rows=len(new_datas)
    if hr_select=="开启 HR 活跃度筛选":
        discard_list = ['半年前活跃','5月内活跃','4月内活跃','3月内活跃','2月内活跃','近半年活跃',]
        drop_index = new_datas[new_datas['HR活跃时间'].isin(discard_list)].index
        clear_datas=new_datas.drop(index=drop_index)
        clear_data_rows = len(clear_datas)
        words=f"文件总共包含岗位数{datas_rows}个，去重后剩余岗位{new_datas_rows}个，排除HR未在本月活跃的岗位后，最终剩余岗位数{clear_data_rows}个"
        return clear_datas,words
    else:
        words = f"文件总共包含岗位数{datas_rows}个，去重后剩余岗位{new_datas_rows}个"
        return new_datas,words


def parse_salary(salary):
    """将薪资统一转换成：salary_min：最低月薪（元），salary_max：最高月薪（元）"""

    if pd.isna(salary):
        return np.nan, np.nan

    salary = str(salary)
    nums = re.findall(r"\d+(?:\.\d+)?", salary)

    if len(nums) == 0:
        return np.nan, np.nan
    low = float(nums[0])

    if len(nums) == 1:
        high = low
    else:
        high = float(nums[1])

    if "元/天" in salary:                           # 日薪 → 月薪（元）
        low = low * 21.75
        high = high * 21.75
    elif "元/时" in salary:                          # 时薪 → 月薪（元）
        low = low * 8 * 21.75
        high = high * 8 * 21.75
    elif "元/月" in salary:                           # 元/月 → 不需要转换
        pass
    elif "万/月" in salary or "万" in salary:         # 万/月 → 元
        low = low * 10000
        high = high * 10000
    elif "K" in salary.upper():                      # K → 元
        low = low * 1000
        high = high * 1000
    else:
        return np.nan, np.nan
    return low, high



def get_analysis_df(file):
    if isinstance(file, str):
        df = pd.read_json(file)
    else:
        analysis_data = json.load(file)
        df=pd.DataFrame(analysis_data)
    df[["最低薪资", "最高薪资"]] = df["薪资"].apply(lambda x: pd.Series(parse_salary(x)))
    return df


def get_top50_df(file):
    analysis_df=get_analysis_df(file)
    top50_df=analysis_df.sort_values("总得分", ascending=False).head(50).reset_index(drop=True)
    top50_df.index = top50_df.index + 1
    return top50_df

