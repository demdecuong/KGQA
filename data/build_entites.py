import pandas as pd
import json
from tqdm import tqdm

# symptom = pd.read_csv('symptom.csv')
# disease = pd.read_csv('disease.csv')
# disease_symptom = pd.read_csv('disease_symptom.csv')
# disease_symptom.fillna(0, inplace=True)


def build_single_kb(symptom,opt='symptom'):
    # Symptom
    if opt=='symptom':
        pairs = pd.DataFrame(symptom, columns=['id', 'name symptom', 'other name', 'acronym'])
        print(pairs.head(3))
        pairs.to_json('symptom.json',orient='index')
    else:
        pairs = pd.DataFrame(symptom, columns=['id', 'name disease', 'other name'])
        print(pairs.head(3))
        pairs.to_json('disease.json',orient='index')

def save_to_json(path,data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

def build_entities(symptoms,disease):
    '''
    Input:
        symptoms: list of json
            "0": {
            "id": 1,
            "name symptom": "Emphysema",
            "other name": "AAT deficiency",
            "acronym": 'null'
            }
        disease : list of json
            "0": {
                "id": 1,
                "name disease": "Alpha-1 antitrypsin deficiency",
                "other name": "AAT deficiency"
            },
    '''
    data = []
    for ii in tqdm(range(len(symptoms))):
        if symptoms[str(ii)]['name symptom'] != None:
            data.append(symptoms[str(ii)]['name symptom'])
        if symptoms[str(ii)]['other name'] != None:
            data.append(symptoms[str(ii)]['other name'])
        if symptoms[str(ii)]['acronym'] != None:
            data.append(symptoms[str(ii)]['acronym'])
        
    for ii in tqdm(range(len(disease))):
        if disease[str(ii)]['other name'] != None:
            data.append(disease[str(ii)]['other name'])
        if disease[str(ii)]['name disease'] != None:
            data.append(disease[str(ii)]['name disease'])

    with open('entities.txt', 'w') as f:
        f. write(json. dumps(data))

symptoms = json.load(open('symptom.json',))
disease = json.load(open('disease.json',))
build_entities(symptoms,disease)
# database = json.load(open('database.json'))
