import requests


def get_repositories(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100"

    try:
        response = requests.get(url, timeout=10)

    except requests.exceptions.Timeout:
        print("The request timed out.")
        raise SystemExit

    except requests.exceptions.ConnectionError:
        print("Could not connect to GitHub.")
        raise SystemExit

    except requests.exceptions.RequestException as error:
        print("A request error occurred.")
        print("Error:", error)
        raise SystemExit

    if response.status_code == 200:
        repos = response.json()
        return repos

    else:
        print("GitHub user not found.")
        print("Status code:", response.status_code)
        return[]

def count_languages(repos):
    language_counts = {}

    for repo in repos:
        language = repo["language"]

        if language in language_counts:
            language_counts[language] += 1
        else:
            language_counts[language] = 1

    return language_counts

if __name__ == "__main__":
    username = input("Enter GitHub username: ")

    repos = get_repositories(username)

    print("Total repositories:", len(repos))
    print("--------------------")

    for repo in repos:
        print("Repository:", repo["name"])
        print("Language:", repo["language"])
        print("--------------------")

    language_counts = count_languages(repos)

    print("\nLanguage Summary")
    print("--------------------")

    for language, count in language_counts.items():
        print(language + ":", count)