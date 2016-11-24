# -*- coding: utf-8 -*-

from .manager import TweetCriteria
from .manager import TweetManager
# import .models
import logging


def setTweetCriteria(username=None,
                     since=None,
                     until=None,
                     querySearch=None,
                     maxTweets=None):
    """
    Sets and validate TweetCriteria
    """
    # validating criteria
    try:
        if (username is None) and (querySearch is None):
            raise Exception("At least a username of querySearch must be provided")
    except:
        raise
    tweetCriteria = TweetCriteria()
    if username:
        tweetCriteria.username = username
    if since:
        import datetime as dt
        if type(since) is not dt.date:
            since = since.strftime("%Y-%m-%d")
        tweetCriteria.since = since
    if until:
        import datetime as dt
        if type(until) is not dt.date:
            until = until.strftime("%Y-%m-%d")
        tweetCriteria.until = until
    if querySearch:
        if not isinstance(querySearch,str):
            newquery = querySearch[0]
            for element in querySearch[1:len(querySearch)]:
                newquery += ' OR ' + str(element)
            querySearch = newquery
        logging.debug('{}'.format(querySearch))
        tweetCriteria.querySearch = querySearch
    if maxTweets:
        tweetCriteria.maxTweets = int(maxTweets)
    else:
        tweetCriteria.maxTweets = 10

    # try:
    #     logging.info("TweetCriteria {}".format(tweetCriteria))
    # except:
    #     pass

    return tweetCriteria

def getoldtweetsGenerator(SearchCriteria):
    """
    scraping tool for the results
    using tweet search Page. It is an alternative to oficial tweeter API.
    but information return results from scraping a webpage so it depends
    on how the scraping is done.
    """
    for rawtweet in TweetManager.getTweets(SearchCriteria):
        result = dict()
        
        result[u'id'] = rawtweet[u'id']
        result[u'id_str'] = rawtweet[u'id']
        result[u'created_at'] = rawtweet[u'date']
        result[u'text'] = rawtweet[u'text']
        result[u'user'] = {u'screen_name': rawtweet[u'username']}
        result[u'favorite_count'] = rawtweet[u'favorites']
        result[u'retweet_count'] = rawtweet[u'retweets']
        if rawtweet[u'lang'] is None or rawtweet[u'lang'] == '':
            result[u'lang'] = 'und'
        else:
            result[u'lang'] = rawtweet[u'lang']
        # process place full_name
        if rawtweet[u'geoText']:
            result[u'place'] = {u'full_name': rawtweet[u'geoText']}

        result[u'entities'] = {"user_mentions": [],
                               "hashtags": []}
        # Process hashtags
        for hashtag in rawtweet[u'hashtags'].split(' '):
            if hashtag != "":
                result[u'entities'][u'hashtags'].append(
                    {u'text': hashtag.replace('#', '')})
        # Process mentions
        for mention in rawtweet[u'mentions'].split(' '):
            if mention != "":
                result[u'entities'][u'user_mentions'].append(
                    {u'text': mention.replace('@', '')})

        # remove entities if no data is set:
        if (len(result[u'entities'][u'hashtags']) == 0) and (len(result[u'entities'][u'user_mentions']) == 0):
            result.pop(u'entities')
            
        yield result
