# pages/project_management.py

"""
这个文件包含了项目管理页面的渲染逻辑。
主要功能包括:
1. 创建新项目
2. 显示用户的项目列表
3. 为项目添加任务
4. 更新任务状态
5. 显示项目统计信息
6. 可视化项目进度
"""

import streamlit as st
from modules import project_management
import plotly.graph_objects as go

def render():
    st.title("项目管理")

    # 创建新项目
    st.subheader("创建新项目")
    project_name = st.text_input("项目名称")
    project_description = st.text_area("项目描述")
    start_date = st.date_input("开始日期")
    end_date = st.date_input("结束日期")

    if st.button("创建项目"):
        # 尝试创建新项目并显示结果
        if project_management.create_project(st.session_state.user['id'], project_name, project_description, start_date, end_date):
            st.success("项目创建成功！")
        else:
            st.error("创建项目失败，请重试。")

    # 显示用户的项目
    st.subheader("我的项目")
    projects = project_management.get_user_projects(st.session_state.user['id'])
    for project in projects:
        # 显示项目基本信息
        st.write(f"**{project['name']}**")
        st.write(f"描述: {project['description']}")
        st.write(f"开始日期: {project['start_date']}, 结束日期: {project['end_date']}")
        st.write(f"状态: {project['status']}")

        # 添加任务
        new_task = st.text_input("新任务", key=f"new_task_{project['id']}")
        if st.button("添加任务", key=f"add_task_{project['id']}"):
            # 尝试添加新任务并显示结果
            if project_management.add_task(project['id'], new_task):
                st.success("任务添加成功！")
                st.experimental_rerun()
            else:
                st.error("添加任务失败，请重试。")

        # 显示任务
        tasks = project_management.get_project_tasks(project['id'])
        for task in tasks:
            col1, col2 = st.columns([3, 1])
            col1.write(task['description'])
            # 允许用户更新任务状态
            status = col2.selectbox("状态", ["进行中", "已完成"], index=0 if task['status'] == "进行中" else 1, key=f"task_status_{task['id']}")
            if status != task['status']:
                if project_management.update_task_status(task['id'], status):
                    st.experimental_rerun()

        st.write("---")

    # 项目统计
    st.subheader("项目统计")
    total_projects = len(projects)
    completed_projects = sum(1 for p in projects if p['status'] == '已完成')
    st.write(f"总项目数: {total_projects}")
    st.write(f"已完成项目: {completed_projects}")
    st.write(f"完成率: {completed_projects / total_projects:.2%}" if total_projects > 0 else "完成率: N/A")

    # 项目进度可视化
    if projects:
        # 使用Plotly创建堆叠柱状图来显示项目任务完成情况
        fig = go.Figure(data=[
            go.Bar(name='已完成', x=[p['name'] for p in projects], y=[p['completed_tasks'] for p in projects]),
            go.Bar(name='进行中', x=[p['name'] for p in projects], y=[p['total_tasks'] - p['completed_tasks'] for p in projects])
        ])
        fig.update_layout(barmode='stack', title='项目任务完成情况')
        st.plotly_chart(fig)