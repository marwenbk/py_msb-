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
            # Display a better-styled info message with guidance
            st.markdown("""
            <div style="padding: 20px; background-color: #f8f9fa; border-radius: 10px; border-left: 4px solid #4CAF50; margin-bottom: 20px;">
                <h3 style="color: #4CAF50; margin-top: 0;">📊 Analytics Dashboard</h3>
                <p>No student data available yet. Follow these steps to see analytics:</p>
                <ol>
                    <li>Go to <b>Database Setup</b> and create tables with sample data</li>
                    <li>Or add your own students, courses, and grades manually</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
            return
            
        # Create a visually appealing header with gradient background
        st.markdown("""
        <div style="padding: 15px; border-radius: 10px; 
            background: linear-gradient(90deg, #4CAF50 0%, #2E7D32 100%); 
            color: white; margin-bottom: 20px;">
            <h2 style="margin:0; text-align:center;">📊 Academic Performance Dashboard</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Summary metrics with improved styling and color indicators
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate values for metrics
        avg_gpa = students_gpa_df['gpa'].mean()
        total_students = len(students_gpa_df)
        passing_students = len(students_gpa_df[students_gpa_df['gpa'] >= 2.0])
        pass_rate = passing_students / total_students * 100 if total_students > 0 else 0
        honor_students = len(students_gpa_df[students_gpa_df['gpa'] >= 3.5])
        honor_rate = honor_students / total_students * 100 if total_students > 0 else 0
        failing_students = len(students_gpa_df[students_gpa_df['gpa'] < 2.0])
        failing_rate = failing_students / total_students * 100 if total_students > 0 else 0
        
        # Add deltas to show context
        with col1:
            st.metric("Average GPA", f"{avg_gpa:.2f}", 
                      delta="out of 4.0" if avg_gpa <= 4 else None,
                      delta_color="off")
        with col2:
            st.metric("Pass Rate", f"{pass_rate:.1f}%", 
                      delta=f"{passing_students} students" if passing_students > 0 else None,
                      delta_color="off")
        with col3:
            st.metric("Honor Students", f"{honor_rate:.1f}%", 
                      delta=f"{honor_students} students" if honor_students > 0 else None,
                      delta_color="off")
        with col4:
            st.metric("Students at Risk", f"{failing_students}", 
                      delta=f"{failing_rate:.1f}% of total" if failing_students > 0 else "None",
                      delta_color="inverse")
        
        # Add a horizontal divider
        st.markdown("<hr style='margin: 15px 0; opacity: 0.3;'>", unsafe_allow_html=True)
        
        # Create a two-column layout for visualization and top students
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Enhanced pie chart for academic standing
            st.markdown("### 📈 Academic Standing")
            
            # Create a figure with a single pie chart
            fig, ax = plt.subplots(figsize=(8, 4.5))
            
            # Better colors for academic standing
            colors = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71']
            
            # Pie chart for academic standing
            academic_standing = pd.cut(
                students_gpa_df['gpa'],
                bins=[0, 2.0, 3.0, 3.5, 4.0],
                labels=['At Risk (< 2.0)', 'Average (2.0-3.0)', 'Good (3.0-3.5)', 'Excellent (3.5-4.0)']
            ).value_counts()
            
            # Create better styled pie chart
            wedges, texts, autotexts = ax.pie(
                academic_standing, 
                labels=None,  # We'll create a custom legend
                autopct='%1.1f%%', 
                startangle=90,
                colors=colors,
                wedgeprops={'width': 0.6, 'edgecolor': 'w', 'linewidth': 1},
                textprops={'fontsize': 11, 'color': 'white', 'fontweight': 'bold'}
            )
            
            # Draw a white circle at the center to create a donut chart
            centre_circle = plt.Circle((0, 0), 0.3, fc='white')
            ax.add_patch(centre_circle)
            
            # Add a custom legend
            legend_labels = academic_standing.index
            legend_handles = [plt.Rectangle((0, 0), 1, 1, color=colors[i]) for i in range(len(legend_labels))]
            ax.legend(legend_handles, legend_labels, loc="center", bbox_to_anchor=(0.5, 0), 
                      frameon=False, ncol=2, fontsize=10)
            
            # Add title with better styling
            ax.set_title('Student Performance Distribution', fontsize=14, fontweight='bold', pad=20)
            
            # Make the plot look clean
            ax.set_aspect('equal')
            
            # Display the chart
            st.pyplot(fig)
            
        with col2:
            # Top 5 students by GPA with better styling
            st.markdown("### 🏆 Top Performers")
            
            top_students = students_gpa_df.sort_values('gpa', ascending=False).head(5)
            
            # Format the data for better display
            display_df = top_students[['name', 'gpa']].reset_index(drop=True)
            display_df.index = display_df.index + 1  # Start index from 1
            
            # Add styling to the table
            st.dataframe(
                display_df, 
                column_config={
                    "name": "Student Name",
                    "gpa": st.column_config.NumberColumn(
                        "GPA",
                        format="%.2f",
                        help="Grade Point Average on a 4.0 scale"
                    )
                },
                use_container_width=True,
                hide_index=False
            )
            
            # Display total number of students with better styling
            st.markdown(f"""
            <div style="margin-top: 20px; text-align: center; padding: 10px; 
                background-color: #f8f9fa; border-radius: 5px;">
                <span style="font-weight: bold;">Total Students:</span> {total_students}
            </div>
            """, unsafe_allow_html=True)
        
        # Course performance snapshot
        if course_analytics:
            st.markdown("<hr style='margin: 15px 0; opacity: 0.3;'>", unsafe_allow_html=True)
            st.markdown("### 📚 Course Performance Snapshot")
            
            # Get average grades for each course
            course_grades = {}
            for course_name, data in course_analytics.items():
                course_grades[course_name] = data['average_grade']
            
            course_df = pd.DataFrame({
                'Course': list(course_grades.keys()),
                'Average Grade': list(course_grades.values())
            }).sort_values('Average Grade', ascending=False)
            
            # Create a horizontal bar chart for course performance
            fig, ax = plt.subplots(figsize=(10, 3 + 0.4 * len(course_grades)))
            bars = ax.barh(course_df['Course'], course_df['Average Grade'], color='#4CAF50')
            
            # Add data labels to the bars
            for i, bar in enumerate(bars):
                grade = course_df['Average Grade'].iloc[i]
                letter = "A" if grade >= 90 else "B" if grade >= 80 else "C" if grade >= 70 else "D" if grade >= 60 else "F"
                ax.text(
                    grade + 1, bar.get_y() + bar.get_height()/2,
                    f"{grade:.1f} ({letter})", 
                    va='center', fontsize=10, fontweight='bold'
                )
            
            # Customize the chart
            ax.set_xlim(0, 105)  # Give a little extra space for labels
            ax.set_xlabel('Average Grade', fontsize=12)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.tick_params(axis='both', which='major', labelsize=10)
            
            # Add grid lines for better readability
            ax.grid(axis='x', linestyle='--', alpha=0.7)
            
            # Display the chart
            st.pyplot(fig)
            
    except Exception as e:
        st.info("Analytics will appear here after you set up the database and add data.")
        import traceback
        print(f"Dashboard analytics error: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 