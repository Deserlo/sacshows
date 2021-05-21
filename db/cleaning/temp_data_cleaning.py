#%%
import json
import pandas as pd
import pdb
import re
import datetime
# -*- coding: utf-8 -*-


def excel2json():
    excel_data_df = pd.DataFrame(pd.read_excel('db\cleaning\Influential Women Database (1).xlsx', sheet_name='Sheet1').iloc[0:])
    excel_data = excel_data_df.rename(columns=lambda x : x.strip())
    #excel_data.rows= excel_data.iloc[2:]
    
    old_names = ["Affliations", 'Life span, date of birth to death' , 'DOB (full month, day (number), full year)']
    new_names = ["Affiliations", 'Life span', 'Date of Birth']
    excel_data.rename(columns=dict(zip(old_names, new_names)), inplace=True)
    excel_data = excel_data.iloc[:, 1:17]
    
    excel_data.dropna(axis=0, thresh=4, inplace=True)
    #excel_data.dropna(axis=1, thresh=8, inplace=True)

    json_str = excel_data.to_json(orient="records")
    json_dict = json.loads(json_str)

    new_dict_list = []
    for i in json_dict: 
        for a, b in i.items(): 
            if b is not None:
                clean_vals(i, a, b)
        new_dict_list.append(remove_any_none_keys(i))   
        print("-------------------------------------------------------------------------")
  
    '''
    for d in new_dict_list:
        print(d)
    '''

    with open('ibw_data.json', 'w', encoding='utf=8') as fp:
        json.dump(new_dict_list, fp, indent=4)



def remove_any_none_keys(bw_dict):
    return {k: v for k, v in bw_dict.items() if v is not None}


def title(b):
    b = b.split(",")
    return b


def prof_focus(b):
    #b = b.replace(",", "|").replace("and", "").split("|")
    b = b.split("|")
    return b

def country(b):
    if b.strip().endswith("U.S."):
        b =  b.strip().replace("U.S.", "U.S.A")
    elif b.strip().endswith("US"):
        b = b.strip().replace("US", "U.S.A")
    elif b.strip().endswith("USA"):
        b = b.strip().replace("USA", "U.S.A")
    elif not b.strip().endswith("U.S.A"):
        b = b.strip() + ",U.S.A"
    return b

def keyword(b): 
    b = b.split(",")
    return [b.strip().replace('"', "").replace("'", "") for b in b]

    

def lifespan(b):
    if "--" in b or "–" in b:
        b = b.replace("(", "").replace(")", "").replace("–", "--").split("--")
    else:
        b = b.replace("(", "").replace(")", "").split("to")
    return b

def dob_from_unix(b):
    '''
    unix_ts = b
    try:
        # when timestamp is in seconds
        b = datetime.datetime.fromtimestamp(unix_ts).date()
    except (ValueError):
        # when timestamp is in miliseconds
        b = datetime.datetime.fromtimestamp(unix_ts/ 1000).date()
    '''
    return b


def check_place(b):
    return b
    '''
    if b.strip() == "San Francisco":
        b = "San Francisco, CA"
    try:
        if b.split(",")[1].strip() in states_list:
            b = country(b)
            return b
    except:
        print("error with place format")
        return b
    '''

def citations(b):
    b = b.split("\n")
    #b = remove_from_lists(b)
    return [b.strip().replace('"', "").replace("'", "") for b in b if b]


def dob_from_str(b):
    print(b)
    try:
        #format_str = '%m/%d/%Y' # The format
        #format_str = '%B %d, %Y'
        print(b)
        #b = datetime.datetime.strptime(str(b.replace(",", " ")), format_str).date()
    except:
        print(b)
        #format_str = '%B %d %Y'
        #b = datetime.datetime.strptime(str(b.replace(",", " ")), format_str).date()
    return b

def works(b):
    b = b.split("\n")
    #b = remove_from_lists(b)
    return [b.strip().replace('"', "").replace("'", "") for b in b if b]

def quotes(b):
    b = b.split("\n")
    b = [b.strip().replace('"', "") for b in b if b]
    return b

def bio(b):
    b = b.replace("'", "").strip()
    return b

def relationships(b):
    return b
    '''
    b = b.split(",")
    return [b.strip().replace('"', "") for b in b if b]
    '''


def affiliations(b):
    b = b.split(",")
    '''
    if isinstance(b, str):
        b = b.split("\n")
    '''
    return [b.strip().replace('"', "") for b in b if b]


def notables(b):
    b = b.split("\n")
    '''
    b = remove_from_lists(b)
    '''
    return [b.strip() for b in b if b]


def remove_from_lists(b):
    b = [b.replace("(1)", "").replace("(2)", "").replace("(3)", "") for b in b if b]
    return b


def contributions(b):
    b = b.split("\n")
    '''
    if isinstance(b, list): 
        b = remove_from_lists(b)
    '''
    return b



def clean_vals(i, a, b):
    if a == "Title":
        b = title(b)
        i.update( { a: [b.strip().capitalize() for b in b]  } )
    if a == "Professional Focus":
        b = prof_focus(b)
        i.update( { a: [b.strip().capitalize() for b in b] } ) 
    if a == "Date of Birth":
        if isinstance(b, str):
            b = dob_from_str(b)
        elif isinstance(b, int) == True:    
            b = dob_from_str(str(b))
        i.update({a: str(b)})
    if a == "Place of Birth":
        print(b)
        b = check_place(b)
        i.update({a: b})
    elif a == "Life span":
        b = lifespan(b)
        i.update({ a: [b.strip() for b in b] })
    elif a == "Key Word Tag":
        b = keyword(b)
        i.update({ a: [b.strip().capitalize() for b in b] } )
    elif a == "Books/Published Works":
        b = works(b)
        i.update({a: b})
    if a == "Quote(s)":
        b = quotes(b)
        i.update({a: b})
    elif a == "Short Biography":
        b = bio(b)
        i.update({a: b})
    elif a == "Citations":
        b = citations(b)
        i.update({a: b})
    elif a == "Relationships to other figures in Black History":
        b = relationships(b)
        i.update({a: b})
    elif a == "Affiliations":
        b = affiliations(b)
        i.update({a: b})
    elif a == "Notable Events":
        b = notables(b)
        i.update({a: b})
    elif a == "Major contributions to American Society":
        b = contributions(b)
        i.update({a: b})



    
if __name__ == '__main__':
    excel2json()