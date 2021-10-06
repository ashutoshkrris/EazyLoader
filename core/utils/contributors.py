from decouple import config
import requests

header = {'Accept': 'application/vnd.github.v3+json',
          'Authorization': config('GITHUB_API_TOKEN')}


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
    url = 'https://api.github.com/repos/ashutoshkrris/EazyLoader/stats/contributors'

    response = requests.get(url, headers=header)
    response_dict = response.json()

    contributors = []
    for contributor in response_dict:
        username = contributor["author"]["login"]
        name = get_name(username)
        avatar = contributor["author"]["avatar_url"]
        profile = contributor["author"]["html_url"]

        contributors.append({
            "username": username,
            "name": name,
            "avatar_url": avatar,
            "profile_url": profile
        })

    return contributors
