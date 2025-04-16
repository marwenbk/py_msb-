# Student Grades Tracker

A streamlined application for educational institutions to manage students, courses, and grades with insightful analytics.

## Features

- **Student Management**: Add, update, and delete student records
- **Course Management**: Manage course information including credits
- **Grade Management**: Assign and track student grades across courses
- **Analytics & Reporting**: View performance metrics, GPA calculations, and course statistics
- **Responsive UI**: User-friendly interface with search capabilities and data visualization

## Project Structure

```
py_msb/
├── app/
│   ├── models/         # Data models 
│   ├── database/       # Database connection and schema
│   ├── services/       # Business logic
│   ├── ui/             # UI components
│   ├── utils/          # Utility functions
│   ├── config.py       # Application configuration
│   └── main.py         # Main application logic
├── run.py              # Entry point
├── requirements.txt    # Dependencies
└── README.md           # This file
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd py_msb
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with database configuration:
```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

## Usage

1. Start the application:
```bash
streamlit run run.py
```

2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. First-time setup:
   - Go to **Database Setup** and create tables with sample data
   - Navigate through the different sections using the sidebar

## Database Schema

- **students**: Stores student information (ID, name, email)
- **courses**: Stores course details (ID, name, code, credits)
- **grades**: Maintains grade records linking students to courses

## Development

The application follows clean architecture principles:
- Separation of concerns with models, services, and UI layers
- DRY (Don't Repeat Yourself) principle applied throughout
- SOLID principles followed for maintainability
- Modular design for easy extension

## Requirements

- Python 3.7+
- PostgreSQL database
- Dependencies listed in requirements.txt

## License

This project is licensed under the MIT License - see the LICENSE file for details. # py_msb-
