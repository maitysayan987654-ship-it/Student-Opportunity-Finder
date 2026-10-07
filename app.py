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

        query = request.form.get(
            "query",
            ""
        ).strip()

        location = request.form.get(
            "location",
            ""
        ).strip()

        search_type = request.form.get(
            "search_type",
            "Internship"
        )

        # --------------------------------
        # Validate input
        # --------------------------------

        if not query or not location:

            error_message = (
                "Please enter both a skill or keyword "
                "and a location."
            )

            return render_template(
                "index.html",
                results=results,
                search_type=search_type,
                error_message=error_message
            )

        # --------------------------------
        # Build search query
        # --------------------------------

        if search_type == "Internship":
            final_query = query + " internship"
        else:
            final_query = query + " job"

        print("SEARCH QUERY:", final_query)
        print("LOCATION:", location)

        # --------------------------------
        # SerpApi parameters
        # --------------------------------

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

            # --------------------------------
            # Handle API error
            # --------------------------------

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

                # --------------------------------
                # Location aliases
                # --------------------------------

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

                requested_skill = query.lower()

                relevant_results = []

                # --------------------------------
                # Process jobs
                # --------------------------------

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

                    company = job.get(
                        "company_name",
                        ""
                    ).lower()

                    # --------------------------------
                    # Better Location Matching
                    # --------------------------------

                    location_text = (
                        job_location
                        + " "
                        + title
                        + " "
                        + description
                    ).lower()

                    location_match = any(
                        city in location_text
                        for city in search_locations
                    )

                    remote_match = (
                        "remote" in job_location
                        or "work from home" in description
                        or "remote" in description
                    )

                    if not location_match and not remote_match:
                        continue

                    # --------------------------------
                    # Extract known skills
                    # --------------------------------

                    job["skills"] = extract_skills(
                        description
                    )

                    # --------------------------------
                    # Internship filtering
                    # --------------------------------

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

                        if not is_internship:
                            continue

                        if is_senior:
                            continue

                    # --------------------------------
                    # Smart relevance scoring
                    # --------------------------------

                    relevance_score = 0

                    # Exact search phrase in title
                    if requested_skill in title:
                        relevance_score += 10

                    # Exact search phrase in description
                    if requested_skill in description:
                        relevance_score += 5

                    # Exact search phrase in company
                    if requested_skill in company:
                        relevance_score += 2

                    # Match against detected skills
                    if any(
                        requested_skill == skill.lower()
                        for skill in job["skills"]
                    ):
                        relevance_score += 8

                    # --------------------------------
                    # Multi-word search support
                    # --------------------------------

                    query_words = [
                        word
                        for word in requested_skill.split()
                        if len(word) > 2
                    ]

                    for word in query_words:

                        if word in title:
                            relevance_score += 2

                        elif word in description:
                            relevance_score += 1

                    # --------------------------------
                    # Internship relevance bonus
                    # --------------------------------

                    if search_type == "Internship":

                        if "intern" in title:
                            relevance_score += 3

                        elif "internship" in description:
                            relevance_score += 2

                    # --------------------------------
                    # Fresher / entry-level bonus
                    # --------------------------------

                    fresher_keywords = [
                        "fresher",
                        "freshers",
                        "entry level",
                        "entry-level",
                        "no experience",
                        "0-1 years",
                        "0 to 1 years"
                    ]

                    if any(
                        keyword in title
                        or keyword in description
                        for keyword in fresher_keywords
                    ):
                        relevance_score += 1

                    # --------------------------------
                    # Save relevance score
                    # --------------------------------

                    job["relevance_score"] = (
                        relevance_score
                    )

                    # --------------------------------
                    # Keep location-matching results
                    #
                    # Main search supports ANY
                    # skill or keyword.
                    # --------------------------------

                    relevant_results.append(job)

                # --------------------------------
                # Remove duplicate jobs
                # --------------------------------

                unique_results = []

                seen_jobs = set()

                for job in relevant_results:

                    job_key = (
                        job.get(
                            "title",
                            ""
                        ).lower().strip(),

                        job.get(
                            "company_name",
                            ""
                        ).lower().strip(),

                        job.get(
                            "location",
                            ""
                        ).lower().strip()
                    )

                    if job_key in seen_jobs:
                        continue

                    seen_jobs.add(job_key)

                    unique_results.append(job)

                # --------------------------------
                # Sort by relevance
                # --------------------------------

                unique_results.sort(
                    key=lambda job: job.get(
                        "relevance_score",
                        0
                    ),
                    reverse=True
                )

                results = unique_results

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