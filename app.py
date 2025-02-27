from flask import Flask, jsonify, render_template
import requests
import os
import google.generativeai as genai
from config import GITHUB_TOKEN, GOOGLE_AI_KEY

app = Flask(__name__)

# Configure Gemini AI
genai.configure(GOOGLE_AI_KEY)

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

def fetch_github_data(username):
    """Fetch GitHub user details using GraphQL API."""
    query = """
    query($login: String!) {
      user(login: $login) {
        name
        login
        avatarUrl
        bio
        followers { totalCount }
        following { totalCount }
        repositories(first: 100, orderBy: {field: STARGAZERS, direction: DESC}) {
          totalCount
          nodes {
            name
            stargazers { totalCount }
            forks { totalCount }
            languages(first: 5) { nodes { name } }
          }
        }
      }
    }
    """

    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.post(GITHUB_GRAPHQL_URL, json={"query": query, "variables": {"login": username}}, headers=headers)

    if response.status_code == 200:
        return response.json().get("data", {}).get("user")
    return None

def summarize_data(data):
    """Generate a summary using Google Gemini AI."""
    prompt = f"Summarize this GitHub user's profile:\n{data}"
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text if hasattr(response, "text") else "No summary available."

def suggestion_data(summary):
    """Generate suggestions using Google Gemini AI."""

    prompt = f"Suggestions for the github user with this analysis/summary: {summary}"
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text if hasattr(response, "text") else "No suggestion(s) available."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/github/<username>")
def github_stats(username):
    data = fetch_github_data(username)
    if not data:
        return jsonify({"error": "User not found"}), 404

    summary = summarize_data(data)
    suggestions = suggestion_data(summary)

    return jsonify({"info": data, "summary": summary, "suggestions": suggestions})

if __name__ == "__main__":
    app.run(debug=True)
