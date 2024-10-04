# pages/reports.py
"""
这个文件包含了报告生成页面的功能实现。
主要功能包括生成月度报告、显示报告内容和提供报告下载功能。
"""

import streamlit as st
from modules import report_generation
import base64

def render():
    """渲染报告生成页面的主要函数"""
    st.title("报告生成")

    # 生成月度报告按钮
    if st.button("生成月度报告"):
        report = report_generation.generate_monthly_report()
        st.session_state.current_report = report
        st.success("报告生成成功！")

    # 如果存在当前报告，显示报告内容
    if "current_report" in st.session_state:
        report = st.session_state.current_report
        st.header(report["title"])

        # 遍历并显示报告的每个部分
        for section in report["sections"]:
            st.subheader(section["title"])
            st.write(section["content"], unsafe_allow_html=True)
            st.image(section["chart"], use_column_width=True)

        # 提供报告下载链接
        report_html = generate_report_html(report)
        b64 = base64.b64encode(report_html.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="monthly_report.html">下载报告</a>'
        st.markdown(href, unsafe_allow_html=True)

def generate_report_html(report):
    """生成报告的HTML格式"""
    html = f"<html><head><title>{report['title']}</title></head><body>"
    html += f"<h1>{report['title']}</h1>"

    # 遍历报告的每个部分，添加到HTML中
    for section in report["sections"]:
        html += f"<h2>{section['title']}</h2>"
        html += section["content"]
        img_base64 = base64.b64encode(section["chart"].getvalue()).decode()
        html += f'<img src="data:image/png;base64,{img_base64}" />'

    html += "</body></html>"
    return html