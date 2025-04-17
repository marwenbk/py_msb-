"""
Grade management UI component.
"""
import streamlit as st
import pandas as pd
from app.services.grade_service import GradeService
from app.services.student_service import StudentService
from app.services.course_service import CourseService

def render_grade_management():
    """Render the grade management section of the UI"""
    st.header("Grades Management")
    
    # Get students and courses for selection
    students_df = StudentService.get_all_students()
    courses_df = CourseService.get_all_courses()
    
    # Check if we have both students and courses
    if students_df.empty or courses_df.empty:
        st.warning("You need to add both students and courses before managing grades.")
        
        if students_df.empty:
            st.error("No students found. Please add students first.")
            
        if courses_df.empty:
            st.error("No courses found. Please add courses first.")
            
        return
    
    # Assign Grade Form
    st.subheader("Assign Grade to Student")
    with st.form("assign_grade_form"):
        col1, col2 = st.columns(2)
        with col1:
            # Student selection with search
            student_search = st.text_input("Search student by name or ID:", "")
            if student_search:
                filtered_students = students_df[
                    students_df['student_id'].str.contains(student_search, case=False) | 
                    students_df['name'].str.contains(student_search, case=False)
                ]
            else:
                filtered_students = students_df
                
            student_option = st.selectbox(
                "Select Student",
                filtered_students['student_id'].tolist(),
                format_func=lambda x: f"{x}: {filtered_students.loc[filtered_students['student_id'] == x, 'name'].values[0]}"
            )
        
        with col2:
            # Course selection with search
            course_search = st.text_input("Search course by name or code:", "")
            if course_search:
                filtered_courses = courses_df[
                    courses_df['name'].str.contains(course_search, case=False) | 
                    courses_df['code'].str.contains(course_search, case=False)
                ]
            else:
                filtered_courses = courses_df
                
            course_option = st.selectbox(
                "Select Course",
                filtered_courses['id'].tolist(),
                format_func=lambda x: f"{filtered_courses.loc[filtered_courses['id'] == x, 'name'].values[0]} ({filtered_courses.loc[filtered_courses['id'] == x, 'code'].values[0]})"
            )
        
        # Grade value with visual indicator
        grade_value = st.slider(
            "Grade (0–100)",
            min_value=0.0,
            max_value=100.0,
            value=75.0,
            step=0.5,
            help="Slide to select grade"
        )
        
        # Visual grade indicator
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Raw Grade", f"{grade_value}/100")
        with col2:
            # Convert to letter grade
            letter_grade = "A" if grade_value >= 90 else "B" if grade_value >= 80 else "C" if grade_value >= 70 else "D" if grade_value >= 60 else "F"
            st.metric("Letter Grade", letter_grade)
        with col3:
            # Convert to GPA
            gpa = 4.0 if grade_value >= 90 else 3.0 if grade_value >= 80 else 2.0 if grade_value >= 70 else 1.0 if grade_value >= 60 else 0.0
            st.metric("GPA Equivalent", gpa)
            
        submitted = st.form_submit_button("Assign Grade")
        
        if submitted:
            success, message = GradeService.add_grade(
                student_option, course_option, grade_value
            )
            if success:
                st.success(message)
            else:
                st.error(message)
    
    # Show existing grades
    st.subheader("Existing Grades")
    
    # Refresh button and search
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Refresh List"):
            # This will trigger a refresh of the DataFrame when clicked
            pass
    with col2:
        search_term = st.text_input("Search grades by student or course:", "")
    
    # Get grades data
    grades_df = GradeService.get_all_grades()
    
    # Filter by search term if provided
    if search_term and not grades_df.empty:
        filtered_df = grades_df[
            grades_df['student_name'].str.contains(search_term, case=False) | 
            grades_df['course_name'].str.contains(search_term, case=False) |
            grades_df['student_id'].str.contains(search_term, case=False)
        ]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(grades_df, use_container_width=True)
    
    # Grade Management by ID
    st.subheader("Update or Delete Grade by ID")
    
    # Grade selection
    grades = GradeService.get_all_grades()
    grade_ids = grades['id'].tolist() if not grades.empty else []
    
    if grade_ids:
        grade_id = st.selectbox(
            "Select Grade ID",
            options=grade_ids,
            format_func=lambda x: f"ID {x}: {grades.loc[grades['id'] == x, 'student_name'].values[0]} - {grades.loc[grades['id'] == x, 'course_name'].values[0]} (Current: {grades.loc[grades['id'] == x, 'raw_grade'].values[0]})"
        )
        
        # Grade update form
        update_grade_value = st.slider(
            "New Grade Value (0–100)",
            min_value=0.0,
            max_value=100.0,
            value=float(grades.loc[grades['id'] == grade_id, 'raw_grade'].values[0]) if grade_id else 75.0,
            step=0.5
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Update Grade"):
                if grade_id:
                    success, message = GradeService.update_grade(
                        grade_id, update_grade_value
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("Please select a grade to update")
        
        with col2:
            if st.button("Delete Grade", type="primary"):
                if grade_id:
                    confirm = st.checkbox("I confirm that I want to delete this grade")
                    if confirm:
                        success, message = GradeService.delete_grade(grade_id)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.warning("Please confirm deletion")
                else:
                    st.error("Please select a grade to delete")
    else:
        st.warning("No grades available. Please assign grades first.")
    
    # Update Grade by Student & Course
    st.subheader("Update Grade by Student & Course")
    
    with st.form("update_grade_by_sc"):
        # Show student and course selects
        col1, col2 = st.columns(2)
        with col1:
            student_id_sc = st.selectbox(
                "Select Student",
                students_df['student_id'].tolist(),
                format_func=lambda x: f"{x}: {students_df.loc[students_df['student_id'] == x, 'name'].values[0]}"
            )
        with col2:
            course_id_sc = st.selectbox(
                "Select Course",
                courses_df['id'].tolist(),
                format_func=lambda x: f"{courses_df.loc[courses_df['id'] == x, 'name'].values[0]} ({courses_df.loc[courses_df['id'] == x, 'code'].values[0]})"
            )
        
        # Try to find existing grade
        existing_grade = None
        if not grades_df.empty:
            existing_grade = grades_df[
                (grades_df['student_id'] == student_id_sc) & 
                (grades_df['course_id'] == course_id_sc)
            ]
        
        # Show current grade if exists
        if existing_grade is not None and not existing_grade.empty:
            st.info(f"Current grade: {existing_grade.iloc[0]['raw_grade']} ({existing_grade.iloc[0]['letter']})")
            
        # Grade slider
        new_grade_sc = st.slider(
            "New Grade (0–100)",
            min_value=0.0,
            max_value=100.0,
            value=float(existing_grade.iloc[0]['raw_grade']) if existing_grade is not None and not existing_grade.empty else 75.0,
            step=0.5
        )
        
        submitted_sc = st.form_submit_button("Update Grade by Student & Course")
        
        if submitted_sc:
            success, message = GradeService.update_grade_by_student_course(
                student_id_sc, course_id_sc, new_grade_sc
            )
            if success:
                st.success(message)
            else:
                st.error(message) 