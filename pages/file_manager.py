# pages/file_manager.py

import streamlit as st
from modules import cloud_storage

def render():
    st.title("文件管理")

    # 文件上传
    uploaded_file = st.file_uploader("上传文件", type=["txt", "pdf", "doc", "docx", "xls", "xlsx"])
    if uploaded_file is not None:
        if st.button("确认上传"):
            file_id = cloud_storage.upload_file(uploaded_file, st.session_state.user['id'])
            if file_id:
                st.success(f"文件 '{uploaded_file.name}' 上传成功！")
            else:
                st.error("文件上传失败，请重试。")

    # 显示用户文件列表
    st.subheader("我的文件")
    files = cloud_storage.list_user_files(st.session_state.user['id'])
    for file in files:
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(file['name'])
        if col2.button("下载", key=f"download_{file['id']}"):
            cloud_storage.download_file(file['id'], st.session_state.user['id'])
        if col3.button("删除", key=f"delete_{file['id']}"):
            if cloud_storage.delete_file(file['id'], st.session_state.user['id']):
                st.experimental_rerun()

    # 文件共享
    st.subheader("文件共享")
    file_to_share = st.selectbox("选择要共享的文件", [f['name'] for f in files])
    share_with = st.text_input("输入要共享的用户名")
    if st.button("共享文件"):
        if cloud_storage.share_file(file_to_share, share_with, st.session_state.user['id']):
            st.success(f"文件 '{file_to_share}' 已成功共享给 {share_with}")
        else:
            st.error("文件共享失败，请检查用户名是否正确。")