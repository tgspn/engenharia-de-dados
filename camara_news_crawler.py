from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import os
import s3_handler


def get_news_link(page_num: int) -> List[str]:

    content = requests.get(
        f'https://www.camara.leg.br/noticias/ultimas?pagina={page_num}')

    soup = BeautifulSoup(content.text, 'html.parser')
    h3_elements = soup.find_all(
        'h3', {'class': 'g-chamada__titulo'})

    links = [element.a.get('href') for element in h3_elements]
    return links


def get_news(link: str) -> None:
    print(link)
    content = requests.get(link)

    filename = link.split(
        '/')[-2] if link.endswith('/') else link.split('/')[-1]

    s3_handler.upload_file(content.text, 'teste', filename+'.html')


def recursively(i):
    links = get_news_link(i)
    print(i)
    if len(links) > 0:
        [get_news(link) for link in links]
        recursively(i+1)


recursively(1)
