import json
import re

import inflect
import pandas as pd
import spacy

from src.complex import ComplexFunc
from src.getentitypair import GetEntity


class QuestionAnswer:
    """docstring for QuestionAnswer."""

    def __init__(self,use_el):
        super(QuestionAnswer, self).__init__()
        self.complex = ComplexFunc(use_el)
        self.nlp = spacy.load('en_core_web_sm')
        self.p = inflect.engine()
        self.database = json.load(open('./data/database.json'))

    def refine_pairs(self,pair):
        if "synonym of" in pair[0] or "synonyms of" in pair[0] or "synonym of" in pair[1] or "synonyms of" in pair[1]:
            pair[0] = pair[0].replace('synonyms','').replace('synonym','').replace('of','').strip()
            pair[1] = 'synonym_of'
        elif "acronym of" in pair[0] or 'acronym' in pair[0] or "acronym of" in pair[1] or 'acronym' in pair[1]:
            pair[0] = pair[0].replace('acronym','').replace('of','').strip()
            pair[1] = 'acronym_of'
        elif "disease of" in pair[0] or "diseases of" in pair[0] or "disease of" in pair[1] or "diseases of" in pair[1]:
            pair[0] = pair[0].replace('diseases','').replace('disease','').replace('of','').strip()
            pair[1] = 'disease_of'
            pair.extend(['rate'])
        elif "symptoms of" in pair[0] or 'symptom of' in pair[0] or "symptoms of" in pair[1] or 'symptom of' in pair[1]:
            pair[0] = pair[0].replace('symptoms','').replace('symptom','').replace('of','').strip()
            pair[1] = 'symptom_of'
            pair.extend(['rate'])
        return pair

    def findanswer(self, question):
        import string
        
        p = self.complex.question_pairs(question)
        
        # if p == [] or p is None:
        #     return "Not Applicable"
        if p is None:
            return None
        # pair = self.nlp(" ".join(p[0]))
        final_answer = []
        final_rate = []
        extracted_ques = []
        for pp in p:
            pair = self.refine_pairs(pp)
            print('ques : ',pair)
            extracted_ques.append(pair)

            relQ = []
            loaded = self.database
            relationQ = self.nlp(pair[1])

            for i in relationQ:
                relationQ = i.lemma_
                relQ.append(relationQ)

            objectQ = pair[2]
            # print(timeQ, placeQ)

            relationQ = " ".join(relQ)
            # print(relationQ)
        # if pair[0] in ('who'):
        #     for i in loaded:
        #         relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
        #         relationSSS = " ".join([relation.lemma_ for relation in self.nlp(loaded[str(i)]["relation"])])

        #         relationS = [i.lemma_ for i in relationS]
        #         relationS = relationS[0]

        #         if relationS == relationQ:
        #             objectS = loaded[str(i)]["target"]
        #             objectS = re.sub('-', ' ', objectS)
        #             objectQ = re.sub('-', ' ', objectQ)
        #             # print(objectQ, objectS)

        #             if self.p.singular_noun(objectS):
        #                 objectS = self.p.singular_noun(objectS)
        #             if self.p.singular_noun(objectQ):
        #                 objectQ = self.p.singular_noun(objectQ)

        #             if objectS == objectQ:
        #                 if str(pair[4]) != "":
        #                     timeS = [str(loaded[str(i)]["time"]).lower()]
        #                     # print(timeQ, timeS)
        #                     if timeQ in timeS:
        #                         answer_subj = loaded[str(i)]["source"]
        #                         subList.append(answer_subj)
        #                 else:
        #                     answer_subj = loaded[str(i)]["source"]
        #                     subList.append(answer_subj)
        #         elif str(relationSSS) == str(relationQ):
        #             objectS = loaded[str(i)]["target"]
        #             objectS = re.sub('-', ' ', objectS)

        #             if objectS == objectQ:
        #                 if str(pair[4]) != "":
        #                     timeS = [str(loaded[str(i)]["time"]).lower()]
        #                     if timeQ in timeS:
        #                         answer_subj = loaded[str(i)]["source"]
        #                         subList.append(answer_subj)
        #                 else:
        #                     answer_subj = loaded[str(i)]["source"]
        #                     subList.append(answer_subj)


        #     answer_subj = ",".join(subList)
        #     if answer_subj == "":
        #         return "None"
        #     return answer_subj

            if pair[2] in ['what','which']:
                subjectQ = pair[0]
                subList = []
                for i in range(len(loaded)):
                    if loaded[i]["source"] != None:
                        subjectS = loaded[i]["source"].lower()
                    else: 
                        continue
                    # print(subjectQ, subjectS,subjectT)
                    if subjectQ == subjectS:
                        relationS = [relation for relation in self.nlp(loaded[i]["relation"])]
                        relationS = [i.lemma_ for i in relationS]
                        if len(relationS) > 1:
                            relationS = " ".join(relationS)
                        else:
                            relationS = relationS[0]
                        if relationQ == relationS:
                            answer_subj = loaded[i]["target"]
                            if answer_subj is not None:
                                subList.append(answer_subj)
                                if len(pair)>=4:
                                    subList[-1] = subList[-1] + ' . Rate: ' + str(loaded[i][str(pair[3])]) + '%'
                    subjectT = loaded[i]["target"]
                    if subjectQ == subjectT:
                        relationS = [relation for relation in self.nlp(loaded[i]["relation"])]
                        relationS = [i.lemma_ for i in relationS]
                        if len(relationS) > 1:
                            relationS = " ".join(relationS)
                        else:
                            relationS = relationS[0]
                        # print(relationQ, relationS)
                        if relationQ == relationS:
                            answer_subj = loaded[i]["source"]
                            if answer_subj is not None:
                                subList.append(answer_subj)
                                if len(pair)>=4:
                                    subList[-1] = subList[-1] + ' . Rate: ' + str(loaded[i][str(pair[3])]) +'%'
                        if len(subList) >= 2:
                            break
                # answer_obj = ",".join(subList)

                if subList == []:
                    final_answer.extend([None])
                else:
                    final_answer.extend(subList)
        return final_answer , extracted_ques
        # elif pair[4] in ['when']:
        #     subjectQ = pair[0]
        #     # print(relationQ, subjectQ)
        #     # print(pair[2])
        #     for i in loaded:
        #         # if i.dep_ in ('obj'):
        #         # print(loaded[str(i)], "HERE we go")
        #         subjectS = loaded[str(i)]["source"]
        #         # print(type(subjectQ), type(subjectS), numberOfPairs)
        #         if subjectQ == subjectS:
        #             relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
        #             # print(relationS)
        #             relationS = [i.lemma_ for i in relationS]
        #             relBuffer = relationS
        #             # print(relationS[0], relationS[1])
        #             # print(relBuffer[1])

        #             if len(relBuffer) < 2:
        #                 relationS = relBuffer[0]
        #             else:
        #                 if str(relBuffer[1]).lower() == 'to':
        #                     relationS = " ".join(relationS)
        #                 else:
        #                     relationS = relationS[0]
        #                     extraIN = relBuffer[1].lower()

        #             # print(relationQ, relationS)
        #             if relationQ == relationS:
        #                 if str(pair[5]) != "":
        #                     placeS = [str(place).lower() for place in self.nlp(loaded[str(i)]["place"])]
        #                     # print(placeQ, placeS)
        #                     if placeQ in placeS:
        #                         if loaded[str(i)]["time"] != '':
        #                             answer_obj = loaded[str(i)]["time"]
        #                         # elif extraIN == "in" or extraIN == "on":
        #                             # answer_obj = loaded[str(i)]["target"]
        #                             return answer_obj
        #                         return None
        #                 else:
        #                     if loaded[str(i)]["time"] != '':
        #                         answer_obj = loaded[str(i)]["time"]
        #                         return answer_obj
        #                     return None

        # elif pair[5] in ['where']:
        #     subjectQ = pair[0]
        #     for i in loaded:
        #         subjectS = loaded[str(i)]["source"]
        #         if subjectQ == subjectS:
        #             relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
        #             relationS = [i.lemma_ for i in relationS]
        #             relationS = relationS[0]

        #             if relationQ == relationS:
        #                 if str(pair[4]) != "":
        #                     timeS = [str(time).lower() for time in self.nlp(loaded[str(i)]["time"])]
        #                     if timeQ in timeS:
        #                         answer_obj = loaded[str(i)]["place"]
        #                         if answer_obj in (" ",""):
        #                             if int(i)<int(len(loaded)-1):
        #                                 pass
        #                             return None
        #                         return answer_obj
        #                     return None
                        
        #                 answer_obj = loaded[str(i)]["place"]
        #                 if answer_obj in (" ",""):
        #                     if int(i)<int(len(loaded)-1):
        #                         pass
        #                     return None
        #                 return answer_obj

