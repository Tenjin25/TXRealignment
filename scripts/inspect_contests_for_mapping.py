import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'data'/'texas_election_results.json'
j=json.loads(p.read_text(encoding='utf-8'))
for year in ('2018','2014'):
    print('YEAR',year)
    rby=j.get('results_by_year',{}).get(year,{})
    names=[]
    for cat,contests in rby.items():
        for key,c in contests.items():
            name=c.get('contest_name') or c.get('contest') or key
            names.append((key,name))
    for k,n in names:
        ln=n.lower()
        if any(x in ln for x in ['railroad','rail','supreme court','sup ct','court of criminal appeals','criminal appeals','representative','house district']):
            print(' ',k,":",n)
    print('\n')
print('done')
