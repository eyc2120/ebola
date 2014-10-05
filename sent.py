# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 01:17:44 2014

@author: kristyc
"""

import requests

def analyze_sentiment(text):
    URL = 'https://api.idolondemand.com/1/api/sync/analyzesentiment/v1'
    API_KEY = 'e7ecaa10-d9fd-46c7-8dfb-b6abff1b78ed'
    
    params = {
        'text': text,
        'apikey': API_KEY
    }
    
    result = requests.get(URL, params=params)
    data = result.json()
    
    return data['aggregate']
   
