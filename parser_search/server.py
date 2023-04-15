from flask import Flask, request
from bs4 import BeautifulSoup
from requests import get
from json import dump, dumps

app = Flask(__name__)


urls = {
    "github": "https://github.com/",
    "career.habr": "https://career.habr.com/",
    "tiktok": "https://www.tiktok.com/@",
    "pikabu": "https://pikabu.ru/@",
    "reddit": "https://reddit.com/user/",
    "instagram": "https://instagram.com/",
}

@app.route('/search')
def all_search():
    username = request.args.get('username')
    search_results = {}
    for url in urls.values():
        try:
            response = get(url + username, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            user_info = soup.find('a', class_='_31VWB3vSkv19o3I7RVE710')
            user_info1 = soup.find('title')
        except:
            continue

        if username in str(user_info) or username in str(user_info1):
            if username not in search_results:
                search_results[username] = []
            search_results[username].append(f"{url}{username}")

    with open('search_results.json', 'w') as f:
        dump(search_results, f, indent=4)

    return dumps(search_results, indent=2)


if __name__ == '__main__':
    app.run()