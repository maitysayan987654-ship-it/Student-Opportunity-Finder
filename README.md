# Student Opportunity Finder

A web application that helps students discover internships and jobs using live Google Jobs search data through the SerpApi API.

## 🚀 Features

- Search internships and jobs using any skill or keyword
- Search by location
- Choose between Internship and Job opportunities
- Get live job search results
- Automatic detection of common technical skills
- Smart relevance-based result ranking
- Filter loaded results by detected skills
- View company, location, source, schedule and posting information
- View a short job description
- Directly open the original opportunity
- Responsive and student-friendly interface

## 🔎 How It Works

1. The user enters a skill or keyword.
2. The user enters a preferred location.
3. The user selects Internship or Job.
4. The application sends the search request to SerpApi's Google Jobs API.
5. SerpApi returns live structured job results.
6. The backend processes and ranks the results.
7. The frontend displays the opportunities in an easy-to-use format.

## 🧩 SerpApi Integration

SerpApi is the core search-data source of this project.

The application uses the Google Jobs API with:

- `engine=google_jobs`
- `q` for the user's search keyword
- `location` for geographic search
- SerpApi API key for authentication

The application processes returned `jobs_results` and displays relevant opportunity information such as:

- Job title
- Company
- Location
- Source
- Description
- Skills
- Posting information
- Apply link

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### API
- SerpApi Google Jobs API

### Environment
- Python Virtual Environment
- python-dotenv

## 📁 Project Structure

```text
Student-Opportunity-Finder/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── venv/