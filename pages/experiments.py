# pages/experiments.py
"""
这个文件包含了实验记录页面的渲染逻辑。
它使用Streamlit库创建一个用户界面，允许用户创建、查看和管理实验记录。
"""

import streamlit as st
from modules import experiment_records

def render():
    """渲染实验记录页面的主函数"""
    st.title("实验记录")

    # 创建新实验记录
    st.subheader("创建新实验记录")
    exp_name = st.text_input("实验名称")
    exp_description = st.text_area("实验描述")
    exp_date = st.date_input("实验日期")
    if st.button("创建实验记录"):
        # 尝试创建新的实验记录
        if experiment_records.create_experiment(st.session_state.user['id'], exp_name, exp_description, exp_date):
            st.success("实验记录创建成功！")
        else:
            st.error("创建实验记录失败，请重试。")

    # 显示用户的实验记录列表
    st.subheader("我的实验记录")
    experiments = experiment_records.get_user_experiments(st.session_state.user['id'])
    for exp in experiments:
        # 为每个实验记录创建一个可展开的部分
        expander = st.expander(f"{exp['name']} - {exp['date']}")
        with expander:
            st.write(f"描述: {exp['description']}")
            if st.button("编辑", key=f"edit_{exp['id']}"):
                # 这里可以添加编辑功能
                pass
            if st.button("删除", key=f"delete_{exp['id']}"):
                # 尝试删除实验记录
                if experiment_records.delete_experiment(exp['id'], st.session_state.user['id']):
                    st.experimental_rerun()
                else:
                    st.error("删除实验记录失败，请重试。")