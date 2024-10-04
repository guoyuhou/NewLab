# pages/file_manager.py
"""
此文件包含文件管理页面的功能实现。
主要功能包括：文件上传、文件列表显示、文件下载、文件删除和文件共享。
"""

import streamlit as st
from modules import cloud_storage

def render():
    """渲染文件管理页面的主要函数"""
    st.title("文件管理")

    # 文件上传部分
    uploaded_file = st.file_uploader("上传文件", type=["txt", "pdf", "doc", "docx", "xls", "xlsx"])
    if uploaded_file is not None:
        if st.button("确认上传"):
            # 调用云存储模块上传文件
            file_id = cloud_storage.upload_file(uploaded_file, st.session_state.user['id'])
            if file_id:
                st.success(f"文件 '{uploaded_file.name}' 上传成功！")
            else:
                st.error("文件上传失败，请重试。")

    # 显示用户文件列表部分
    st.subheader("我的文件")
    # 获取用户的文件列表
    files = cloud_storage.list_user_files(st.session_state.user['id'])
    for file in files:
        # 为每个文件创建三列布局：文件名、下载按钮和删除按钮
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(file['name'])
        if col2.button("下载", key=f"download_{file['id']}"):
            # 调用云存储模块下载文件
            cloud_storage.download_file(file['id'], st.session_state.user['id'])
        if col3.button("删除", key=f"delete_{file['id']}"):
            # 调用云存储模块删除文件，成功后刷新页面
            if cloud_storage.delete_file(file['id'], st.session_state.user['id']):
                st.experimental_rerun()

    # 文件共享部分
    st.subheader("文件共享")
    # 选择要共享的文件
    file_to_share = st.selectbox("选择要共享的文件", [f['name'] for f in files])
    # 输入要共享的用户名
    share_with = st.text_input("输入要共享的用户名")
    if st.button("共享文件"):
        # 调用云存储模块共享文件
        if cloud_storage.share_file(file_to_share, share_with, st.session_state.user['id']):
            st.success(f"文件 '{file_to_share}' 已成功共享给 {share_with}")
        else:
            st.error("文件共享失败，请检查用户名是否正确。")