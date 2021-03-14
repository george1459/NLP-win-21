import json
import tqdm

file_path = '/home/shicheng2000/NLP-win-21/idea_relations/data/RMRB_all.jsonlist'
jsList = []
with open(file_path) as f:
    for jsonObj in tqdm.tqdm(f):
        studentDict = json.loads(jsonObj)
        jsList.append(studentDict)

import pandas as pd

a = pd.DataFrame(jsList)
a['date'] = a.date.apply(int)
a.to_csv('/home/shicheng2000/NLP-win-21/idea_relations/data/rmrb_full_df-V1.csv')