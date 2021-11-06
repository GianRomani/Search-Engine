from utils import *
from inverted_index import *
from cosine import * 

import heapq 
import pandas as pd
import os

def create_index(path:str):
    index = InvertedIndex()
    index.buildIndex(path)
    #index.printIndex(3)

def search(index: InvertedIndex, path_jobs:str):
    while(True):
        print("Hi! Write a query to search a job on kijiji, q to exit:")
        query = input()
        if query=='q':
            print('Goodbye!')
            break
        query = preprocess(query)
        rank = ranking(index) 
        res = rank.get_ranking(query)
        if not res:
            print("No results for your query")
        else:
            #Return the 5 best announcements
            best = heapq.nlargest(5, res) 
            #print(best)
            print("Results ({}/{}):".format(len(best), len(res)))
            for i,r in enumerate(best):
                docId = r[1]  
                ann = pd.read_csv(path_jobs, sep = "\t", nrows = 1, skiprows = docId-1)
                print("{})docId: {}, link: {}".format(i+1,docId, ann.columns[4]))


def main():
    try:
        path = os.getcwd() +"/docs/"
        path_jobs = path + "jobs.tsv"#"jobs.tsv"
    except Exception as e:
        print("Write the path to the folder containing the files:")
        path = input()
        path_jobs = path + "/jobs.tsv"

    create_index(path)
    #To search I need to open again the inverted index
    index = InvertedIndex()
    index.openIndex(path)
    #Now we can use the search engine!
    search(index, path_jobs)

if __name__ == "__main__":
    main()