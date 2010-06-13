# Encoding: utf8
# Copyright 2010 Amaç Herdağdelen

import urllib
from urllib import quote_plus as urlquote_plus

# Uses built-in json for Python2.6 and later on.
try:
    import json
except ImportError:
    import simplejson as json

class Boss():
    """Thin wrapper for BOSS API."""
    def __init__(self, appid):
        self.appid = appid
    
    def search(self, query):
        query = urlquote_plus(query)
        params = {'appid': self.appid}
        encoded_params = urllib.urlencode(params)
        url =  ('http://boss.yahooapis.com/ysearch/web/v1/%s?%s' %
                (query,encoded_params))
        response = urllib.urlopen(url)
        data = json.load(response)
        return data

class WebNameGender:
    """For a given name, carries out several pattern-based searches via YAHOO
    BOSS and collects hit numbers. For instance, if the query
    "husband of X" returns more results than the query "wife of X" this counts
    as an evidence that X is a female name."""
    def __init__(self, appid):
        self.boss = Boss(appid)
        # A pattern is a dictionary with two items. The item with "male_query"
        # searches for evidence of being male and the item with "female_query"
        # searches for evidence of being female.
        self.patterns = [{"male_query": "%s and his",
                          "female_query": "%s and her"},
                         {"male_query": "his * and %s",
                          "female_query": "her * and %s"},
                         {"male_query": "%s himself",
                          "female_query": "%s herself"},
                         {"male_query": "%s's (girlfriend OR wife)",
                          "female_query": "%s's boyfriend OR husband)"},
                         {"male_query": "(girlfriend OR wife) of %s",
                          "female_query": "(boyfriend OR husband) of %s"},
                        ]

    def get_gender_scores(self, name):
        # Gender scores, m + f = 1 and
        m = 0.0
        f = 0.0        
        confidence = 0.0
        for p in self.patterns:
            # Gets raw hit counts for male and female per pattern.
            p_m = self._get_pattern_count(p["male_query"] % name)
            p_f = self._get_pattern_count(p["female_query"] % name)
            # Processes the scores if there is at least one hit for either
            # of the queries.
            if p_m or p_f:
                confidence += 1
                # Adds 0.5 to each hit for smoothing.
                tot = p_m + p_f + 1.0
                # Updates global gender scores
                m += ((p_m + 0.5) / tot)
                f += ((p_f + 0.5) / tot)
        # Averages the total gender scores. If there was no hit for the name
        # returns (-1,-1)
        if confidence:
            m /= confidence
            f /= confidence
        else:
            m = -1
            f = -1
        return (m,f)

    def _get_pattern_count(self, pattern):
        result = self.boss.search('"%s"' % pattern)
        return int(result[u'ysearchresponse'][u'totalhits'])


    

    