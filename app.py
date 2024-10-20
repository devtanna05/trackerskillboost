from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

# Updated list of required courses for Google Gen AI Study Jam 2024
required_courses = [
    'The Basics of Google Cloud Compute',
    'Get Started with Cloud Storage',
    'Get Started with API Gateway',
    'Get Started with Looker',
    'Get Started with Dataplex',
    'Get Started with Google Workspace Tools',
    'Cloud Functions: 3 Ways',
    'App Engine: 3 Ways',
    'Cloud Speech API: 3 Ways',
    'Monitoring in Google Cloud',
    'Networking Fundamentals on Google Cloud',
    'Analyze Images with the Cloud Vision API',
    'Prompt Design in Vertex AI',
    'Develop GenAI Apps with Gemini and Streamlit',
    'Get Started with Pub/Sub',
    'Level 3: Google Cloud Adventures'
]

# Function to fetch the HTML content of the profile page
def fetch_profile_data(profile_url):
    response = requests.get(profile_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the profile page. Status Code: {response.status_code}")
    return response.text

# Function to scrape the completed courses and their completion dates
def get_completed_courses(profile_url):
    page_content = fetch_profile_data(profile_url)
    soup = BeautifulSoup(page_content, 'html.parser')

    completed_courses = []
    completion_dates = []

    # Adjust these selectors based on the actual structure of the Google Skill Boost profile page
    for course in soup.find_all('span', class_='ql-title-medium'):
        completed_courses.append(course.text.strip())
    
    for date in soup.find_all('span', class_='ql-body-medium'):
        completion_dates.append(date.text.strip())

    return completed_courses, completion_dates

# Route to display the form and handle submission
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        profile_url = request.form["profile_url"]
        try:
            # Scrape completed courses and dates
            completed_courses, completion_dates = get_completed_courses(profile_url)

            # Calculate progress
            completed_set = set(completed_courses)
            required_set = set(required_courses)
            completed = required_set.intersection(completed_set)
            missing = required_set - completed_set

            total_required = len(required_courses)
            completed_count = len(completed)
            progress_percentage = (completed_count / total_required) * 100

            # Prepare data for the template
            completed_data = zip(completed_courses, completion_dates)
            missing_courses = list(missing)
            return render_template("report.html", progress=progress_percentage, 
                                   completed_data=completed_data, missing_courses=missing_courses)
        except Exception as e:
            return render_template("index.html", error=str(e))
    return render_template("index.html")

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
