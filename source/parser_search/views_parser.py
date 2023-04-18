from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from requests import get
from json import dump, dumps

# Список URL-адресов для поиска
urls = {
    "github": "https://github.com/",
    "career.habr": "https://career.habr.com/",
    "tiktok": "https://www.tiktok.com/@",
    "pikabu": "https://pikabu.ru/@",
    "reddit": "https://reddit.com/user/",
    "instagram": "https://instagram.com/",
}

@csrf_exempt
def search(request):
    if request.method == "GET":
        username = request.GET.get("username")
        search_results = {}
        for url in urls.values():
            try:
                response = get(url + username, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")
                user_info = soup.find("a", class_="_31VWB3vSkv19o3I7RVE710")
                user_info1 = soup.find("title")
            except:
                continue

            if username in str(user_info) or username in str(user_info1):
                if username not in search_results:
                    search_results[username] = []
                search_results[username].append(f"{url}{username}")

        with open("search_results.json", "w") as f:
            dump(search_results, f, indent=4)

        return JsonResponse(search_results, json_dumps_params={"indent": 2})

    return JsonResponse({"error": "Неверный метод запроса."})
