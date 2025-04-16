"""
Student management UI component.
"""
import streamlit as st
from app.services.student_service import StudentService

def render_student_management():
    """Render the student management section of the UI"""
    st.header("Student Management")
    
    # Add new student form
    st.subheader("Add a New Student")
    with st.form("add_student_form"):
        col1, col2 = st.columns(2)
        with col1:
            enrollment_code = st.text_input(
                "Enrollment Code (3 digits)", 
                max_chars=3,
                help="3-digit enrollment code for student ID generation"
            )
            student_name = st.text_input(
                "Student Name",
                help="Full name of the student"
            )
        with col2:
            student_email = st.text_input(
                "Student Email",
                help="Will be converted to @outlook.com format"
            )
        
        submitted = st.form_submit_button("Add Student")
        
        if submitted:
            if not enrollment_code or not student_name or not student_email:
                st.error("Please fill in all fields")
            else:
                success, message = StudentService.add_student(
                    student_name, student_email, enrollment_code
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    # Show existing students
    st.subheader("Existing Students")
    
    # Refresh button and search
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Refresh List"):
            # This will trigger a refresh of the DataFrame when clicked
            pass
    with col2:
        search_term = st.text_input("Search by name or ID:", "")
    
    # Get students data
    students_df = StudentService.get_all_students()
    
    # Filter by search term if provided
    if search_term and not students_df.empty:
        filtered_df = students_df[
            students_df['student_id'].str.contains(search_term, case=False) | 
            students_df['name'].str.contains(search_term, case=False)
        ]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(students_df, use_container_width=True)
    
    # Update/Delete student section
    st.subheader("Update or Delete a Student")
    st.info("Enter the student's current ID and the new information to update, or just the ID to delete.")
    
    col1, col2 = st.columns(2)
    with col1:
        old_student_id = st.text_input("Current Student ID (e.g., 201-1234)")
        new_student_id = st.text_input("New Student ID (same format)", key="new_sid")
    with col2:
        update_name = st.text_input("New Name")
        update_email = st.text_input("New Email")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Update Student"):
            if old_student_id:
                success, message = StudentService.update_student(
                    old_student_id, new_student_id, update_name, update_email
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.error("Please enter the current Student ID to update")
    
    with col2:
        if st.button("Delete Student", type="primary"):
            if old_student_id:
                # Add a confirmation step
                confirm = st.checkbox("I confirm that I want to delete this student and all their grades")
                if confirm:
                    success, message = StudentService.delete_student(old_student_id)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.warning("Please confirm deletion")
            else:
                st.error("Please enter the Student ID to delete") 