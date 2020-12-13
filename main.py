from bs4 import BeautifulSoup
from colorama import init, Fore
import requests
import threading
import random

init(convert=True)

class YOPmail(object):
    def __init__(self):
        self.targettitles = ['TikTok'] #Add more to the list if you are looking for other accounts
        self.writter = open('results.txt', 'a', encoding='utf-8', errors='replace')
        self.proxies = []
        self.lock = threading.Lock()
    
    def get_proxies(self):
        r = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all')
        for proxy in r.text.splitlines():
            threading.Thread(target=self._check, args=(proxy, )).start()
        return 

    def _check(self, proxy):
        try:
            proxies = {
                'http': f'socks4://{proxy}',
                'https': f'socks4://{proxy}'
            }
            r = requests.get('http://www.yopmail.com/en/', proxies=proxies, timeout=3)
            self.proxies.append(proxy)
        except:
            pass

    def get_yp(self):
        while True:
            try:
                #Gets the YP param that is used in the get_mail def
                _proxy = random.choice(self.proxies)
                proxies = {
                    'http': f'socks4://{_proxy}',
                    'https': f'socks4://{_proxy}'
                }
                r = requests.get('http://www.yopmail.com/en/', proxies=proxies)
                soup = BeautifulSoup(r.text, features="lxml")
                return soup.find("input", attrs={'id': 'yp'})['value']
            except:
                pass
    
    def info(self, message, end='\n', color=Fore.GREEN, tag='INFO'):
        self.lock.acquire()
        print(f'{color}[{Fore.WHITE}{tag}{color}] {Fore.WHITE} > {color}{message}', end=end)
        self.lock.release()

    def get_yj(self):
        while True:
            try:
                #Gets the YJ param that is used in the get_mail def
                _proxy = random.choice(self.proxies)
                proxies = {
                    'http': f'socks4://{_proxy}',
                    'https': f'socks4://{_proxy}'
                }
                r = requests.get('http://www.yopmail.com/style/3.1/webmail.js', proxies=proxies)
                return r.text.split('&yj=')[1].split('&')[0]
            except :
                pass

    def get_mail(self, login):
        headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://www.yopmail.com/en/',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        params = (
            ('login', login),
            ('p', 'r'),
            ('spam', 'true'),
            ('yf', '115'),
            ('yp', self.get_yp()),
            ('yj', self.get_yj()),
            ('v', '3.1'),
        )
        while True:
            try:
                _proxy = random.choice(self.proxies)
                proxies = {
                    'http': f'socks4://{_proxy}',
                    'https': f'socks4://{_proxy}'
                }
                response = requests.get('http://www.yopmail.com/en/inbox.php', headers=headers, params=params, proxies=proxies)
                if 'class="lms' in response.text:
                    break
            except:
                pass
        soup = BeautifulSoup(response.text, features='lxml')
        for element in soup.findAll('a', attrs={'class': 'lm'}):
            link = 'http://www.yopmail.com/en/' + element['href']
            title = element.find('span', attrs={'class': 'lmf'}).text
            desc = element.find('span', attrs={'class': 'lms'}).text
            for target in self.targettitles:
                if target in title:
                    self.info(f'Target "{target}" found: {link}')
                    self.info(f'Title: {title}')
                    self.info(f'Login: {login}@yopmail.com')
                    self.info(f'Preview: {desc}', end='\n' + Fore.WHITE + '='*120 + '\n')
    
    def run(self):
        self.get_proxies()
        for char in 'qwertyuiopasdfghjklzxcvbnm':
            for char1 in 'qwertyuiopasdfghjklzxcvbnm':
                threading.Thread(target=self.get_mail, args=(char+char1,)).start()


if __name__ == "__main__":
    yop = YOPmail()
    yop.run()