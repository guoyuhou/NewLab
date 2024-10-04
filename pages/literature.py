"""
pages/literature.py

本模块实现了实验室管理系统的学术文献管理功能。

主要功能:
1. 添加新文献
2. 搜索现有文献
3. 编辑文献信息

作者: [您的名字]
创建日期: [创建日期]
最后修改日期: [最后修改日期]
"""

import streamlit as st
from modules import literature_management
import datetime

def render():
    """渲染学术文献管理页面的主函数"""
    st.title("学术文献管理")

    # 添加新文献
    st.subheader("添加新文献")
    title = st.text_input("标题")
    authors = st.text_input("作者 (用逗号分隔)")
    journal = st.text_input("期刊")
    year = st.number_input("年份", min_value=1900, max_value=datetime.now().year, value=datetime.now().year)
    doi = st.text_input("DOI (可选)")
    notes = st.text_area("笔记 (可选)")

    if st.button("添加文献"):
        # 尝试添加新文献
        if literature_management.add_literature(st.session_state.user['id'], title, authors, journal, year, doi, notes):
            st.success("文献添加成功！")
        else:
            st.error("添加文献失败，请重试。")

    # 搜索文献
    st.subheader("搜索文献")
    search_query = st.text_input("搜索 (标题、作者或关键词)")
    if search_query:
        # 执行文献搜索
        results = literature_management.search_literature(search_query)
        for result in results:
            st.write(f"**{result['title']}**")
            st.write(f"作者: {result['authors']}")
            st.write(f"期刊: {result['journal']}, {result['year']}")
            if result['doi']:
                st.write(f"DOI: {result['doi']}")
            if result['notes']:
                st.write(f"笔记: {result['notes']}")
            if st.button("编辑", key=f"edit_{result['id']}"):
                # 设置要编辑的文献ID
                st.session_state.edit_literature_id = result['id']
                st.experimental_rerun()
            st.write("---")

    # 编辑文献
    if 'edit_literature_id' in st.session_state:
        st.subheader("编辑文献")
        # 获取要编辑的文献信息
        literature = literature_management.get_literature(st.session_state.edit_literature_id)
        new_title = st.text_input("标题", value=literature['title'])
        new_authors = st.text_input("作者", value=literature['authors'])
        new_journal = st.text_input("期刊", value=literature['journal'])
        new_year = st.number_input("年份", min_value=1900, max_value=datetime.now().year, value=literature['year'])
        new_doi = st.text_input("DOI", value=literature['doi'])
        new_notes = st.text_area("笔记", value=literature['notes'])

        if st.button("保存更改"):
            # 尝试更新文献信息
            if literature_management.update_literature(st.session_state.edit_literature_id, new_title, new_authors, new_journal, new_year, new_doi, new_notes):
                st.success("文献更新成功！")
                del st.session_state.edit_literature_id
                st.experimental_rerun()
            else:
                st.error("更新文献失败，请重试。")

        if st.button("取消编辑"):
            # 取消编辑，清除编辑状态
            del st.session_state.edit_literature_id
            st.experimental_rerun()