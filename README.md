# Student Progress Dashboard

A Streamlit application for tracking and visualizing student progress.

## Features

- Password-protected access
- Student progress tracking
- Interactive visualizations
- Data import/export capabilities
- Smart data processing

## Deployment Instructions

1. Fork this repository
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy the app

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Security Note

The app uses local file-based authentication. For production deployment, consider implementing a more robust authentication system.

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