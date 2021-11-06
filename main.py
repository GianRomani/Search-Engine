from utils import *
from inverted_index import *
from cosine import * 

import numpy as np
from math import sqrt, log
import linecache
import heapq 
import pandas as pd

def create_index(path:str):

    #path = '/content/drive/MyDrive/Data Mining/HW2/batch_aa.tsv'
    index = InvertedIndex()
    index.buildIndex(path)
    #print(index.docsTF)
    #index.printIndex(3)
    print("Index built and written on file with success!")

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
                ann = pd.read_csv(path_jobs, sep = "\t", nrows = 1, skiprows = docId)
                print("{}) {}".format(i+1,ann.columns[4]))


def main():
    path = '/home/gianfree/Desktop/Data Mining/HW2/search_engine/'
    path_jobs = '/home/gianfree/Desktop/Data Mining/HW2/search_engine/jobs.tsv'
    path_index = '/home/gianfree/Desktop/Data Mining/HW2/search_engine/index.tsv'
    create_index(path)

    #To search I need to open again the inverted index
    index = InvertedIndex()
    index.openIndex(path)
    #Now we can use the search engine!
    search(index, path_jobs)

if __name__ == "__main__":
    main()