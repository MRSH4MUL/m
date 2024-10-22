import requests
from bs4 import BeautifulSoup
import re
import webbrowser
import os
import sys
import subprocess
from colorama import init, Fore, Style

# Инициализация colorama для работы с цветами в Windows
init(autoreset=True)

# Функция для автоустановки библиотек
def install_libraries():
    try:
        import requests
        import bs4
        import colorama
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'requests', 'bs4', 'colorama'])

# Основная функция для поиска по номеру телефона
def search_phone_number(phone_number):
    url = "https://www.google.com/search?q={}".format(phone_number)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('a')
        excluded_domains = ['google.com', 'maps.google.com', 'shop.grahamfield.com']
        phone_links = []
        for link in search_results:
            href = link.get('href')
            if href and not any(domain in href for domain in excluded_domains):
                cleaned_url = re.findall(r'(https?://\S+)', href)
                if cleaned_url:
                    phone_links.extend(cleaned_url)
        return phone_links
    else:
        return "Невозможно получить результаты поиска. Пожалуйста, попробуйте еще раз позже."

# Сохранение ссылок в файл HTML
def save_links_to_html(links):
    css_styles = """
        <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #222; color: #ddd; }
        .container { max-width: 800px; margin: 0 auto; padding: 40px; background-color: #333; box-shadow: 0 0 20px rgba(0, 0, 0, 0.5); border-radius: 10px; }
        h1 { text-align: center; margin-bottom: 30px; font-size: 36px; color: #fff; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5); }
        .link-list { list-style-type: none; }
        .link-item { margin-bottom: 20px; padding: 20px; background-color: #444; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5); transition: transform 0.3s ease, box-shadow 0.3s ease; }
        .link-item:hover { transform: translateY(-5px); box-shadow: 0 5px 10px rgba(0, 0, 0, 0.7); }
        .link-item a { display: block; color: #00ff99; text-decoration: none; font-size: 18px; font-weight: bold; transition: color 0.3s ease; }
        .link-item a:hover { color: #00ccff; }
        </style>
    """

    html = """<!DOCTYPE html>
<html>
<head>
    <title>Search Results</title>
    {}
</head>
<body>
    <div class="container">
        <h1>Search Results</h1>
        <ul class="link-list">
            {}
        </ul>
    </div>
</body>
</html>
""".format(css_styles, ''.join(['<li class="link-item"><a href="{}">{}</a></li>'.format(link, link) for link in links]))

    with open("search_results.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"{Fore.GREEN}Результаты сохранены в search_results.html")

# Очистка консоли
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Печать баннера
def print_banner():
    banner = f"""
{Fore.GREEN}   _____ _________    ____  ________  ____________ 
  / ___// ____/   |  / __ \/ ____/ / / / ____/ __ \\
  \\__ \\/ __/ / /| | / /_/ / /   / /_/ / __/ / /_/ /
{Fore.CYAN} ___/ / /___/ ___ |/ _, _/ /___/ __  / /___/ _, _/ 
/____/_____/_/  |_/_/ |_|\____/_/ /_/_____/_/ |_| 
tg: underllife
                        
"""
    print(banner)

# Вывод ссылок в консоль
def print_links_to_console(links):
    print(f"{Fore.CYAN}\nFound {len(links)} links:")
    for link in links:
        print(f"{Fore.GREEN}{link}")

def main():
    install_libraries()
    
    while True:
        clear_console()
        print_banner()
        phone_number = input(f"{Fore.GREEN}Введите номер телефона: ")

        results = search_phone_number(phone_number)
        if isinstance(results, list):
            print_links_to_console(results)
            save_links_to_html(results)
        else:
            print(f"{Fore.RED}{results}")

        input(f"{Fore.YELLOW}\nНажмите enter для продолжения...")

if __name__ == "__main__":
    main()
