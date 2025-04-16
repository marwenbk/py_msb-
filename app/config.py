import os
import streamlit as st
from dotenv import load_dotenv

def load_config():
    """Load environment variables and return configuration dictionary"""
    load_dotenv()
    
    config = {
        "db": {
            "name": os.getenv("DB_NAME", "postgres"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", ""),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432")
        },
        "app": {
            "title": "Student Grades Tracker",
            "theme": {
                "primary_color": "#4CAF50",
                "secondary_color": "#333333",
                "background_color": "#f9f9f9",
                "font": "'Segoe UI', sans-serif"
            }
        }
    }
    
    return config

def apply_styling():
    """Apply consistent styling to the Streamlit application"""
    config = load_config()
    theme = config["app"]["theme"]
    
    st.markdown(f"""
    <style>
        .main {{background-color: {theme["background_color"]}; font-family: {theme["font"]};}}
        .stButton>button {{background-color: {theme["primary_color"]}; color: white; font-weight: bold;}}
        .stSidebar {{background-color: #e6e6e6;}}
        h1 {{color: {theme["secondary_color"]};}}
        h2 {{color: #444444;}}
        .stAlert {{border-radius: 8px;}}
        .stProgress > div > div > div > div {{background-color: {theme["primary_color"]} !important;}}
        div[data-testid="stForm"] {{background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);}}
    </style>
    """, unsafe_allow_html=True) 