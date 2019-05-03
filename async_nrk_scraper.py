#!/usr/local/bin/python3.5
import asyncio
import io
import json

from aiohttp import ClientSession
from bs4 import BeautifulSoup

import app
import nrk_nav


async def fetch(aurl, session):
    async with session.get(aurl) as response:
        return await response.text()


resp = []
nyheter = {}


async def run(aurl):
    global resp
    tasks = []
    nyhet = ""
    not_visited = []  # TODO
    visited = []  # TODO
    main_nrk = app.simple_get(aurl)
    html = BeautifulSoup(main_nrk, 'html.parser')
    print("Fetched nrk.no")

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        print("Fetching all links")
        for i, li in enumerate(html.findAll('a')):
            li_ref = li.get('href')
            if li_ref not in nrk_nav.nrk_nav:
                if "https://" in li_ref:
                    task = asyncio.ensure_future(fetch(li_ref.format(i), session))
                    tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        resp = responses


def fetch_article_text(nrk_responses):
    global nyheter
    print("Gathering content from articles")
    for html in nrk_responses:
        if html is not None:
            nyhet = BeautifulSoup(html, 'html.parser')

            text = []
            for p in nyhet.select('p'):
                if p.get(
                        'class') is None and p.text not in "Den som mener seg rammet av urettmessig publisering, " \
                                                           "oppfordres til å ta kontakt med redaksjonen. Pressens " \
                                                           "Faglige Utvalg (PFU) er et klageorgan oppnevnt av Norsk " \
                                                           "Presseforbund som behandler klager mot mediene i " \
                                                           "presseetiske spørsmål.":
                    text.append(p.text)
            text = ' '.join(text)

            author = []
            for a in nyhet.select('a'):
                a_class = a.get('class')
                if a_class is not None and a_class[0] == 'author__name':
                    author.append(a.text)

            time = nyhet.select('time')
            if len(time) > 0:
                time = time[0].get('datetime')

            if author:
                nyheter[nyhet.select('title')[0].text] = {
                    "text": text,
                    "author": author,
                    "datetime": time
                }


def print_responses(result):
    print(result)


def write_articles(topic):
    global nyheter
    with io.open(f'{topic}.json', 'w', encoding='utf8') as outfile:
        json.dump(nyheter, outfile, sort_keys=True, indent=4, ensure_ascii=False)
    nyheter = {}


print("Starting main")
url = "https://www.nrk.no/urix/"
# Urix
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run("https://www.nrk.no/urix/"))
loop.run_until_complete(future)
fetch_article_text(resp)
write_articles("urix")
# Norge
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run("https://www.nrk.no/norge/"))
loop.run_until_complete(future)
fetch_article_text(resp)
write_articles("Norge")
print("Fetched all urls")
