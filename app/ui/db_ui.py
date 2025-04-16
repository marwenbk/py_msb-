"""
Database setup UI component.
"""
import streamlit as st
from app.database.schema import create_tables, seed_data

def render_db_setup():
    """Render the database setup section of the UI"""
    st.header("Database Setup")
    
    # Warning box
    st.warning("""
    ⚠️ **CAUTION: Database Operations** ⚠️
    
    This page allows you to reset the database schema and seed sample data.
    These operations will **DELETE ALL EXISTING DATA**.
    
    Use this page only during development or initial setup.
    """)
    
    # Create tables section
    st.subheader("Database Schema")
    
    with st.expander("View Database Schema"):
        st.code("""
        -- Students Table
        CREATE TABLE students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
        
        -- Courses Table
        CREATE TABLE courses (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            code TEXT NOT NULL UNIQUE,
            credits INTEGER NOT NULL
        );
        
        -- Grades Table
        CREATE TABLE grades (
            id SERIAL PRIMARY KEY,
            student_id TEXT NOT NULL,
            course_id INTEGER NOT NULL,
            grade REAL NOT NULL,
            UNIQUE(student_id, course_id),
            FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY(course_id) REFERENCES courses(id) ON DELETE CASCADE
        );
        """, language="sql")
    
    # Setup options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Create Tables Only", help="Creates database tables without sample data"):
            success, message = create_tables()
            if success:
                st.success(message)
            else:
                st.error(message)
    
    with col2:
        if st.button("Create Tables with Sample Data", help="Creates tables and populates with sample data"):
            # Confirmation check
            confirm = st.checkbox("I confirm that I want to reset the database and add sample data")
            
            if confirm:
                # First create tables
                success_tables, message_tables = create_tables()
                
                if success_tables:
                    # Then seed data
                    success_seed, message_seed = seed_data()
                    
                    if success_seed:
                        st.success(f"{message_tables}\n{message_seed}")
                    else:
                        st.error(f"Tables created but seeding failed: {message_seed}")
                else:
                    st.error(f"Failed to create tables: {message_tables}")
            else:
                st.warning("Please confirm the operation first")
    
    # Database information
    st.subheader("Database Information")
    
    st.info("""
    This application uses PostgreSQL for data storage. Make sure your database connection is properly configured in the environment variables:
    
    - DB_NAME: Database name
    - DB_USER: Database user
    - DB_PASSWORD: Database password
    - DB_HOST: Database host
    - DB_PORT: Database port
    
    These can be set in a .env file in the project root.
    """)
    
    # Database operations explanation
    st.markdown("""
    ### Database Operations
    
    - **Create Tables Only**: This will drop and recreate all tables without adding any data.
    - **Create Tables with Sample Data**: This will drop and recreate all tables, then populate them with sample data:
        - 22 students with random IDs
        - 5 courses (Mathematics, Physics, Chemistry, English Literature, History)
        - Random grades for each student in each course
    """)
    
    st.markdown("---")
    st.caption("Note: For production use, you should disable this page or restrict access to administrators only.") 