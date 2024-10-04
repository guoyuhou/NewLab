# pages/tools.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from modules import data_analysis

def render():
    st.title("数据分析工具")

    # 文件上传
    uploaded_file = st.file_uploader("上传CSV文件", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("数据预览:")
        st.write(data.head())

        # 选择分析类型
        analysis_type = st.selectbox("选择分析类型", ["描述性统计", "相关性分析", "简单回归分析"])

        if analysis_type == "描述性统计":
            st.write(data_analysis.descriptive_statistics(data))

        elif analysis_type == "相关性分析":
            correlation_matrix = data_analysis.correlation_analysis(data)
            fig, ax = plt.subplots()
            im = ax.imshow(correlation_matrix, cmap="coolwarm")
            ax.set_xticks(range(len(data.columns)))
            ax.set_yticks(range(len(data.columns)))
            ax.set_xticklabels(data.columns, rotation=45, ha="right")
            ax.set_yticklabels(data.columns)
            plt.colorbar(im)
            st.pyplot(fig)

        elif analysis_type == "简单回归分析":
            x_column = st.selectbox("选择自变量", data.columns)
            y_column = st.selectbox("选择因变量", data.columns)
            result = data_analysis.simple_regression(data, x_column, y_column)
            st.write(result)
            
            # 绘制回归图
            fig, ax = plt.subplots()
            ax.scatter(data[x_column], data[y_column])
            ax.plot(data[x_column], result.predict(data[[x_column]]), color='red')
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            ax.set_title(f"{y_column} vs {x_column}")
            st.pyplot(fig)

    # 添加保存分析结果的功能
    if st.button("保存分析结果"):
        if data_analysis.save_analysis_result(st.session_state.user['id'], analysis_type, uploaded_file.name):
            st.success("分析结果已保存！")
        else:
            st.error("保存分析结果失败，请重试。")

    # 显示历史分析记录
    st.subheader("历史分析记录")
    history = data_analysis.get_analysis_history(st.session_state.user['id'])
    for record in history:
        st.write(f"分析类型: {record['analysis_type']}, 文件名: {record['file_name']}, 时间: {record['timestamp']}")