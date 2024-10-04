"""
数据分析模块

该模块提供了一系列数据分析工具和功能，包括描述性统计、相关性分析、回归分析、
预测模型、聚类分析等。它还集成了项目管理、库存管理和用户行为分析等功能。

主要功能:
1. 基础统计分析
2. 预测分析（支出、库存需求）
3. 项目成功因素分析
4. 用户行为聚类分析
5. 综合洞察生成

设计思路:
1. 提供各种数据分析工具和算法
2. 实现数据可视化功能（待实现）
3. 支持自定义分析脚本执行（待实现）
4. 集成机器学习模型训练和预测
5. 处理大规模数据集和分布式计算（待优化）

依赖:
- pandas: 数据处理
- numpy: 数值计算
- scikit-learn: 机器学习算法
- 自定义模块: inventory_management, financial_management, project_management, user_management
- 自定义工具: database
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
from sklearn.cluster import KMeans
from modules import inventory_management, financial_management, project_management, user_management
from utils import database
from datetime import datetime, timedelta

def descriptive_statistics(data):
    """
    计算并返回数据的描述性统计信息
    
    参数:
    data (pandas.DataFrame): 输入数据

    返回:
    pandas.DataFrame: 包含描述性统计信息的DataFrame
    """
    return data.describe()

def correlation_analysis(data):
    """
    计算并返回数据各列之间的相关性

    参数:
    data (pandas.DataFrame): 输入数据

    返回:
    pandas.DataFrame: 相关性矩阵
    """
    return data.corr()

def simple_regression(data, x_column, y_column):
    """
    执行简单线性回归分析

    参数:
    data (pandas.DataFrame): 输入数据
    x_column (str): 自变量列名
    y_column (str): 因变量列名

    返回:
    sklearn.linear_model.LinearRegression: 训练好的线性回归模型
    """
    X = data[[x_column]]
    y = data[y_column]
    model = LinearRegression()
    model.fit(X, y)
    return model

def save_analysis_result(user_id, analysis_type, file_name):
    """
    保存分析结果到数据库

    参数:
    user_id (int): 用户ID
    analysis_type (str): 分析类型
    file_name (str): 结果文件名

    返回:
    bool: 保存成功返回True，否则返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO analysis_history (user_id, analysis_type, file_name, timestamp) VALUES (?, ?, ?, ?)",
                  (user_id, analysis_type, file_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_analysis_history(user_id):
    """
    获取用户的分析历史记录

    参数:
    user_id (int): 用户ID

    返回:
    list: 包含分析历史记录的字典列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT analysis_type, file_name, timestamp FROM analysis_history WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    history = c.fetchall()
    return [{'analysis_type': h[0], 'file_name': h[1], 'timestamp': h[2]} for h in history]

def predict_future_expenses(months_ahead=3):
    """
    预测未来几个月的支出

    参数:
    months_ahead (int): 预测未来的月数，默认为3

    返回:
    dict: 包含预测结果、模型评估指标和预测日期的字典
    """
    financial_data = financial_management.get_monthly_trend()
    
    # 准备特征
    X = financial_data.index.astype(int).values.reshape(-1, 1)  # 使用时间作为特征
    y = financial_data['expense'].values

    # 分割数据
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练随机森林模型
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 评估模型
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # 预测未来支出
    last_date = financial_data.index[-1]
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=months_ahead, freq='M')
    future_X = future_dates.astype(int).values.reshape(-1, 1)
    future_expenses = model.predict(future_X)

    return {
        'predictions': future_expenses,
        'mse': mse,
        'r2': r2,
        'dates': future_dates
    }

def predict_inventory_needs():
    """
    预测未来的库存需求

    返回:
    dict: 包含每种物品预测需求量和模型评估指标的字典
    """
    inventory_usage = inventory_management.get_inventory_usage_history()
    
    predictions = {}
    for item in inventory_usage:
        if len(item['usage_history']) > 12:  # 只预测有足够历史数据的物品
            # 准备特征
            X = np.array(range(len(item['usage_history']))).reshape(-1, 1)
            y = np.array(item['usage_history'])
            
            # 分割数据
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # 训练随机森林模型
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # 评估模型
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # 预测下个月的需求
            next_month_prediction = model.predict([[len(item['usage_history'])]])
            predictions[item['name']] = {
                'prediction': next_month_prediction[0],
                'mse': mse,
                'r2': r2
            }
    
    return predictions

def analyze_project_success_factors():
    """
    分析影响项目成功的因素

    返回:
    dict: 包含模型准确率、分类报告和特征重要性的字典
    """
    projects = project_management.get_all_projects_with_details()
    
    # 准备特征和目标变量
    X = []
    y = []
    for project in projects:
        X.append([
            project['budget'],
            project['team_size'],
            (project['end_date'] - project['start_date']).days,  # 项目持续时间
            len(project['tasks']),  # 任务数量
        ])
        y.append(1 if project['status'] == 'completed' and project['on_time'] and project['within_budget'] else 0)
    
    X = np.array(X)
    y = np.array(y)
    
    # 分割数据
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 训练随机森林分类器
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 评估模型
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    # 特征重要性
    feature_importance = model.feature_importances_
    features = ['预算', '团队规模', '项目持续时间', '任务数量']
    
    return {
        'accuracy': accuracy,
        'classification_report': report,
        'feature_importance': dict(zip(features, feature_importance))
    }

def analyze_user_behavior():
    """
    分析用户行为并进行聚类

    返回:
    dict: 包含用户聚类结果和聚类中心的字典
    """
    user_activity = user_management.get_user_activity()
    
    # 准备数据
    X = np.array([[u['financial_transactions'], u['events_created'], u['inventory_usages'], u['completed_trainings']] for u in user_activity])
    
    # 标准化数据
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 使用K-means聚类
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    
    # 添加聚类结果到原始数据
    for i, u in enumerate(user_activity):
        u['cluster'] = clusters[i]
    
    # 计算每个聚类的中心点
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    
    return {
        'user_clusters': user_activity,
        'cluster_centers': cluster_centers
    }

def generate_insights():
    """
    生成综合洞察报告

    返回:
    list: 包含各种洞察的字符串列表
    """
    insights = []

    # 支出预测洞察
    expense_prediction = predict_future_expenses()
    avg_predicted_expense = np.mean(expense_prediction['predictions'])
    insights.append(f"未来3个月的平均预计支出为 ¥{avg_predicted_expense:.2f}。模型的 R² 值为 {expense_prediction['r2']:.2f}，表明预测的可信度较高。")

    # 库存需求预测洞察
    inventory_predictions = predict_inventory_needs()
    high_demand_items = [item for item, data in inventory_predictions.items() if data['prediction'] > np.mean([d['prediction'] for d in inventory_predictions.values()])]
    insights.append(f"以下物品预计下个月需求较高：{', '.join(high_demand_items)}。请考虑提前补充库存。")

    # 项目成功因素洞察
    project_analysis = analyze_project_success_factors()
    most_important_factor = max(project_analysis['feature_importance'], key=project_analysis['feature_importance'].get)
    insights.append(f"项目成功的最重要因素是{most_important_factor}。模型的准确率为 {project_analysis['accuracy']:.2f}。")

    # 用户行为洞察
    user_behavior = analyze_user_behavior()
    most_active_cluster = np.argmax([np.sum(center) for center in user_behavior['cluster_centers']])
    insights.append(f"用户可以分为3个群组，其中群组{most_active_cluster + 1}的用户最活跃。考虑为不同群组的用户制定不同的参与策略。")

    return insights