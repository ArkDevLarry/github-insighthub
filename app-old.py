from flask import Flask, jsonify, render_template
import requests
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini AI
genai.configure(api_key=os.environ.get("API_KEY"))

def get_github_stats(username):
    url = f"https://api.github.com/users/{username}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

def summarize_data(data):
    info = {
        "name": data.get("name"),
        "public_repos": data.get("public_repos"),
        "followers": data.get("followers"),
        "following": data.get("following"),
        "bio": data.get("bio"),
    }

    sum_prompt = f"Analyze this GitHub user's stats: {info}"
    sum_model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    sum_response = sum_model.generate_content(sum_prompt)
    summary = sum_response.text if hasattr(sum_response, "text") else "No summary available."

    sugg_prompt = f"Suggestions for the github user with this analysis: {summary}"
    sugg_model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    sugg_response = sugg_model.generate_content(sugg_prompt)
    
    suggestions = sugg_response.text if hasattr(sugg_response, "text") else "No suggestions available."
    return {"info": info, "summary": summary, "suggestions": suggestions}

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/github/<username>', methods=['GET'])
def github_stats(username):
    data = get_github_stats(username)
    return jsonify(summarize_data(data)) if data else jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
