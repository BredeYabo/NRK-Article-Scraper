import asyncio
import io
import json
from contextlib import closing

from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException

import nrk_nav


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


nyheter = {}


def get_nrk_text():
    global nyheter
    raw_html = simple_get("https://www.nrk.no/norge/")
    html = BeautifulSoup(raw_html, 'html.parser')
    nyhet = ""
    not_visited = []
    visited = []
    loop = asyncio.get_event_loop()
    for li in html.findAll('a'):
        li_ref = li.get('href')
        if li_ref not in nrk_nav.nrk_nav:
            if "https://" in li_ref:
                nyhet = simple_get(li_ref)
                if nyhet is not None:
                    nyhet = BeautifulSoup(nyhet, 'html.parser')

                    text = []
                    for p in nyhet.select('p'):
                        if p.get(
                                'class') is None and p.text not in "Den som mener seg rammet av urettmessig publisering, oppfordres til å ta kontakt med redaksjonen. Pressens Faglige Utvalg (PFU) er et klageorgan oppnevnt av Norsk Presseforbund som behandler klager mot mediene i presseetiske spørsmål.":
                            # print(p.text)
                            text.append(p.text)
                    text = ' '.join(text)

                    author = []
                    for a in nyhet.select('a'):
                        a_class = a.get('class')
                        if a_class is not None and a_class[0] == 'author__name':
                            # print(a.text)
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


# get_nrk_text()
with io.open('nyheter.json', 'w', encoding='utf8') as outfile:
    json.dump(nyheter, outfile, sort_keys=True, indent=4, ensure_ascii=False)
