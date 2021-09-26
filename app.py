import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect


app = Flask(__name__)

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/wiki/")
def base_redirect():
    return redirect('/wiki/Naruto')


@app.route("/wiki/<page_name>")
def wiki_page(page_name):
    url = f'https://naruto.fandom.com/wiki/{page_name}'
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    main = soup.find('main')
    aside = main.find('aside').extract() if main.find('aside') else None
    infobox = main.find(class_='infobox').extract() if main.find(class_='infobox') else None

    main.find(class_='page-header__top').decompose()
    main.find(class_='page-header__actions').decompose()
    main.find(class_='page-footer').decompose()
    main.find(class_='page-header__title').decompose()

    for item in main.find_all(class_='reference'):
        item.decompose()

    for item in main.find_all(class_='wikia-slideshow-overlay'):
        item.decompose()

    for item in main.find_all(class_='caption'):
        item.decompose()

    for item in main.find_all('img'):
        del item['decoding']
        del item['data-image-key']
        del item['data-image-name']
        del item['data-caption']

        if (item.get('data-src')):
            item['src'] = item.get('data-src')

        if (item.get('src')):
            item['src'] = item.get('src').rpartition('/revision')[0]

    content = main.find_all(['p', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img'])

    htmlString = ''
    for item in content:
        if ('lazyload' in str(item.get('class'))):
            continue

        htmlString += str(item)

    return render_template('wiki_page.html', wiki_content=htmlString)


if __name__ == '__main__':
    app.run()
