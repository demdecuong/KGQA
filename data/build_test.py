'''
Auto generated testcase :)
'''
import pandas as pd
import json
import random

class TestBuilder:
    def __init__(self):
        self.symptoms = json.load(open('symptom.json'))
        self.disease = json.load(open('disease.json'))
        self.database = json.load(open('database.json'))
    
    def build_test(self):
        ''' Build multiple test from give file '''
        test_cases = open("testcase.txt", "r")
        content = test_cases.read().split('\n')
        output = []
        for con in content:
            output.append(self.build_single_test(cont))

        ou
    def build_single_test(self,sentence):
        ''' Build only one test '''
        if '[entity]' in sentence:
            output = sentence.replace('[entity]',self.get_exist_entity('symptom'))
            output = sentence.replace('[entity]',self.get_exist_entity('disease'))
            output = sentence.replace('[entity]',self.get_exist_entity('acronym'))
            output = sentence.replace('[entity]',self.get_unknown_entity())
        if '[list of entity]' in sentence:


    def get_exist_entity(self,option='symptom'):
        ''' Get an exist entity '''
        
        if option == 'symptom':
            idx = self.get_a_random(len(self.symptoms))
            return [self.symptoms[idx]['name symptom']]

        if option == 'disease':
            idx = self.get_a_random(len(self.disease))
            return [self.disease[idx]['name disease']]

        if option == 'acronym':
            idx = self.get_a_random(len(self.disease))
            return [self.symptoms[idx]['name disease']]

    def get_unknown_entity(self,option='symptom'):
        return 'helloworld'
        
    def get_a_random(self, max_len):
        return random.randint(0,max_len)

    def remove_random_character(self,s):
        ''' From perfect sentence --> missing character sentence '''
        pass




if __name__ == '__main__':
    test_builder = TestBuilder()
    test_builder.build_test()