##!/usr/bin/env python
# -*- coding: utf-8 -*-

import webbrowser
from newsapi import NewsApiClient
from datetime import datetime, timedelta

def google_search(query):
    """
        Use google to search something and open the result page.
    """
    webbrowser.open('http://www.google.com/search?hl=fr&q='+str(query))

def youtube_search(query):
    """
        Search for a query on youtube and open the result page.
    """
    webbrowser.open('https://www.youtube.com/results?search_query='+str(query))

def news_search():
    """
        Research top technology-related news in France.
            For more informations : https://newsapi.org/
    """
    now=datetime.strftime(datetime.now(), '%Y-%m-%d')
    yesterday=datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

    newsapi = NewsApiClient(api_key='d323e8ea3ff044d3b8833c67d93092eb')
    top_headlines = newsapi.get_top_headlines(category='technology',
                                              country='fr',
                                              language='fr',
                                              page=1)

    response="Voici les nouvelles du jour.\n"
    for article in top_headlines['articles']:
        response+=str(article['title']+" "+article['description'])+"\n"

    return response

if __name__ == '__main__':
    query=news_search()
    print(query)
