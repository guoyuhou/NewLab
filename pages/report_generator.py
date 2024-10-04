# pages/report_generator.py

import streamlit as st
from modules import report_generation
import pandas as pd

def render():
    st.title("报告生成器")

    # 选择报告类型
    report_type = st.selectbox("选择报告类型", ["实验报告", "项目进度报告", "设备使用报告"])

    if report_type == "实验报告":
        experiment_name = st.text_input("实验名称")
        experiment_date = st.date_input("实验日期")
        experiment_description = st.text_area("实验描述")
        experiment_results = st.text_area("实验结果")
        
        if st.button("生成实验报告"):
            report = report_generation.generate_experiment_report(
                st.session_state.user['id'], experiment_name, experiment_date, 
                experiment_description, experiment_results
            )
            st.success("实验报告生成成功！")
            st.download_button("下载报告", report, file_name="experiment_report.pdf")

    elif report_type == "项目进度报告":
        projects = report_generation.get_user_projects(st.session_state.user['id'])
        selected_project = st.selectbox("选择项目", [p['name'] for p in projects])
        report_period = st.date_input("报告周期", [pd.Timestamp.now().date() - pd.Timedelta(days=30), pd.Timestamp.now().date()])
        
        if st.button("生成项目进度报告"):
            report = report_generation.generate_project_progress_report(
                st.session_state.user['id'], selected_project, report_period[0], report_period[1]
            )
            st.success("项目进度报告生成成功！")
            st.download_button("下载报告", report, file_name="project_progress_report.pdf")

    elif report_type == "设备使用报告":
        equipment = report_generation.get_lab_equipment()
        selected_equipment = st.selectbox("选择设备", [e['name'] for e in equipment])
        report_period = st.date_input("报告周期", [pd.Timestamp.now().date() - pd.Timedelta(days=30), pd.Timestamp.now().date()])
        
        if st.button("生成设备使用报告"):
            report = report_generation.generate_equipment_usage_report(
                selected_equipment, report_period[0], report_period[1]
            )
            st.success("设备使用报告生成成功！")
            st.download_button("下载报告", report, file_name="equipment_usage_report.pdf")

    # 显示历史报告
    st.subheader("历史报告")
    historical_reports = report_generation.get_historical_reports(st.session_state.user['id'])
    for report in historical_reports:
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.write(report['type'])
        col2.write(report['date'])
        col3.download_button("下载", report['content'], file_name=f"{report['type']}_{report['date']}.pdf")