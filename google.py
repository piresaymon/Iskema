#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Arquivo: iskema/google.py
# ATENÇÃO: Este arquivo requer atualizações significativas além das mostradas aqui
# para funcionar corretamente com Python 3 e as mudanças na web.
# Esta é uma versão parcialmente atualizada apenas para demonstrar as mudanças de sintaxe.

# Python bindings to the Google search engine
# Copyright (c) 2009-2012, Mario Vilas
# All rights reserved.
# (Licença mantida conforme o original)

__version__ = "$Id: google.py 930 2012-02-13 21:21:25Z qvasimodo $"

__all__ = ['search']

# Atualiza imports para Python 3
import bs4 as BeautifulSoup # Ou importe BeautifulSoup diretamente de bs4
import http.cookiejar as cookielib # Substitui cookielib
import os
import time
# Substitui urllib, urllib2, urlparse por módulos do Python 3
import urllib.request as urllib2
import urllib.parse as urlparse
import urllib.parse

# URL templates to make Google searches.
url_home          = "http://www.google.%(tld)s/"
url_search        = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&btnG=Google+Search"
url_next_page     = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&start=%(start)d"
url_search_num    = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&btnG=Google+Search"
url_next_page_num = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&start=%(start)d"

# Cookie jar. Stored at the user's home folder.
home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERPROFILE') # Correção para Windows
    if not home_folder:
        home_folder = '.'   # Use the current folder on error.
cookie_jar = cookielib.LWPCookieJar(
                            os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass

# Request the given URL and return the response page, using the cookie jar.
def get_page(url):
    """
    Request the given URL and return the response page, using the cookie jar.
    (Docstring mantida conforme o original)
    """
    # Substitui urllib2.Request e opener
    request = urllib2.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
    cookie_jar.add_cookie_header(request)
    try:
        response = urllib2.urlopen(request)
        cookie_jar.extract_cookies(response, request)
        html = response.read()
        response.close()
        cookie_jar.save()
        return html
    except Exception as e: # Adiciona tratamento de erro básico
        print(f"Erro ao obter página {url}: {e}")
        return ""

# Filter links found in the Google result pages HTML code.
# Returns None if the link doesn't yield a valid result.
def filter_result(link):
    try:
        # Valid results are absolute URLs not pointing to a Google domain
        # like images.google.com or googleusercontent.com
        o = urlparse.urlparse(link, 'http')
        if o.netloc and 'google' not in o.netloc.lower(): # .lower() para comparação case-insensitive
            return link

        # Decode hidden URLs.
        if link.startswith('/url?'):
            # Substitui urlparse.parse_qs
            parsed_query = urlparse.parse_qs(o.query)
            q_values = parsed_query.get('q')
            if q_values:
                link = q_values[0] # Pega o primeiro valor de 'q'

            # Valid results are absolute URLs not pointing to a Google domain
            o = urlparse.urlparse(link, 'http')
            if o.netloc and 'google' not in o.netloc.lower():
                return link

    # Otherwise, or on error, return None.
    except Exception:
        pass
    return None

# Returns a generator that yields URLs.
def search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0):
    """
    Search the given query string using Google.
    (Docstring mantida conforme o original)
    """
    hashes = set()

    # Substitui urllib.quote_plus por urllib.parse.quote_plus
    query = urllib.parse.quote_plus(query)

    get_page(url_home % vars())

    if num == 10:
        url = url_search % vars()
    else:
        url = url_search_num % vars()

    while not stop or start < stop:

        time.sleep(pause)

        html = get_page(url)

        # Substitui BeautifulSoup.BeautifulSoup por bs4.BeautifulSoup
        # e adiciona o parser
        soup = BeautifulSoup.BeautifulSoup(html, 'html.parser')
        anchors = soup.find_all('a') # Substitui findAll por find_all
        for a in anchors:

            try:
                link = a['href']
            except KeyError:
                continue

            link = filter_result(link)
            if not link:
                continue

            h = hash(link)
            if h in hashes:
                continue
            hashes.add(h)

            yield link

        start += num
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()

# When run as a script, take all arguments as a search query and run it.
if __name__ == "__main__":
    import sys
    query = ' '.join(sys.argv[1:])
    if query:
        for url in search(query, stop=20):
            print(url)
