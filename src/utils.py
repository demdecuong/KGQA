import spacy
import re
import textacy
from src.subject_verb_object_extract import findSVOs, nlp

def refine_question(question):
    '''
    Document ---> possible questions
    Features:
        1. Identify objective question + remove noise sentences
        2. Generate questions based on:
            2.1 Multiple Entity in a sentence
            2.2 relation(goal questions, given sentences)
            2.3 Entity linking for unexist entity (TBU)
        3. Transform sentence --> what is question.
    Input:
        question : given string

    Output:
        questions : list
            list of quality questions/sentences
    '''
    final_question = []
    question = question.split('.')
    intent = get_intent(question)
    if question[-1] == '':
        question = question[:-1]
    for ques in question:
        # padding for punct
        ques = re.sub('([.,!?()])', r' \1 ', ques)
        ques = re.sub('\s{2,}', ' ', ques)
        ques = ques.replace(',','and')
        
        # if a sentence is not a question
        # make it becomes a question
        # auto find/give a relation
        if is_question(ques) == False:
            trans_ques = transform_ques(ques,intent) 
            final_question.extend(trans_ques)

        else:
            final_question.append(ques.strip().lower())

    # If 
    # print(final_question)
    # exit()

    return final_question

    # # Generate more questions if have multiple entity
    # for ques in objective_question:
    #     final_question.extend(get_possible_ques(ques))
def transform_ques(ques,rela):
    tokens = nlp(ques)
    svos = findSVOs(tokens)
    final_ques = []
    for item in svos:
        item = list(item)
        item[0] = 'what is the'
        item[1] = rela
        text = ' '.join(item) 
        final_ques.append(text)
    return final_ques

def get_intent(doc):
    for sent in doc:
        if is_question(sent.lower()):
            if 'disease' in sent or 'diseases' in sent:
                return 'disease of'
            if 'acronym' in sent or 'acronyms' in sent:
                return 'acronym of'
            if 'synonym' in sent or 'synonyms' in sent:
                return 'synonym of'
            if 'symptom' in sent or 'symptoms' in sent:
                return 'symptom of'
    return 'is'
def is_question(question):
    w_ = ['what','how'] 
    for w in w_:
        if w in question:
            return True
    return False


def get_possible_ques(ques):
    '''
    1. Get relation
    2. Get all entities in object
    3. Intent classification for unknown type question : symptoms or disease or show info
    '''
    pass

# if __name__ == '__main__':
    # tokens = nlp("What are the disease of a1at deficiency and babinski sign.")
    # What is the disease
    # svos = findSVOs(tokens)
    # print(svos)

    # get_relation_idx('I feel not good and I have a Lymphedema,Accelerated atherosclerosis and TCC')
    # get_relation_idx('What is the disease of Lymphedema, Accelerated atherosclerosis and TCC')

    # attr PRON what
    # ROOT VERB is
    # det DET the
    # nsubj NOUN disease
    # prep ADP of
    # pobj NOUN lymphedema
    # punct PUNCT ,
    # conj VERB accelerated
    # dobj NOUN atherosclerosis
    # cc CCONJ and
    # conj NOUN tcc


    # What is the disease of Lymphedema --> [(e1,p,e2)]
    # What is the disease of Accelerated --> [(e3,p,e4)]
    # What is the disease of TCC --> [(e1,p,e2)]
    # I feel not good and I have a Lymphedema,Accelerated atherosclerosis and TCC'
    # What is the disease of Lymphedema --> [(e1,p,e2)]
    # What is the disease of Accelerated --> [(e3,p,e4)]
    # What is the disease of TCC --> [(e1,p,e2)]