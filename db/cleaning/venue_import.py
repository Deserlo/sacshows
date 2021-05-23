import json
import pandas as pd
import pdb
import re
import datetime



def excel2json():
    excel_data_df = pd.DataFrame(pd.read_excel('db\cleaning\Venue Listings (3).xlsx', sheet_name='Sheet6').iloc[0:])
    excel_data = excel_data_df.rename(columns=lambda x : x.strip().lower())
    
    excel_data = excel_data.iloc[:, 0:12]
    '''
    excel_data.dropna(axis=0, thresh=4, inplace=True)
    #excel_data.dropna(axis=1, thresh=8, inplace=True)
    '''

    json_str = excel_data.to_json(orient="records")
    json_dict = json.loads(json_str)
    
    new_dict_list = []
    for i in json_dict: 
        for a, b in i.items(): 
            if b is not None and not b.startswith('https://') and not b.startswith("data:image"):
                i.update( { a: b.strip().lower() } ) 
        new_dict_list.append(i)   
  
    '''
    for d in new_dict_list:
        print(d)
    '''
    
    with open('venues.json', 'w', encoding='utf=8') as fp:
        json.dump(new_dict_list, fp, indent=4)


excel2json()