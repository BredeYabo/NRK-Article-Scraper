from requests import get
import nrk_nav
import pprint
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

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

raw_html = simple_get("https://www.nrk.no/norge/")
html = BeautifulSoup(raw_html, 'html.parser')
nyhet = ""

nyheter = {}
for i, li in enumerate(html.findAll('a')):
    li_ref = li.get('href')
    # if li_ref not in nrk_nav.nrk_nav:
        # print(li.get('href'))
    if li_ref not in nrk_nav.nrk_nav:
        if "https://" in li_ref:
            nyhet = simple_get(li_ref)
            nyhet = BeautifulSoup(nyhet, 'html.parser')

            text = []
            for j, p in enumerate(nyhet.select('p')):

                if p.get('class') is None:
                    print(j, p.text)
                    text.append(p.text)
            text = ' '.join(text)

            author = []
            for j, a in enumerate(nyhet.select('a')):
                a_class = a.get('class')
                if a_class is not None and a_class[0]  == 'author__name':
                    print(a.text)
                    author.append(a.text)
            nyheter[nyhet.select('title')[0].text] = {
                "text": text,
                "author": author
            }

print(nyheter)
