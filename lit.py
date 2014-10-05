
def process_ebola_data_2():
    with open('ebola_lit.json', 'w') as f:
        json.dump(resp3.json(), f)
    with open('ebola_lit.json','r') as f:
        data2 = json.load(f)
        
    output_data2 = []
    with open('fdsa.json', 'w') as fdsa:
        json.dump(data2['literatureResultsOutput' ]['SearchResults']['Literature'], fdsa)
    
    for datum in data2['literatureResultsOutput']['SearchResults']['Literature']:
        title = datum['Title']
        dt = parser.parse(datum['IssueDate']).strftime('%Y-%m-%d')
        abstract = datum['Teaser']
        s = analyze_sentiment(abstract)
        output_data2.append((title, dt, abstract, s['score'], s['sentiment']))
        
        with open('ebola_lit.csv', 'w') as wf:
            w = csv.writer(wf)
            for datum in output_data2:
                w.writerow(datum)