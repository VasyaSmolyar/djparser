import requests
from lxml import html,etree

url = 'https://habrahabr.ru'

headers = {
    'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'
}
prDict = {
    'https' : 'socks5://95.110.186.48:23084',
    'http' : 'socks5://95.110.186.48:23084'
}

def parser(url,query,headers,proxies):
    res = requests.get(url,headers=headers,proxies=proxies)
    if res.status_code != 200:
        raise ValueError("Статус запроса равен {}".format(res.status_code))
    tree = html.fromstring(res.text)
    data = tree.xpath(query)
    res = [d.text for d in data]
    return res

if __name__ == "__main__":
    print(parse(url,'//h2[@class="post__title"]/a'))
