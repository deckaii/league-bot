from bs4 import BeautifulSoup
import urllib.request as urllib2
import requests
import lxml
import cchardet


def get_character_data(char_text):
    char_dict = {}
    for i in char_text:
        char_dict[i.find('div', attrs={'class': 'name'}).text.strip()] = {
            "cs": i.find('div', attrs={'class': 'cs'}).text.strip().split("CS")[1],
            "kda": i.find('div', attrs={'class': 'detail'}).text.strip(),
            "win_rate": i.find('div', attrs={'class': 'played'}).text.strip().split("%")[0],
            "games_played": i.find('div', attrs={'class': 'played'}).text.strip().split("%")[1]
        }
    return char_dict


def get_rank(soup):
    try:
        return soup.find('div', attrs={'class': 'tier'}).text.strip()
    except:
        return "Unranked"


def get_data(url):
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
    page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page, 'lxml')

    payload = {
        'name': soup.find('span', attrs={'class': 'summoner-name'}).text.strip(),
        'level': soup.find('span', attrs={'class': 'level'}).text.strip(),
        'rank': get_rank(soup),
        # 'win-lose': soup.find('div', attrs={'class': 'stats'}).text.strip(),
        'profimg': soup.select_one('.profile-icon img')['src'],
        'chars_played': get_character_data(soup.find_all('div', attrs={'class': 'champion-box'}))
    }

    return (payload)
