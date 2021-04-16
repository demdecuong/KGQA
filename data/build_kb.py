import pandas as pd
import json
from tqdm import tqdm




disease_symptom = pd.read_csv('disease_symptom.csv')
disease_symptom.fillna(0, inplace=True)
# print(disease_symptom.columns)
# exit()


def build_single_kb(symptom,opt='symptom'):
    # Symptom
    if opt=='symptom':
        pairs = pd.DataFrame(symptom, columns=['id', 'name symptom', 'other name','link','acronym'])
        pairs = pairs.astype(str).apply(lambda x: x.str.lower())
        print(pairs.head(3))
        pairs.to_json('symptom.json',orient='index')
    else:
        pairs = pd.DataFrame(symptom, columns=['id', 'name disease', 'other name'])
        pairs = pairs.astype(str).apply(lambda x: x.str.lower())
        print(pairs.head(3))
        pairs.to_json('disease.json',orient='index')

# symptom = pd.read_csv('symptom.csv')
# build_single_kb(symptom,opt='symptom')
# disease = pd.read_csv('disease.csv')
# build_single_kb(disease,opt='disease')
# exit()
def save_to_json(path,data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

def matching_kb(disease_symptoms,symptoms,disease):
    '''
    Matching 2 KB: symptoms and disease by disease_symptom.csv
    Input:
        symptoms: list of json
            "0": {
            "id": 1,
            "name symptom": "Emphysema",
            "other name": "AAT deficiency",
            "acronym": null
            }
        disease : list of json
            "0": {
                "id": 1,
                "name disease": "Alpha-1 antitrypsin deficiency",
                "other name": "AAT deficiency"
            },
    '''
    data = []
    # disease_symptoms = pd.DataFrame(disease_symptoms,columns['id disease', 'id symptom', 'rate'])
    for index, row in tqdm(disease_symptoms.iterrows()):
        sample1 = {
            'source' :  disease[str(row['id disease'] + 1)]['name disease'].lower(),
            'relation' : 'symptom_of',
            "target": symptoms[str(row['id symptom'] + 1)]['name symptom'].lower(),
            'rate' : row['rate'],
        }
        
        sample2 = {
            "source": symptoms[str(row['id symptom'] + 1)]['acronym'].lower(),
            'relation' : 'disease_of',
            'target' :  disease[str(row['id disease'] + 1)]['name disease'].lower(),
            'rate' : row['rate'],
        }
        sample3 = {
            "source": symptoms[str(row['id symptom'] + 1)]['other name'].lower(),
            'relation' : 'disease_of',
            'target' :  disease[str(row['id disease'] + 1)]['name disease'].lower(),
            'rate' : row['rate'],
        }
        
        sample4 = {
            "source": symptoms[str(row['id symptom'] + 1)]['name symptom'].lower(),
            'relation' : 'disease_of',
            'target' :  disease[str(row['id disease'] + 1)]['name disease'].lower(),
            'rate' : row['rate'],
        }

        sample5 = {
            'source' :  disease[str(row['id disease'] + 1)]['other name'].lower(),
            'relation' : 'symptom_of',
            "target": symptoms[str(row['id symptom'] + 1)]['name symptom'].lower(),
            'rate' : row['rate'],
        }
        data.append(sample1)
        data.append(sample2)
        data.append(sample3)
        data.append(sample4)
        data.append(sample5)

    for ii in tqdm(range(len(symptoms))):
        sy1 = {
            "source": symptoms[str(ii)]['name symptom'],
            'relation' : 'synonym_of',
            "target": symptoms[str(ii)]['other name'],
        }
        sy2 = {
            "source": symptoms[str(ii)]['name symptom'],
            'relation' : 'acronym_of',
            "target": symptoms[str(ii)]['acronym'],
        }
        sy3 = {
            "source": symptoms[str(ii)]['other name'],
            'relation' : 'synonym_of',
            "target": symptoms[str(ii)]['name symptom'],
        }
        sy4 = {
            "source": symptoms[str(ii)]['name symptom'],
            'relation' : 'is',
            "target": 'symtom-'+ str(symptoms[str(ii)]['other name']),
        }
        sy5 = {
            "source": symptoms[str(ii)]['name symptom'],
            'relation' : 'is',
            "target": 'symtom-'+str(symptoms[str(ii)]['acronym']),
        }
        sy6 = {
            "source": symptoms[str(ii)]['other name'],
            'relation' : 'is',
            "target": 'symtom-'+str(symptoms[str(ii)]['name symptom']),
        }
        sy7 = {
            "source": symptoms[str(ii)]['acronym'],
            'relation' : 'is',
            "target": 'symtom-'+str(symptoms[str(ii)]['name symptom']),
        }
        sy8 = {
            "source": symptoms[str(ii)]['acronym'],
            'relation' : 'is',
            "target": 'symtom-'+str(symptoms[str(ii)]['other name']),
        }
        sy9 = {
            "source": symptoms[str(ii)]['other name'],
            'relation' : 'acronym_of',
            "target": symptoms[str(ii)]['acronym'],
        }
        data.append(sy1)
        data.append(sy2)
        data.append(sy3)
        data.append(sy4)
        data.append(sy5)
        data.append(sy6)
        data.append(sy7)
        data.append(sy8)
        data.append(sy9)
        
    for ii in tqdm(range(len(disease))):
        di1 = {
            'source' : disease[str(ii)]['other name'],
            'relation' : 'synonym_of',
            'target' :  disease[str(ii)]['name disease'],
        }
        di2 = {
            'source' :  disease[str(ii)]['name disease'],
            'relation' : 'synonym_of',
            'target' : disease[str(ii)]['other name'],
        }
        di3 = {
            'source' : disease[str(ii)]['other name'],
            'relation' : 'is',
            'target' :  'disease-'+str(disease[str(ii)]['name disease']),
        }
        di4 = {
            'source' :  disease[str(ii)]['name disease'],
            'relation' : 'is',
            'target' : 'disease-'+str(disease[str(ii)]['other name']),
        }
        data.append(di1)
        data.append(di3)
        data.append(di2)
        data.append(di4)
    with open('database.json', 'w') as jsonfile:
        json.dump(data, jsonfile)

symptoms = json.load(open('symptom.json',))
disease = json.load(open('disease.json',))
matching_kb(disease_symptom,symptoms,disease)
# database = json.load(open('database.json'))
