"""
pages/lab_info.py

这个文件包含了实验室信息页面的渲染逻辑。
它显示实验室的基本信息、成员列表、主要设备和最新发表的论文。
如果用户是管理员，还提供了编辑实验室信息的功能。
"""

import streamlit as st
from modules import lab_management

def render():
    """渲染实验室信息页面的主函数"""
    st.title("实验室信息")

    # 获取实验室基本信息
    lab_info = lab_management.get_lab_info()

    # 显示实验室基本信息
    st.header("基本信息")
    st.write(f"实验室名称: {lab_info['name']}")
    st.write(f"所属机构: {lab_info['institution']}")
    st.write(f"成立时间: {lab_info['established_date']}")
    st.write(f"研究方向: {lab_info['research_focus']}")

    # 显示实验室成员
    st.header("实验室成员")
    members = lab_management.get_lab_members()
    for member in members:
        st.subheader(member['name'])
        st.write(f"职位: {member['position']}")
        st.write(f"邮箱: {member['email']}")
        st.write(f"研究方向: {member['research_area']}")

    # 显示实验室设备
    st.header("主要设备")
    equipment = lab_management.get_lab_equipment()
    for item in equipment:
        st.subheader(item['name'])
        st.write(f"型号: {item['model']}")
        st.write(f"购置时间: {item['purchase_date']}")
        st.write(f"状态: {item['status']}")

    # 显示最近发表的论文
    st.header("最新发表论文")
    papers = lab_management.get_recent_papers()
    for paper in papers:
        st.write(f"**{paper['title']}**")
        st.write(f"作者: {paper['authors']}")
        st.write(f"发表于: {paper['journal']}, {paper['date']}")

    # 如果用户是管理员，显示编辑按钮
    if lab_management.is_admin(st.session_state.user['id']):
        if st.button("编辑实验室信息"):
            st.session_state.edit_lab_info = True
            st.experimental_rerun()

    # 编辑实验室信息的表单
    if st.session_state.get('edit_lab_info', False):
        st.header("编辑实验室信息")
        # 创建输入字段，用于编辑实验室信息
        new_name = st.text_input("实验室名称", lab_info['name'])
        new_institution = st.text_input("所属机构", lab_info['institution'])
        new_established_date = st.date_input("成立时间", lab_info['established_date'])
        new_research_focus = st.text_area("研究方向", lab_info['research_focus'])

        # 保存更改按钮
        if st.button("保存更改"):
            # 尝试更新实验室信息
            if lab_management.update_lab_info(new_name, new_institution, new_established_date, new_research_focus):
                st.success("实验室信息更新成功！")
                st.session_state.edit_lab_info = False
                st.experimental_rerun()
            else:
                st.error("更新失败，请重试。")