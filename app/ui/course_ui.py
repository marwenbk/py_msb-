"""
Course management UI component.
"""
import streamlit as st
from app.services.course_service import CourseService

def render_course_management():
    """Render the course management section of the UI"""
    st.header("Course Management")
    
    # Add new course form
    st.subheader("Add a New Course")
    with st.form("add_course_form"):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            course_name = st.text_input(
                "Course Name",
                help="Full name of the course"
            )
        with col2:
            course_code = st.text_input(
                "Course Code (Unique)",
                help="Unique identifier for the course (e.g., MATH101)"
            )
        with col3:
            course_credits = st.number_input(
                "Credits",
                min_value=1,
                max_value=6,
                value=3,
                step=1,
                help="Number of credit hours"
            )
        
        submitted = st.form_submit_button("Add Course")
        
        if submitted:
            if not course_name or not course_code:
                st.error("Please fill in all fields")
            else:
                success, message = CourseService.add_course(
                    course_name, course_code, course_credits
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    # Show existing courses
    st.subheader("Existing Courses")
    
    # Refresh button and search
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Refresh List"):
            # This will trigger a refresh of the DataFrame when clicked
            pass
    with col2:
        search_term = st.text_input("Search by name or code:", "")
    
    # Get courses data
    courses_df = CourseService.get_all_courses()
    
    # Filter by search term if provided
    if search_term and not courses_df.empty:
        filtered_df = courses_df[
            courses_df['name'].str.contains(search_term, case=False) | 
            courses_df['code'].str.contains(search_term, case=False)
        ]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(courses_df, use_container_width=True)
    
    # Update/Delete course section
    st.subheader("Update or Delete a Course")
    st.info("Select a course ID to update or delete.")
    
    # Course selection for update/delete
    courses = CourseService.get_all_courses()
    course_ids = courses['id'].tolist() if not courses.empty else []
    
    if course_ids:
        course_id = st.selectbox(
            "Select Course ID",
            options=course_ids,
            format_func=lambda x: f"{x}: {courses.loc[courses['id'] == x, 'name'].values[0]} ({courses.loc[courses['id'] == x, 'code'].values[0]})"
        )
        
        # Show course details and update form
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            update_name = st.text_input(
                "New Course Name",
                value=courses.loc[courses['id'] == course_id, 'name'].values[0] if course_id else ""
            )
        with col2:
            update_code = st.text_input(
                "New Course Code",
                value=courses.loc[courses['id'] == course_id, 'code'].values[0] if course_id else ""
            )
        with col3:
            update_credits = st.number_input(
                "New Credits",
                min_value=1,
                max_value=6,
                value=int(courses.loc[courses['id'] == course_id, 'credits'].values[0]) if course_id else 3,
                step=1
            )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Update Course"):
                if course_id:
                    success, message = CourseService.update_course(
                        course_id, update_name, update_code, update_credits
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("Please select a course to update")
        
        with col2:
            if st.button("Delete Course", type="primary"):
                if course_id:
                    # Add a confirmation step
                    confirm = st.checkbox("I confirm that I want to delete this course and all associated grades")
                    if confirm:
                        success, message = CourseService.delete_course(course_id)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.warning("Please confirm deletion")
                else:
                    st.error("Please select a course to delete")
    else:
        st.warning("No courses available. Please add a course first.") 