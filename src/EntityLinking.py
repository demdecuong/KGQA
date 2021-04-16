# A Space efficient Dynamic Programming
# based Python3 program to find minimum
# number operations to convert str1 to str2
import json
import re
import editdistance

class EntityLinking:
    def __init__(self):
        '''
        Input:
            symptoms_list : list of exist symptoms
            disease_list : list of exist disease
        '''

        # self.symptoms_list = json.load(open(symptoms_path))
        # self.disease_list = json.load(open(disease_path))
        self.entites = self.read_entities()
        
    def read_entities(self):
        with open('./data/entities.txt', 'r') as f:
            a = json.loads(f.read())
        return a

    def get_entity_linking(self,subject,k=1):
        '''
        subject : list of subj
        '''
        res = []
        for subj in subject:
            res.append(subj)
            res.extend(self.get_el_one_sample(self.refine(subj),k))
        res = list(set(res))
        return res
    
    def get_el_one_sample(self,s,k=1):
        '''
        Input:
            s : given string
            k : top k 
        Output:
            res : [k1 , k2 ,k3]
            Return top k min distance 
        '''
        rank_score = [0]*len(self.entites) 
        for i,ent in enumerate(self.entites):
            score = editdistance.eval(s,ent)
            # not optimized
            rank_score[i] = score

        idx = sorted(range(len(rank_score)), key=lambda i: rank_score[i], reverse=False)[:k]
        res_list = [self.entites[i] for i in idx]
        return res_list
    def refine(self,s):
        s = s.replace('of','').replace('symptom','').replace('disease','').replace('synonym','').replace('acronym','').strip()
        return s
if __name__ == '__main__':
    el = EntityLinking()
    a = el.get_entity_linking(['Riht aortic arh'])
    print(a)