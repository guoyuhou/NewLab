# pages/data_export.py

import streamlit as st
import pandas as pd
from modules import inventory_management, financial_management, project_management, user_management
from io import BytesIO
import xlsxwriter

def render():
    st.title("数据导出")

    export_options = {
        "库存报告": inventory_management.get_inventory_report,
        "财务报告": financial_management.get_financial_report,
        "项目报告": project_management.get_project_report,
        "用户活动报告": user_management.get_user_activity_report
    }

    selected_report = st.selectbox("选择要导出的报告", list(export_options.keys()))

    if st.button("生成报告"):
        report_data = export_options[selected_report]()
        
        # 创建 Excel 文件
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # 写入数据
        for i, col in enumerate(report_data.columns):
            worksheet.write(0, i, col)
        for i, row in enumerate(report_data.values):
            for j, value in enumerate(row):
                worksheet.write(i+1, j, value)

        workbook.close()
        output.seek(0)

        # 提供下载链接
        st.download_button(
            label="下载 Excel 报告",
            data=output,
            file_name=f"{selected_report}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
