from decouple import config
import requests

header = {'Accept': 'application/vnd.github.v3+json',
          'Authorization': f"token {config('GITHUB_API_TOKEN')}"}


def get_name(username):
    """
    returns name of the Github user
    """
    url = 'https://api.github.com/users/'+username
    response = requests.get(url, headers=header)
    response_dict = response.json()

    return response_dict["name"]


def get_contributors():
    """
    returns contributor details
    """
    url = 'https://api.github.com/repos/ashutoshkrris/EazyLoader/contributors?per_page=1000'
    response = requests.get(url, headers=header)
    response_dict = response.json()
    bots = ['dependabot[bot]', 'dependabot-preview[bot]', 'restyled-commits',
            'bug-debug-done', 'allcontributors[bot]', 'ImgBotApp']
    contributors = []
    for contributor in response_dict:
        username = contributor["login"]
        name = get_name(username)
        avatar = contributor["avatar_url"]
        profile = contributor["html_url"]
        if username not in bots:
            contributors.append({
                "username": username,
                "name": name,
                "avatar_url": avatar,
                "profile_url": profile
            })

    return contributors
