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
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from app.services.grade_service import GradeService

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
    """)
    
    # Attempt to show analytics on the dashboard
    dashboard_analytics()
    
    st.markdown("### Key Features:")
    
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
            st.rerun()
    
    with col2:
        st.markdown("""
        ### 📚 Course Management
        - Add new courses
        - Update course details
        - Delete courses
        """)
        if st.button("Go to Course Management"):
            st.session_state.navigation = "📚 Course Management"
            st.rerun()
    
    with col3:
        st.markdown("""
        ### 📝 Grade Management
        - Assign grades
        - Update existing grades
        - Delete grades
        """)
        if st.button("Go to Grade Management"):
            st.session_state.navigation = "📝 Grades Management"
            st.rerun()
    
    # Analytics preview
    st.markdown("---")
    st.subheader("📊 Full Analytics & Reporting")
    st.markdown("""
    For more detailed insights from your data, visit the Analytics section:
    - Detailed student GPA analyses
    - Complete performance distribution
    - In-depth course analytics
    - At-risk student identification and filtering
    """)
    if st.button("Go to Full Analytics"):
        st.session_state.navigation = "📊 Analytics & Reporting"
        st.rerun()
    
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
            st.rerun()

def dashboard_analytics():
    """Show a summary of key analytics on the dashboard"""
    try:
        # Get analytics data
        students_gpa_df, course_analytics = GradeService.get_analytics_data()
        
        if students_gpa_df.empty:
            st.info("No student data available for analytics yet. Set up the database and add data to see analytics here.")
            return
            
        st.markdown("## 📊 Academic Overview")
        
        # Summary metrics in a clean row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            avg_gpa = students_gpa_df['gpa'].mean()
            st.metric("Average GPA", f"{avg_gpa:.2f}")
        with col2:
            passing_students = len(students_gpa_df[students_gpa_df['gpa'] >= 2.0])
            total_students = len(students_gpa_df)
            pass_rate = passing_students / total_students * 100 if total_students > 0 else 0
            st.metric("Pass Rate", f"{pass_rate:.1f}%")
        with col3:
            honor_students = len(students_gpa_df[students_gpa_df['gpa'] >= 3.5])
            honor_rate = honor_students / total_students * 100 if total_students > 0 else 0
            st.metric("Honor Students", f"{honor_rate:.1f}%")
        with col4:
            failing_students = len(students_gpa_df[students_gpa_df['gpa'] < 2.0])
            st.metric("Students at Risk", f"{failing_students}")
        
        # Show a single consolidated visualization instead of multiple
        st.markdown("### Academic Standing")
        
        # Create a figure with a single pie chart to save space
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Pie chart for academic standing
        academic_standing = pd.cut(
            students_gpa_df['gpa'],
            bins=[0, 2.0, 3.0, 3.5, 4.0],
            labels=['At Risk (< 2.0)', 'Average (2.0-3.0)', 'Good (3.0-3.5)', 'Excellent (3.5-4.0)']
        ).value_counts()
        
        ax.pie(
            academic_standing, 
            labels=academic_standing.index,
            autopct='%1.1f%%', 
            startangle=90,
            colors=sns.color_palette('viridis', len(academic_standing))
        )
        ax.set_title('Academic Standing Distribution')
        
        # Display the chart with minimized size
        st.pyplot(fig)
        
        # Top 5 students by GPA for quick reference
        st.markdown("### Top Performing Students")
        top_students = students_gpa_df.sort_values('gpa', ascending=False).head(5)
        st.dataframe(top_students[['student_id', 'name', 'gpa']], use_container_width=True)
        
    except Exception as e:
        st.info("Analytics will appear here after you set up the database and add data.")
        import traceback
        print(f"Dashboard analytics error: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 