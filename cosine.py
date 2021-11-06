from math import log,sqrt
from inverted_index import *

class ranking:
    def __init__(self, index:InvertedIndex):
        self.index = index
        self.N = int(self.index.docs_number)
        self.list_cosines = []
    
    #tf-idf = log(1+tf)*log(N/df)
    def tfidf(self, tf: int, N: int, df: int) -> float:
        return (1+log(tf,10))*log(N/df,10)

    def compute_doc_norm(self, docId:int, df:int) ->float:
        doc_tf_path = self.index.path_doc_tfs
        tfs_dict = dict()
        with open(doc_tf_path, 'r') as f:
            read_tsv = csv.reader(f, delimiter="\t")
            next(read_tsv) #just the head
            for i,row in enumerate(read_tsv):
                try:
                    if i==docId-2:
                        tfs_dict = ast.literal_eval(row[1])
                        break
                except Exception as e:
                    print(e)
                    break  
        f.close()
        norm = 0
        for value in tfs_dict.values():
            norm += self.tfidf(value, self.N, df)**2
        return sqrt(norm)

    def cosine(self, query: dict, doc: dict, norm:float) -> float:
        dot_product = 0
        q_norm = 0
        for token in doc.keys():
            dot_product += query[token] * doc[token]
        for token in query.keys():
            q_norm += query[token] ** 2
        q_norm = sqrt(q_norm)
        cosine = dot_product / (q_norm*norm) 
        return cosine
    

    def get_ranking(self, query: list)->list:
        q_vector = dict()
        docs_vectors = dict()
        docs_norm_dict = dict()
        for token in query:
            #query tf-idf vector
            q_tf = query.count(token)
            #consider case in which token is not in list
            try:
                idx = int(self.index.list_of_postings.index(token))
                df = int(self.index.list_of_postings[idx].df)
                q_vector[token] = self.tfidf(q_tf,self.N,df)
            except Exception as e:
                #print(e)
                #if a term is not present in any document, it will not be considered 
                continue 
            posting = self.index.list_of_postings[idx].posting #->posting for the token
            for d in posting.keys():
                docId = int(d)
                doc_norm = self.compute_doc_norm(docId,df)
                docs_norm_dict[docId] = doc_norm
                d_tf = posting[docId]
                if docId in docs_vectors:
                    docs_vectors[docId][token]= self.tfidf(d_tf,self.N,df)
                else:
                    docs_vectors[docId] = {}
                    docs_vectors[docId][token] = self.tfidf(d_tf,self.N,df)
        
        for key,value in docs_vectors.items():
            norm = docs_norm_dict[key]
            cos_sim = self.cosine(q_vector, value, norm)
            self.list_cosines.append((cos_sim,key))

        return self.list_cosines

