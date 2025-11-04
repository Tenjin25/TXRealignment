import pandas as pd
import glob

files = glob.glob('openelections-data-tx/2014/counties/20141104__tx__general__*_precinct.csv')
print('County,DEM,REP')
for f in files:
    try:
        df = pd.read_csv(f)
        senate = df[df['office'].str.contains('Senate|SEN', case=False, na=False)]
        if not senate.empty:
            dem = senate[senate['party']=='DEM']['votes'].sum()
            rep = senate[senate['party']=='REP']['votes'].sum()
            print(f.split('__')[-2].upper()+','+str(dem)+','+str(rep))
    except Exception as e:
        print(f"Error in {f}: {e}")
