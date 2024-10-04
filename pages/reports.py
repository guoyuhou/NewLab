# pages/reports.py

import streamlit as st
from modules import report_generation
import base64

def render():
    st.title("报告生成")

    if st.button("生成月度报告"):
        report = report_generation.generate_monthly_report()
        st.session_state.current_report = report
        st.success("报告生成成功！")

    if "current_report" in st.session_state:
        report = st.session_state.current_report
        st.header(report["title"])

        for section in report["sections"]:
            st.subheader(section["title"])
            st.write(section["content"], unsafe_allow_html=True)
            st.image(section["chart"], use_column_width=True)

        # 提供下载链接
        report_html = generate_report_html(report)
        b64 = base64.b64encode(report_html.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="monthly_report.html">下载报告</a>'
        st.markdown(href, unsafe_allow_html=True)

def generate_report_html(report):
    html = f"<html><head><title>{report['title']}</title></head><body>"
    html += f"<h1>{report['title']}</h1>"

    for section in report["sections"]:
        html += f"<h2>{section['title']}</h2>"
        html += section["content"]
        img_base64 = base64.b64encode(section["chart"].getvalue()).decode()
        html += f'<img src="data:image/png;base64,{img_base64}" />'

    html += "</body></html>"
    return html