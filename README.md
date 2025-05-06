# Student Progress Dashboard

A Streamlit application for visualizing and tracking student progress across different subjects.

## Features

- View student progress metrics
- Filter by student, subject, and date
- Track skills practiced and mastered
- Visualize progress over time
- View diagnostic growth (where available)

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Place your data file:
- Put your `combined_data.csv` file in the `data` directory
- The CSV should contain columns for student information and subject-specific metrics

## Running the App

Run the following command from the `streamlit_app` directory:
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501` by default.

## Data Format

The app expects a CSV file with the following columns:
- Student ID
- Student first name
- Student last name
- Teacher names
- End date
- Subject-specific columns for:
  - Questions answered
  - Skills practiced
  - Skills proficient
  - Skills mastered
  - Starting diagnostic level
  - Ending diagnostic level
  - Diagnostic growth

## Contributing

Feel free to submit issues and enhancement requests! 