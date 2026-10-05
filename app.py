from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def extract_skills(text):

    skills_list = [
        "Python",
        "Java",
        "JavaScript",
        "HTML",
        "CSS",
        "React",
        "Angular",
        "Django",
        "Flask",
        "SQL",
        "MySQL",
        "MongoDB",
        "Git",
        "GitHub",
        "Machine Learning",
        "Artificial Intelligence",
        "Data Science",
        "Power BI",
        "Excel",
        "C++",
        "C",
        "AWS",
        "Docker"
    ]

    found_skills = []

    text = text.lower()

    for skill in skills_list:

        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


@app.route("/", methods=["GET", "POST"])
def home():

    results = []
    search_type = "Internship"
    error_message = None

    if request.method == "POST":

        query = request.form.get("query", "").strip()
        location = request.form.get("location", "").strip()
        search_type = request.form.get(
            "search_type",
            "Internship"
        )

        if search_type == "Internship":
            final_query = query + " internship"
        else:
            final_query = query + " job"

        print("SEARCH QUERY:", final_query)
        print("LOCATION:", location)

        params = {
            "engine": "google_jobs",
            "q": final_query,
            "location": location,
            "api_key": SERPAPI_KEY
        }

        try:

            response = requests.get(
                "https://serpapi.com/search.json",
                params=params,
                timeout=20
            )

            response.raise_for_status()

            data = response.json()

            if "error" in data:

                error_message = (
                    "Unable to fetch opportunities right now. "
                    "Please try again later."
                )

                print(
                    "SerpApi Error:",
                    data.get("error")
                )

            else:

                all_results = data.get(
                    "jobs_results",
                    []
                )

                selected_location = location.lower()

                location_aliases = {
                    "bangalore": [
                        "bangalore",
                        "bengaluru"
                    ],
                    "bengaluru": [
                        "bangalore",
                        "bengaluru"
                    ],
                    "kolkata": [
                        "kolkata",
                        "calcutta"
                    ],
                    "calcutta": [
                        "kolkata",
                        "calcutta"
                    ],
                    "mumbai": [
                        "mumbai",
                        "bombay"
                    ],
                    "chennai": [
                        "chennai",
                        "madras"
                    ],
                    "delhi": [
                        "delhi",
                        "new delhi"
                    ]
                }

                search_locations = location_aliases.get(
                    selected_location,
                    [selected_location]
                )

                for job in all_results:

                    job_location = job.get(
                        "location",
                        ""
                    ).lower()

                    description = job.get(
                        "description",
                        ""
                    ).lower()

                    title = job.get(
                        "title",
                        ""
                    ).lower()

                    location_match = (
                        any(
                            city in job_location
                            for city in search_locations
                        )
                        or "remote" in job_location
                        or "anywhere" in job_location
                    )

                    if search_type == "Internship":

                        internship_keywords = [
                            "intern",
                            "internship",
                            "trainee"
                        ]

                        senior_keywords = [
                            "mid",
                            "senior",
                            "lead",
                            "principal",
                            "manager",
                            "2+ years",
                            "3+ years",
                            "4+ years",
                            "5+ years",
                            "6+ years",
                            "7+ years",
                            "8+ years",
                            "9+ years",
                            "10+ years"
                        ]

                        is_internship = any(
                            keyword in title
                            or keyword in description
                            for keyword in internship_keywords
                        )

                        is_senior = any(
                            keyword in title
                            or keyword in description
                            for keyword in senior_keywords
                        )

                        if not is_internship or is_senior:
                            continue

                    if location_match:

                        job["skills"] = extract_skills(
                            description
                        )

                        results.append(job)

        except requests.RequestException as error:

            error_message = (
                "Could not connect to the job search service. "
                "Please check your internet connection and try again."
            )

            print(
                "Request Error:",
                error
            )

        except Exception as error:

            error_message = (
                "Something went wrong while searching. "
                "Please try again."
            )

            print(
                "Unexpected Error:",
                error
            )

    return render_template(
        "index.html",
        results=results,
        search_type=search_type,
        error_message=error_message
    )


if __name__ == "__main__":
    app.run(debug=True)