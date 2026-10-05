\# Student Opportunity Finder



Student Opportunity Finder is a web application that helps students find relevant internships and jobs using live job search data from SerpApi.



Users can search opportunities by skill, location, and opportunity type.



\## Features



\- Search for internships and jobs

\- Search by skill such as Python, Java, SQL, React, etc.

\- Search by location

\- Uses live Google Jobs data through SerpApi

\- Filters internship results to reduce irrelevant experienced roles

\- Extracts relevant technical skills from job descriptions

\- Filter displayed results by skill

\- Shows company, location, source, job type, posting information, and description

\- Provides a direct opportunity link



\## How SerpApi Is Used



SerpApi is the core search data provider of this project.



The application uses the SerpApi Google Jobs API to retrieve live job and internship opportunities.



The backend sends the user's search query and location to SerpApi and receives job results in JSON format.



These results are then processed and displayed in the web application.



\## Technology Stack



\- Python

\- Flask

\- HTML

\- CSS

\- JavaScript

\- SerpApi Google Jobs API

\- python-dotenv

\- Requests



\## Project Structure



```text

Student-Opportunity-Finder/

│

├── app.py

├── requirements.txt

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

