from utils import *
from inverted_index import *
from cosine import * 

import heapq 
import pandas as pd
import os

def search(index: InvertedIndex, path_jobs:str):
    """Function that simulates a search engine

    Args:
        index (InvertedIndex): index object created by buildIndex() or loaded using openIndex()
        path_jobs (str): path to the tsv file containing the jobs announcements
    """
    while(True):
        print("Hi! Type a query to search a job on kijiji, q to exit:")
        query = input()
        if query=='q':
            print('Goodbye!')
            break
        query = preprocess(query)
        rank = Ranking(index) 
        res = rank.get_ranking(query)
        if not res:
            print("No results for your query")
        else:
            #Return the 5 best announcements using an heap
            best = heapq.nlargest(5, res) 
            print("Results ({}/{}):".format(len(best), len(res)))
            for i,r in enumerate(best):
                docId = r[1]  
                #get the right row to retrieve the link (fourth column)
                ann = pd.read_csv(path_jobs, sep = "\t", nrows = 1, skiprows = docId-1)
                print("{})docId: {}, link: {}".format(i+1,docId, ann.columns[4]))


def main():
    try:
        path = os.getcwd() +"/docs/"
        path_jobs = path + "jobs.tsv"
    except Exception as e: #insert manually the path
        print("Write the path to the folder containing the files:")
        path = input()
        path_jobs = path + "/jobs.tsv"

    print("Building the inverted index...")
    index = InvertedIndex()
    index.buildIndex(path)
    #index.printIndex(3)

    #To search I open again the inverted index
    print("Opening and loading the inverted index...")
    index = InvertedIndex()
    index.openIndex(path)
    #Now we can use the search engine!
    search(index, path_jobs)

if __name__ == "__main__":
    main()