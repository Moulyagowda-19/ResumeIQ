# ResumeIQ 🚀

ResumeIQ is a modern, AI-powered resume analyzer that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS).

## Features

- **📄 Multi-Format Support**: Upload PDF or DOCX resumes.
- **⚡ Instant Analysis**: Basic NLP extracts contact info, skills, experience, and projects.
- **🎯 Role-Based Scoring**: Select a target role (Frontend, Backend, DevOps, Data Science) for tailored feedback.
- **📊 Visual Dashboard**: 
    - Circular ATS Score Meter.
    - Radar Chart for score breakdown.
    - Skill Gap Analysis.
- **💡 Smart Suggestions**: Actionable feedback and "Power Verb" recommendations.

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, TailwindCSS (CDN), JavaScript
- **Parsing**: PyPDF2, python-docx
- **Charts**: Chart.js

## Installation

1. **Clone the repository** (or unzip the folder).
2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   ```bash
   python app.py
   ```
2. **Open your browser**:
   Navigate to `http://127.0.0.1:5000`
3. **Analyze**:
   - Select your target role.
   - Drag and drop your resume.
   - View your simplified ATS report!

## Project Structure

```
ResumeIQ/
├── app.py              # Flask application entry point
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css   # Custom animations
│   └── js/
│       └── script.js   # Frontend logic & Chart.js
├── templates/
│   ├── base.html       # Base layout
│   ├── index.html      # Landing & Upload page
│   └── result.html     # Analysis Dashboard
└── utils/
    ├── analyzer.py     # Skill gap & suggestion logic
    ├── extractor.py    # Text extraction (PDF/DOCX)
    └── scorer.py       # ATS scoring algorithm
```

## License

MIT License
