import requests
import os

def count_languages(repos):
    language_counts = {}

    for repo in repos:
        language = repo["language"] or "Unknown"

        if language in language_counts:
            language_counts[language] += 1
        else:
            language_counts[language] = 1

    return language_counts



def get_github_repositories(username):
    page = 1
    all_repos = []
    github_token = os.getenv("GITHUB_TOKEN")

    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        headers = {}

        if github_token:
            headers["Authorization"] = f"Bearer {github_token}"

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 404:
            return {"error": "GitHub user not found"}, 404

        if response.status_code != 200:
            return {"error": "GitHub API request failed"}, 502

        repos = response.json()

        if not repos:
            break

        all_repos.extend(repos)

        page += 1

    return all_repos
