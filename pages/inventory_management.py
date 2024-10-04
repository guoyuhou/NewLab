"""
库存管理页面

本模块实现了实验室管理系统的库存管理功能。
主要功能包括：
1. 添加新物品到库存
2. 显示和更新现有库存
3. 显示库存警报
4. 记录和显示库存使用情况
5. 添加库存使用记录

作者: [您的名字]
创建日期: [创建日期]
最后修改日期: [最后修改日期]
"""

import streamlit as st
from modules import inventory_management, user_management

def render():
    # 检查用户权限
    if not user_management.has_permission(st.session_state.user['id'], 'manage_inventory'):
        st.error("您没有权限访问此页面。")
        return

    st.title("库存管理")

    # 添加新物品
    st.subheader("添加新物品")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("物品名称")
        category = st.selectbox("类别", ["试剂", "耗材", "设备", "其他"])
    with col2:
        quantity = st.number_input("数量", min_value=0, step=1)
        unit = st.text_input("单位 (如: 个, 瓶, 盒)")

    # 处理添加物品的请求
    if st.button("添加物品"):
        if inventory_management.add_item(name, category, quantity, unit):
            st.success(f"成功添加 {quantity} {unit} {name}")
        else:
            st.error("添加物品失败，请重试。")

    # 显示库存列表
    st.subheader("库存列表")
    items = inventory_management.get_all_items()
    for item in items:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        col1.write(f"**{item['name']}** ({item['category']})")
        col2.write(f"{item['quantity']} {item['unit']}")
        new_quantity = col3.number_input("新数量", min_value=0, step=1, value=item['quantity'], key=f"quantity_{item['id']}")
        
        # 处理更新物品数量的请求
        if col4.button("更新", key=f"update_{item['id']}"):
            if inventory_management.update_item_quantity(item['id'], new_quantity):
                st.success(f"已更新 {item['name']} 的数量为 {new_quantity} {item['unit']}")
            else:
                st.error("更新数量失败，请重试。")

    # 显示库存警报
    st.subheader("库存警报")
    low_stock_items = inventory_management.get_low_stock_items()
    if low_stock_items:
        for item in low_stock_items:
            st.warning(f"{item['name']} 库存不足，当前数量: {item['quantity']} {item['unit']}")
    else:
        st.info("目前没有库存不足的物品。")

    # 显示库存使用记录
    st.subheader("库存使用记录")
    usage_records = inventory_management.get_usage_records()
    for record in usage_records:
        st.write(f"{record['timestamp']} - {record['user']} 使用了 {record['quantity']} {record['unit']} {record['item_name']}")

    # 添加使用记录
    st.subheader("添加使用记录")
    col1, col2, col3 = st.columns(3)
    with col1:
        item_id = st.selectbox("选择物品", [(item['id'], item['name']) for item in items], format_func=lambda x: x[1])
    with col2:
        used_quantity = st.number_input("使用数量", min_value=0, step=1)
    with col3:
        st.write("")
        st.write("")
        # 处理添加使用记录的请求
        if st.button("记录使用"):
            if inventory_management.add_usage_record(st.session_state.user['id'], item_id[0], used_quantity):
                st.success("使用记录已添加")
            else:
                st.error("添加使用记录失败，请重试。")