# KGQA

### Installation
```
    spacy==2.3.5
    pandas==1.1.5
```

### Run

python main.py -q [question] -t [test_type] (optional)

Example

    python main.py -q "Doctor told me I got short johnson neuroectodermal syndrome . What are the symptoms ?" -t 14

Output:_____________________________________________
    
    Question:  What is the disease . I got intellectual  disability and short stature .
    Answer
    aagenaes syndrome . Rate: 0%
    diamond-blackfan anemia . Rate: 1%-4%%
    spasmodic dysphonia . Rate: 1%-4%%
    adermatoglyphia . Rate: 1%-4%%

### Build KB
There are 2 main script are `build_entities.py` for entity linking and `build_kb.py` for our main KB.

    cd ./data
    python build_entities.py
    python build_kb.py

### Supported Features
- What is/are the synonym of [entity] 
- What is/are the synonym of [list of entity]
- What is/are the synonym of [unknown entity]  
- What is/are the disease of [list of symptoms] 
- What is/are the disease of [list contains unknown entity] 
- What is/are the disease of [other name/acronym of symptoms] 
- What is/are the acronym of [single entity] 
- What is/are the acronym of [list of entity] 
- What is/are [single entity] 
- What is/are [unknown single] 
- What is/are [list of entity] 
- I have [symptoms] . What diseases 
- I have [list of symptoms] . What diseases  
- I have [disease] . What symptoms  
- What disease  . [description]  
- What symptoms . [description] 

[TODO]
- What is/are the [unknown relation] [single entity]
- What is/are the [unknown relation] [unknown entity]
- What is/are the [unknown relation] [list of entity]
- What is/are the [unknown relation] [list contains unknown entity]

The code still not optimized and still contains hard-coded due to fast-building for PoC. 
Please feel free to raise the issue. :)