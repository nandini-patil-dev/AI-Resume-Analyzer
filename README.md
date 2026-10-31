
# ✨ AI Resume Analyzer & Job Matcher

An AI-powered resume analysis application that compares
candidate resumes with job descriptions, identifies skill
gaps, calculates keyword-based skill match scores, and
generates personalized feedback using Google Gemini.

## 🚀 Features

- Upload resumes in PDF format.
- Extract resume text using PyPDF.
- Identify technical and professional skills.
- Compare resume skills with job requirements.
- Calculate a keyword-based skill match percentage.
- Identify matched and missing skills.
- Generate AI-powered resume feedback using Gemini.
- Interactive dashboard built with Streamlit.

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API
- LangChain
- PyPDF
- NLP
- Scikit-learn

## 📂 Project Structure

AI-Resume-Analyzer/
│
├── app.py
├── resume_parser.py
├── skill_matcher.py
├── ai_analyzer.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
└── utils/
    └── skills.py

## ⚙️ Installation and Setup

### 1. Clone the repository

git clone https://github.com/YOUR_USERNAME/AI-Resume-Analyzer.git

### 2. Navigate to the project

cd AI-Resume-Analyzer

### 3. Create a virtual environment

python -m venv venv

### 4. Activate the environment

Windows:

venv\Scripts\activate

### 5. Install dependencies

pip install -r requirements.txt

### 6. Configure Gemini API key

Create a `.env` file in the project directory.

Add:

GOOGLE_API_KEY=your_actual_api_key

Get your API key from:
https://aistudio.google.com/

### 7. Run the application

streamlit run app.py

## 🔍 How It Works

1. Upload a PDF resume.
2. Paste the job description.
3. Extract text from the resume.
4. Identify skills in the resume and job description.
5. Compare the detected skills.
6. Calculate the skill match percentage.
7. Generate personalized AI feedback.

## 📌 Future Enhancements

- Resume improvement recommendations.
- Downloadable PDF analysis reports.
- Advanced semantic skill matching.
- Multiple job description comparisons.
- AI resume chatbot.

## 👩‍💻 Author

Nandini Patil

B.Tech – Computer Science and Business Systems
