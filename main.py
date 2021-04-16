import time
import pandas as pd
import getopt
import sys
import argparse

from src.getentitypair import GetEntity
from src.qna import QuestionAnswer
from src.utils import refine_question

class Main:
    """docstring for Main."""

    def __init__(self,args):
        super(Main, self).__init__()
        self.qna = QuestionAnswer(args.use_el)
        self.getEntity = GetEntity()

    def main(self, argv):
        inputQue = ''
        try:
            opts, args = getopt.getopt(
                argv, "hi:q:g:s:", ["ifile=", "question=", "showGraph=", "showEntities="])
            if opts == [] and args == []:
                print("ERROR")
                print("Help:")
                print("python init.py -q <Question> -e <use_el>")
        except getopt.GetoptError as err:
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print('test.py -q <question> -g <y or n> -s <Show Entities>')
                sys.exit()
            elif opt in ("-q", "--question"):
                inputQue = arg
            elif opt in ("-e", "--use_el"):
                showEntities = arg
            else:
                assert False, "unhandled option"

        return inputQue, showEntities
    def get_ranked_ans(self, li, top_k):
        
        li = list(filter(None, li))
        li = sorted(li, key = li.count,
                                reverse = True)
        try:
            li = list(dict.fromkeys(li))
        except:
            print('error')
            print(li)
        return li[:top_k]
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--use_el', type=int, default=True)
    parser.add_argument('-q', type=str, help='question')
    parser.add_argument('-t', type=str, help='test type')

    args = parser.parse_args()

    initialize = Main(args)
    # inputQue, showEntities = initialize.main(sys.argv[1:])
    inputQue = args.q
    extract_question = []
    if inputQue:    
        log = []
        # avoid nontype case
        question = refine_question(inputQue)
        for sent in question:
            start = time.time()
            # List of answer
            outputAnswer,extracted_ques = initialize.qna.findanswer(sent)
            ranked_ans = initialize.get_ranked_ans(outputAnswer,top_k=5)
            extract_question.extend(extracted_ques) 
            if ranked_ans != []:
                # list of list
                for ii in range(min(len(ranked_ans), 5)):
                    log.append(f"{ranked_ans[ii]}")
            else:
                log.append(f"{'Unknown'}")
            # else:
            #     log.append("Answer: Could not defifne")
        print("------------------------------------------------------------------------------------------------------------")
        print("Question: ", inputQue)
        print("Answer")
        if log != []:
            for ans in log:
                print(ans)
        else:
            print('None')
        print("Run time: ", time.time() - start)
        print("------------------------------------------------------------------------------------------------------------")

        # Save to excel
        f = open('log.csv','a')

        f.write(f'"{inputQue}","{extracted_ques}","{log}",{args.t}\n')

        # Mot cau hoi can cau tra loi tu nhieu cau khac nhau.
        # List of trieu chung --> Benh gi ?
        # Query : list of related docs | Deep:
        # Entity Linking (Embedding) : edit-distance, embedding space (BioBERT).
        # Process multiple symptoms, diseases. || Duoc

        # Semantic Parsing :

# list(chain.from_iterable(repeat(i, c)
#          for i, c in Counter(ini_list).most_common()))