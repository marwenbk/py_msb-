"""
Analytics and reporting UI component.
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from app.services.grade_service import GradeService

def render_analytics():
    """Render the analytics and reporting section of the UI"""
    st.header("Analytics & Reporting")
    
    # Get analytics data
    try:
        students_gpa_df, course_analytics = GradeService.get_analytics_data()
        
        if students_gpa_df.empty:
            st.warning("No student data available for analytics.")
            return
            
        # Overall Stats Overview
        st.subheader("Overall Academic Performance")
        
        # Summary metrics
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
            st.metric("Honor Rate (GPA ≥ 3.5)", f"{honor_rate:.1f}%")
        with col4:
            failing_students = len(students_gpa_df[students_gpa_df['gpa'] < 2.0])
            st.metric("Students at Risk", f"{failing_students}")
        
        # Students with GPA
        st.subheader("Students with GPA (4.0 Scale)")
        
        # Add search functionality
        search = st.text_input("Search students by name or ID:")
        if search:
            filtered_df = students_gpa_df[
                students_gpa_df['name'].str.contains(search, case=False) | 
                students_gpa_df['student_id'].str.contains(search, case=False)
            ]
            st.dataframe(filtered_df.sort_values('gpa', ascending=False), use_container_width=True)
        else:
            st.dataframe(students_gpa_df.sort_values('gpa', ascending=False), use_container_width=True)
        
        # GPA Distribution Visualization
        st.subheader("GPA Distribution")
        
        # Create a figure with multiple plots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram for GPA distribution
        sns.histplot(students_gpa_df['gpa'], bins=8, kde=True, ax=ax1)
        ax1.set_title('GPA Distribution')
        ax1.set_xlabel('GPA')
        ax1.set_ylabel('Number of Students')
        
        # Pie chart for academic standing
        academic_standing = pd.cut(
            students_gpa_df['gpa'],
            bins=[0, 2.0, 3.0, 3.5, 4.0],
            labels=['At Risk (< 2.0)', 'Average (2.0-3.0)', 'Good (3.0-3.5)', 'Excellent (3.5-4.0)']
        ).value_counts()
        
        ax2.pie(
            academic_standing, 
            labels=academic_standing.index,
            autopct='%1.1f%%', 
            startangle=90,
            colors=sns.color_palette('viridis', len(academic_standing))
        )
        ax2.set_title('Academic Standing')
        
        st.pyplot(fig)
        
        # Filters for performance analysis
        st.subheader("Performance Analysis")
        
        # Filter students by GPA threshold
        col1, col2 = st.columns([1, 3])
        with col1:
            threshold = st.number_input(
                "GPA Threshold:", 
                min_value=0.0, 
                max_value=4.0, 
                value=2.0, 
                step=0.1
            )
        with col2:
            threshold_type = st.radio(
                "Filter Type:",
                ["Below Threshold (At Risk)", "Above Threshold (Good Standing)"]
            )
        
        # Apply filter based on selection
        if threshold_type == "Below Threshold (At Risk)":
            filtered_students = students_gpa_df[students_gpa_df['gpa'] < threshold]
            filter_description = f"Students with GPA below {threshold} (At Risk)"
        else:
            filtered_students = students_gpa_df[students_gpa_df['gpa'] >= threshold]
            filter_description = f"Students with GPA {threshold} or above (Good Standing)"
        
        # Show filtered results
        st.subheader(filter_description)
        st.dataframe(filtered_students.sort_values('gpa', ascending=threshold_type == "Below Threshold (At Risk)"), use_container_width=True)
        
        # Course Analytics
        st.subheader("Course Performance Analysis")
        
        if course_analytics:
            # Create selectbox for courses
            course_names = list(course_analytics.keys())
            selected_course = st.selectbox(
                "Select Course to Analyze:",
                options=course_names
            )
            
            if selected_course in course_analytics:
                course_data = course_analytics[selected_course]
                
                # Display course analytics
                st.markdown(f"### {selected_course}")
                
                # Course stats
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Average Grade", f"{course_data['average_grade']}/100")
                    
                    # Calculate letter grade equivalent
                    avg_grade = course_data['average_grade']
                    letter = "A" if avg_grade >= 90 else "B" if avg_grade >= 80 else "C" if avg_grade >= 70 else "D" if avg_grade >= 60 else "F"
                    st.metric("Letter Grade Equivalent", letter)
                
                with col2:
                    # Top students in course
                    st.subheader("Top Students")
                    st.dataframe(course_data['top_students'])
        else:
            st.info("No course analytics data available")
    
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")
        st.info("Please make sure students, courses, and grades have been added to the system.") 