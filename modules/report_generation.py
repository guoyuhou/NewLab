"""
modules/report_generation.py

这个模块负责生成各种实验室报告,包括实验报告、项目进度报告、设备使用报告和月度报告等。
它提供了多个函数来生成不同类型的报告,并包含了一些辅助函数来获取数据和生成图表。

主要功能:
1. 生成各种类型的报告
2. 保存和检索报告
3. 生成报告相关的图表
4. 获取用户项目和实验室设备信息
"""

from utils import database
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import matplotlib.pyplot as plt
import io
from modules import inventory_management, financial_management, project_management, data_analysis

def generate_experiment_report(user_id, name, date, description, results):
    """
    生成实验报告并保存
    
    参数:
    user_id (int): 用户ID
    name (str): 实验名称
    date (str): 实验日期
    description (str): 实验描述
    results (str): 实验结果
    
    返回:
    bytes: 生成的PDF报告内容
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    c.drawString(100, 750, f"实验报告: {name}")
    c.drawString(100, 730, f"日期: {date}")
    c.drawString(100, 710, f"描述: {description}")
    c.drawString(100, 690, f"结果: {results}")
    
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    
    save_report(user_id, "实验报告", pdf)
    return pdf

def generate_project_progress_report(user_id, project_name, start_date, end_date):
    """
    生成项目进度报告
    
    参数:
    user_id (int): 用户ID
    project_name (str): 项目名称
    start_date (str): 开始日期
    end_date (str): 结束日期
    """
    # 实现项目进度报告生成逻辑
    pass

def generate_equipment_usage_report(equipment_name, start_date, end_date):
    """
    生成设备使用报告
    
    参数:
    equipment_name (str): 设备名称
    start_date (str): 开始日期
    end_date (str): 结束日期
    """
    # 实现设备使用报告生成逻辑
    pass

def get_user_projects(user_id):
    """
    获取用户的所有项目
    
    参数:
    user_id (int): 用户ID
    
    返回:
    list: 包含项目ID和名称的字典列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM projects WHERE user_id = ?", (user_id,))
    projects = c.fetchall()
    return [{'id': p[0], 'name': p[1]} for p in projects]

def get_lab_equipment():
    """
    获取实验室所有设备
    
    返回:
    list: 包含设备ID和名称的字典列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM resources WHERE type = 'equipment'")
    equipment = c.fetchall()
    return [{'id': e[0], 'name': e[1]} for e in equipment]

def save_report(user_id, report_type, content):
    """
    保存报告到数据库
    
    参数:
    user_id (int): 用户ID
    report_type (str): 报告类型
    content (bytes): 报告内容
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO reports (user_id, type, date, content)
        VALUES (?, ?, ?, ?)
    """, (user_id, report_type, datetime.now().strftime("%Y-%m-%d"), content))
    conn.commit()

def get_historical_reports(user_id):
    """
    获取用户的历史报告
    
    参数:
    user_id (int): 用户ID
    
    返回:
    list: 包含报告类型、日期和内容的字典列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT type, date, content FROM reports WHERE user_id = ? ORDER BY date DESC", (user_id,))
    reports = c.fetchall()
    return [{'type': r[0], 'date': r[1], 'content': r[2]} for r in reports]

def generate_monthly_report():
    """
    生成月度报告
    
    返回:
    dict: 包含报告标题和各个部分内容的字典
    """
    report = {
        "title": f"实验室月度报告 - {datetime.now().strftime('%Y年%m月')}",
        "sections": []
    }

    # 库存概况
    inventory_data = inventory_management.get_all_items()
    inventory_df = pd.DataFrame(inventory_data)
    report["sections"].append({
        "title": "库存概况",
        "content": inventory_df.to_html(index=False),
        "chart": generate_inventory_chart(inventory_df)
    })

    # 财务概况
    financial_summary = financial_management.get_financial_summary()
    report["sections"].append({
        "title": "财务概况",
        "content": f"总收入: ¥{financial_summary['total_income']:.2f}<br>"
                   f"总支出: ¥{financial_summary['total_expense']:.2f}<br>"
                   f"结余: ¥{financial_summary['balance']:.2f}",
        "chart": generate_financial_chart(financial_summary)
    })

    # 项目进展
    projects = project_management.get_all_projects()
    projects_df = pd.DataFrame(projects)
    report["sections"].append({
        "title": "项目进展",
        "content": projects_df.to_html(index=False),
        "chart": generate_project_chart(projects_df)
    })

    # 预测分析
    future_expenses = data_analysis.predict_future_expenses()
    report["sections"].append({
        "title": "未来支出预测",
        "content": f"未来3个月预计支出: ¥{sum(future_expenses):.2f}",
        "chart": generate_prediction_chart(future_expenses)
    })

    return report

def generate_inventory_chart(inventory_df):
    """
    生成库存图表
    
    参数:
    inventory_df (DataFrame): 库存数据
    
    返回:
    BytesIO: 包含图表图像的字节流
    """
    plt.figure(figsize=(10, 6))
    plt.bar(inventory_df['name'], inventory_df['quantity'])
    plt.title("库存数量")
    plt.xlabel("物品名称")
    plt.ylabel("数量")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    return img_buf

def generate_financial_chart(financial_summary):
    """
    生成财务图表
    
    参数:
    financial_summary (dict): 财务摘要数据
    
    返回:
    BytesIO: 包含图表图像的字节流
    """
    plt.figure(figsize=(8, 8))
    plt.pie([financial_summary['total_income'], financial_summary['total_expense']], 
            labels=['收入', '支出'], autopct='%1.1f%%')
    plt.title("收支比例")
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    return img_buf

def generate_project_chart(projects_df):
    """
    生成项目状态图表
    
    参数:
    projects_df (DataFrame): 项目数据
    
    返回:
    BytesIO: 包含图表图像的字节流
    """
    status_counts = projects_df['status'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%')
    plt.title("项目状态分布")
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    return img_buf

def generate_prediction_chart(future_expenses):
    """
    生成未来支出预测图表
    
    参数:
    future_expenses (list): 未来支出预测数据
    
    返回:
    BytesIO: 包含图表图像的字节流
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(future_expenses) + 1), future_expenses, marker='o')
    plt.title("未来支出预测")
    plt.xlabel("月份")
    plt.ylabel("预计支出")
    plt.xticks(range(1, len(future_expenses) + 1))
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    return img_buf