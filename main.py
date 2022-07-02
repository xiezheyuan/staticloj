import json
import traceback
import streamlit as st
import numpy as np
from database import *

st.sidebar.title("Static LibreOJ")


# noinspection PyBroadException
def on_click():
    try:
        data = LOJProblem.get(LOJProblem.id == int(id_))
    except BaseException:
        st.markdown("该题目 **尚未收录**！")
        st.markdown("内部错误：\n```\n%s\n```" % traceback.format_exc())
    else:
        st.header("#" + str(data.id) + ". " + str(data.name))
        st.markdown("题型：%s，时间限制：$%d \\operatorname{ms}$，空间限制 $%d \\operatorname{MB}$。"
                    % (data.problem_type, data.time_limit, data.memory_limit))
        st.markdown("标签：%s" % data.tags)
        st.markdown("提交数：$%d$，通过数：$%d$。" % (data.submit_count, data.accepted_count))
        st.markdown(data.body, unsafe_allow_html=True)
        st.download_button("下载题面", data.body, "%s.md" % data.name)
        if data.score != "[]":
            st.markdown("## 提交信息\n\n### 统计")
            st.markdown("#### 分数统计")
            score_array = json.loads(data.score)
            st.line_chart(score_array)
            pjs = 0
            people = 0
            for i in enumerate(score_array):
                people += i[1]
                pjs += i[0]*i[1]
            st.markdown("平均分：$%.2f$。" % (pjs/people))
            # noinspection PyStringFormat
            st.markdown("方差：$%.2f$，标准差：$%.2f$。" % (np.var(score_array), np.std(score_array, ddof=1)))
            qzh = [score_array[0]]
            for i in score_array[1:]:
                qzh.append(qzh[-1] + i)
            st.markdown("#### 前缀和")
            st.line_chart(qzh)
            st.markdown("#### 前缀差分")
            cha = [0]
            for i in enumerate(score_array[1:]):
                cha.append(i[1] - score_array[i[0] - 1])
            st.line_chart(cha)
            st.markdown("### 最优解")
            st.markdown("提交者：`%s`，提交语言：`%s`。" % (data.fastest_submitter, data.fastest_language))
            st.markdown("```%s\n%s\n```" % (data.fastest_language, data.fastest_code))
            st.download_button("下载程序", data.fastest_code, "%d.%s" % (data.id, data.fastest_language))
        st.sidebar.markdown("[提交这个题目](https://loj.ac/p/%d)" % data.id)


def search_action():
    keyword = str(search)

    if not bool(is_body):
        problems = LOJProblem.select().where(LOJProblem.name.contains(keyword))
    else:
        problems = LOJProblem.select().where((LOJProblem.name.contains(keyword)) | (LOJProblem.body.contains(keyword)))

    st.markdown("找到 $%d$ 个结果。" % len(problems))
    for problem in problems:
        st.markdown("- ID: $%d$, 名字：**%s**。" % (problem.id, problem.name))


def show_all():
    for i in LOJProblem.select():
        st.markdown("%d. %s" % (i.id, i.name))


id_ = st.sidebar.number_input("ID:", min_value=1)

load = st.sidebar.button("加载", on_click=on_click)

st.sidebar.markdown("或者尝试搜索题目名：")

search = st.sidebar.text_input("关键词：")

is_body = st.sidebar.checkbox("搜索内容")

search_btn = st.sidebar.button("搜索", on_click=search_action)

show_all_btn = st.sidebar.button("显示全部题目", on_click=show_all)
