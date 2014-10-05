# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 02:39:23 2014

@author: kristyc
"""

import requests
import re
from requests.auth import HTTPDigestAuth
import json
from flask import Flask, jsonify, render_template
app = Flask(__name__)
from flask_bootstrap import Bootstrap
Bootstrap(app)

REUTERS_LIT_SEARCH = 'https://lsapi-demo.thomson-pharma.com/ls-api-ws/ws/rs/literature-v1/literature/search'
REUTERS_DRUGS_SEARCH = 'https://lsapi-demo.thomson-pharma.com/ls-api-ws/ws/rs/drugs-v1/drug/search'
REUTERS_TRIAL_SEARCH = 'https://lsapi-demo.thomson-pharma.com/ls-api-ws/ws/rs/trials-v1/search/'
REUTERS_CONF_SEARCH = 'https://lsapi-demo.thomson-pharma.com/ls-api-ws/ws/rs/conference-v1/conference/search'
REUTERS_PRESS_SEARCH= 'https://lsapi-demo.thomson-pharma.com/ls-api-ws/ws/rs/pressRelease-v1/pressRelease/search'

def getTweets(query):
    URL = 'http://otter.topsy.com/searchdate.json'

    params = {
        'apikey': '09C43A9B270A470B8EB8F2946A9369F3',
        'perpage': 100,
        'q': query,
        'window': 'a',
        'zoom': 10,
        'locale': 'en'}

    result = requests.get(URL, params=params)

    try:
        data = result.json()
    except:
        print result.content
        raise

    return data['response']['list']

def get_from_thomson_reuters(url, params):
    auth = HTTPDigestAuth('Hackathon_09','AUIZ2BWTFR5M679E')
    
    if not 'fmt' in params:
        params['fmt'] = 'json'
    
    resp = requests.get(url, params=params, auth=auth)
    return resp.json()
    
def get_literature_for(search_string):
    resp = None
    cache_file_name = 'cache/{}_lit.json'.format(search_string)
    try:
        with open(cache_file_name) as f:
            resp = json.load(f)
    except IOError:
        pass
    
    if not resp:
        resp = get_from_thomson_reuters(REUTERS_LIT_SEARCH, {
            'query': search_string
        })
        with open(cache_file_name, 'w') as f:
            json.dump(resp, f)
    return resp['literatureResultsOutput']['SearchResults']['Literature']

def get_drugs_for(search_string):
    resp = None
    cache_file_name = 'cache/{}_drugs.json'.format(search_string)
    try:
        with open(cache_file_name) as f:
            resp = json.load(f)
    except IOError:
        pass
    
    if not resp:
        resp = get_from_thomson_reuters(REUTERS_DRUGS_SEARCH, {
            'query': search_string
        })
        with open(cache_file_name, 'w') as f:
            json.dump(resp, f)
    return resp['drugResultsOutput']['SearchResults']['Drug']

def get_trials_for(search_string):
    resp = None
    cache_file_name = 'cache/{}_trials.json'.format(search_string)
    try:
        with open(cache_file_name) as f:
            resp = json.load(f)
            print 'Using cache'
    except IOError:
        pass
    
    if not resp:
        resp = get_from_thomson_reuters(REUTERS_TRIAL_SEARCH + search_string, {})
        with open(cache_file_name, 'w') as f:
            json.dump(resp, f)
    return resp['trialResultsOutput']['SearchResults']['Trial']


def get_conference_for(search_string):
    resp = None
    cache_file_name = 'cache/{}_conference.json'.format(search_string)
    try:
        with open(cache_file_name) as f:
            resp = json.load(f)
    except IOError:
        pass
    
    if not resp:
        resp = get_from_thomson_reuters(REUTERS_CONF_SEARCH, {
            'query': search_string
        })
        with open(cache_file_name, 'w') as f:
            json.dump(resp, f)
    return resp['conferenceResultsOutput']['SearchResults']['Conference']

def get_press_for(search_string):
    resp = None
    cache_file_name = 'cache/{}_press.json'.format(search_string)
    try:
        with open(cache_file_name) as f:
            resp = json.load(f)
    except IOError:
        pass
    
    if not resp:
        resp = get_from_thomson_reuters(REUTERS_PRESS_SEARCH, {
            'query': search_string
        })
        with open(cache_file_name, 'w') as f:
            json.dump(resp, f)
    return resp['pressReleaseResultsOutput']['SearchResults']['PressRelease']

@app.route('/reuter/<search_string>')
def process_data_web(search_string):
    data = get_trials_for(search_string)
    return jsonify({'results': data})
    
@app.route('/')
def derp():
    return render_template('index.html')

@app.route('/twitter/<search_string>')
def query_data(search_string):
    data = getTweets(search_string)
    return jsonify({'results': data})
            
def process_data_trial(search_string):
    with open('ebola_trials_2.json', 'r') as f:
        data = json.load(f)
        
        output_data = []
        with open('asdf.json', 'w') as asdf:
            json.dump(data['trialResultsOutput' ]['SearchResults']['Trial'], asdf)
        for datum in data['trialResultsOutput']['SearchResults']['Trial']:
            try:
                print datum['PatientCountEnrollment'], len(datum['IndicationsAdverse']['Indication']) \
                if 'Indication' in datum['IndicationsAdverse'] else 0
            except Exception as e:
                print e
            title = datum['TitleDisplay']
            dt = parser.parse(datum['DateChangeLast']).strftime('%Y-%m-%d')
            abstract = datum['Teaser']
            s = analyze_sentiment(abstract)
            output_data.append((title, dt, abstract, s['score'], s['sentiment']))
        
        with open('ebola_trials.csv', 'w') as wf:
            w = csv.writer(wf)
            for datum in output_data:
                w.writerow(datum)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
