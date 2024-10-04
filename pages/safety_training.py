# pages/safety_training.py

"""
此文件包含安全培训页面的渲染逻辑。
主要功能包括:
1. 显示可用的培训课程
2. 进行培训和测试
3. 显示用户的培训记录

作者: [您的名字]
创建日期: [创建日期]
最后修改日期: [最后修改日期]
"""

import streamlit as st
from modules import safety_training

def render():
    """渲染安全培训页面的主函数"""
    st.title("安全培训")

    # 显示可用的培训课程
    st.subheader("可用培训课程")
    courses = safety_training.get_available_courses()
    for course in courses:
        st.write(f"**{course['title']}**")
        st.write(course['description'])
        if st.button("开始培训", key=f"start_{course['id']}"):
            # 将当前课程ID存储在会话状态中
            st.session_state.current_course = course['id']
            st.experimental_rerun()

    # 显示当前进行的培训
    if 'current_course' in st.session_state:
        course = safety_training.get_course(st.session_state.current_course)
        st.subheader(f"当前培训: {course['title']}")
        
        # 显示培训内容
        st.write(course['content'])
        
        # 显示测试题
        st.subheader("测试")
        questions = safety_training.get_course_questions(st.session_state.current_course)
        user_answers = {}
        for q in questions:
            user_answers[q['id']] = st.radio(q['question'], q['options'])
        
        if st.button("提交答案"):
            # 评估用户答案并显示结果
            score = safety_training.evaluate_answers(st.session_state.current_course, user_answers)
            if score >= 80:
                st.success(f"恭喜！您通过了测试，得分：{score}分")
                safety_training.mark_course_completed(st.session_state.user['id'], st.session_state.current_course)
            else:
                st.error(f"很遗憾，您没有通过测试，得分：{score}分。请重新学习后再次尝试。")
            # 清除当前课程状态
            del st.session_state.current_course

    # 显示用户的培训记录
    st.subheader("我的培训记录")
    training_records = safety_training.get_user_training_records(st.session_state.user['id'])
    for record in training_records:
        st.write(f"**{record['course_title']}**")
        st.write(f"完成日期: {record['completion_date']}")
        st.write(f"得分: {record['score']}")
        st.write("---")