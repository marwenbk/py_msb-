"""
Student Grades Tracker - Main Application

This Streamlit application provides a user-friendly interface for tracking student grades,
with features for managing students, courses, grades, and analytics.
"""
import streamlit as st
from app.config import apply_styling
from app.ui.student_ui import render_student_management
from app.ui.course_ui import render_course_management
from app.ui.grade_ui import render_grade_management
from app.ui.analytics_ui import render_analytics
from app.ui.db_ui import render_db_setup

def main():
    """Main application entry point"""
    # Set page config - MUST be first Streamlit command
    st.set_page_config(
        page_title="Student Grades Tracker",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply consistent styling
    apply_styling()
    
    # Initialize session state for navigation if it doesn't exist
    if "navigation" not in st.session_state:
        st.session_state.navigation = "🏠 Dashboard"
    
    # Application title
    st.title("Student Grades Tracker")
    
    # Sidebar navigation with icons
    st.sidebar.title("Navigation")
    
    # Use session state for menu selection to maintain state across reruns
    menu = st.sidebar.radio(
        "Select a Section:",
        [
            "🏠 Dashboard",
            "👨‍🎓 Student Management",
            "📚 Course Management",
            "📝 Grades Management",
            "📊 Analytics & Reporting",
            "⚙️ Database Setup"
        ],
        index=0 if st.session_state.navigation == "🏠 Dashboard" else
              1 if st.session_state.navigation == "👨‍🎓 Student Management" else
              2 if st.session_state.navigation == "📚 Course Management" else
              3 if st.session_state.navigation == "📝 Grades Management" else
              4 if st.session_state.navigation == "📊 Analytics & Reporting" else
              5
    )
    
    # Update navigation state based on sidebar selection
    st.session_state.navigation = menu
    
    # Route to the appropriate UI component based on menu selection
    if menu == "🏠 Dashboard":
        render_dashboard()
    elif menu == "👨‍🎓 Student Management":
        render_student_management()
    elif menu == "📚 Course Management":
        render_course_management()
    elif menu == "📝 Grades Management":
        render_grade_management()
    elif menu == "📊 Analytics & Reporting":
        render_analytics()
    elif menu == "⚙️ Database Setup":
        render_db_setup()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.caption("Student Grades Tracker v1.0")
    st.sidebar.caption("© 2023 Educational Tools")

def render_dashboard():
    """Render the dashboard/home screen"""
    st.header("Dashboard")
    
    # Welcome message and application overview
    st.markdown("""
    ## Welcome to the Student Grades Tracker!
    
    This application helps you manage and analyze student grades efficiently.
    
    ### Key Features:
    """)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 👨‍🎓 Student Management
        - Add new students
        - Update student information
        - Delete students
        """)
        if st.button("Go to Student Management"):
            st.session_state.navigation = "👨‍🎓 Student Management"
            st.experimental_rerun()
    
    with col2:
        st.markdown("""
        ### 📚 Course Management
        - Add new courses
        - Update course details
        - Delete courses
        """)
        if st.button("Go to Course Management"):
            st.session_state.navigation = "📚 Course Management"
            st.experimental_rerun()
    
    with col3:
        st.markdown("""
        ### 📝 Grade Management
        - Assign grades
        - Update existing grades
        - Delete grades
        """)
        if st.button("Go to Grade Management"):
            st.session_state.navigation = "📝 Grades Management"
            st.experimental_rerun()
    
    # Analytics preview
    st.markdown("---")
    st.subheader("📊 Analytics & Reporting")
    st.markdown("""
    Get valuable insights from your data:
    - Student GPA calculations
    - Performance distribution
    - Course analytics
    - At-risk student identification
    """)
    if st.button("Go to Analytics"):
        st.session_state.navigation = "📊 Analytics & Reporting"
        st.experimental_rerun()
    
    # Getting started guide
    st.markdown("---")
    st.subheader("Getting Started")
    
    with st.expander("First-time User? Follow these steps:"):
        st.markdown("""
        1. First, go to **Database Setup** and create the tables with sample data.
        2. Navigate to **Student Management** to view and manage students.
        3. Check out **Course Management** to view and manage courses.
        4. Use **Grades Management** to assign grades to students.
        5. Finally, view **Analytics & Reporting** to see insights about student performance.
        """)
        if st.button("Go to Database Setup"):
            st.session_state.navigation = "⚙️ Database Setup"
            st.experimental_rerun()

if __name__ == "__main__":
    main() 