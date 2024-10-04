"""
数据可视化与分析模块

本模块负责生成和展示实验室管理系统的各种数据可视化图表和分析结果。
它使用Streamlit库来创建交互式Web界面，并利用Plotly库绘制各种图表。

主要功能包括：
1. 库存数据可视化
2. 财务数据可视化
3. 项目进度可视化
4. 用户活跃度分析
5. 设备使用率分析
6. 安全培训完成情况
7. 未来支出预测
8. 库存需求预测
9. 项目成功因素分析
10. 用户行为分析

作者: [您的名字]
创建日期: [创建日期]
最后修改日期: [最后修改日期]
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from modules import inventory_management, financial_management, project_management, user_management, data_analysis
import pandas as pd

def render():
    st.title("数据可视化与分析")

    # 库存数据可视化
    st.subheader("库存概览")
    inventory_data = inventory_management.get_all_items()
    fig_inventory = px.bar(inventory_data, x='name', y='quantity', color='category',
                           title="库存数量",
                           labels={'name': '物品名称', 'quantity': '数量', 'category': '类别'})
    st.plotly_chart(fig_inventory)

    # 财务数据可视化
    st.subheader("财务概览")
    financial_summary = financial_management.get_financial_summary()
    fig_finance = go.Figure(data=[
        go.Bar(name='收入', x=['总额'], y=[financial_summary['total_income']]),
        go.Bar(name='支出', x=['总额'], y=[financial_summary['total_expense']])
    ])
    fig_finance.update_layout(title="收支概览", barmode='group')
    st.plotly_chart(fig_finance)

    # 支出分布饼图
    expense_distribution = financial_management.get_expense_distribution()
    fig_expense = px.pie(values=expense_distribution.values, names=expense_distribution.index,
                         title="支出分布")
    st.plotly_chart(fig_expense)

    # 月度收支趋势
    monthly_trend = financial_management.get_monthly_trend()
    fig_trend = px.line(monthly_trend, x=monthly_trend.index, y=['income', 'expense'],
                        title="月度收支趋势",
                        labels={'value': '金额', 'variable': '类型', 'month': '月份'})
    st.plotly_chart(fig_trend)

    # 项目进度可视化
    st.subheader("项目进度")
    projects = project_management.get_all_projects()
    project_data = pd.DataFrame(projects)
    fig_projects = px.timeline(project_data, x_start="start_date", x_end="end_date", y="name",
                               color="status", title="项目时间线",
                               labels={'name': '项目名称', 'start_date': '开始日期', 'end_date': '结束日期'})
    fig_projects.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_projects)

    # 用户活跃度可视化
    st.subheader("用户活跃度")
    user_activity = user_management.get_user_activity()
    fig_activity = px.bar(user_activity, x='username', y='activity_score',
                          title="用户活跃度",
                          labels={'username': '用户名', 'activity_score': '活跃度得分'})
    st.plotly_chart(fig_activity)

    # 实验室设备使用率
    st.subheader("设备使用率")
    equipment_usage = inventory_management.get_equipment_usage()
    fig_equipment = px.bar(equipment_usage, x='name', y='usage_rate',
                           title="设备使用率",
                           labels={'name': '设备名称', 'usage_rate': '使用率'})
    st.plotly_chart(fig_equipment)

    # 安全培训完成情况
    st.subheader("安全培训完成情况")
    training_completion = user_management.get_safety_training_completion()
    fig_training = px.pie(training_completion, values='count', names='status',
                          title="安全培训完成情况")
    st.plotly_chart(fig_training)

    # 预测未来支出
    st.subheader("预测未来支出")
    future_expenses = data_analysis.predict_future_expenses()
    fig_future_expenses = px.line(x=range(1, len(future_expenses) + 1), y=future_expenses,
                                  labels={'x': '未来月份', 'y': '预测支出'},
                                  title="未来3个月的预测支出")
    st.plotly_chart(fig_future_expenses)

    # 预测设备使用率
    st.subheader("预测设备使用率")
    predicted_usage = data_analysis.predict_equipment_usage()
    fig_predicted_usage = px.bar(predicted_usage, x='name', y='predicted_usage',
                                 labels={'name': '设备名称', 'predicted_usage': '预测使用率'},
                                 title="设备使用率预测")
    st.plotly_chart(fig_predicted_usage)

    # 添加新的分析结果
    st.header("高级数据分析")

    # 支出预测
    st.subheader("未来支出预测")
    expense_prediction = data_analysis.predict_future_expenses()
    fig_expense_prediction = px.line(x=expense_prediction['dates'], y=expense_prediction['predictions'],
                                     labels={'x': '日期', 'y': '预测支出'},
                                     title=f"未来3个月支出预测 (R² = {expense_prediction['r2']:.2f})")
    st.plotly_chart(fig_expense_prediction)

    # 库存需求预测
    st.subheader("库存需求预测")
    inventory_predictions = data_analysis.predict_inventory_needs()
    fig_inventory_prediction = px.bar(x=list(inventory_predictions.keys()), 
                                      y=[data['prediction'] for data in inventory_predictions.values()],
                                      labels={'x': '物品', 'y': '预测需求'},
                                      title="下个月物品需求预测")
    st.plotly_chart(fig_inventory_prediction)

    # 项目成功因素分析
    st.subheader("项目成功因素分析")
    project_analysis = data_analysis.analyze_project_success_factors()
    fig_project_factors = px.bar(x=list(project_analysis['feature_importance'].keys()),
                                 y=list(project_analysis['feature_importance'].values()),
                                 labels={'x': '因素', 'y': '重要性'},
                                 title=f"项目成功因素重要性 (模型准确率: {project_analysis['accuracy']:.2f})")
    st.plotly_chart(fig_project_factors)

    # 用户行为分析
    st.subheader("用户行为分析")
    user_behavior = data_analysis.analyze_user_behavior()
    fig_user_clusters = px.scatter_3d(
        pd.DataFrame(user_behavior['user_clusters']),
        x='financial_transactions',
        y='events_created',
        z='inventory_usages',
        color='cluster',
        hover_name='username',
        labels={'financial_transactions': '财务交易', 'events_created': '创建事件', 'inventory_usages': '库存使用'},
        title="用户行为聚类分析"
    )
    st.plotly_chart(fig_user_clusters)

    # 显示洞察
    st.header("数据洞察")
    insights = data_analysis.generate_insights()
    for insight in insights:
        st.info(insight)