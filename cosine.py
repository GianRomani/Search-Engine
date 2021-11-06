from math import log,sqrt
from inverted_index import *

class ranking:
    def __init__(self, index:InvertedIndex):
        self.index = index
        self.N = int(self.index.docs_number)
        self.list_cosines = []
    
    #tf-idf = log(1+tf)*log(N/df)
    def tfidf(self, tf: int, N: int, df: int) -> float:
        #print("types of tf:{}\nN: {}\ndf:{}".format(type(tf),type(N),type(df)))
        return log(1+tf,10)*log(N/df,10)


    def cosine(self, query: dict, doc: dict, docId: int) -> float:
        dot_product = 0
        q_norm = 0
        doc_norm = 0
        query_len = len(query)
        try:
            doc_len = self.index.doc_len[docId]
        except Exception as e:
            print(e)
        #doc_norm = index.docsTF.computeNorm(docId, index, tfidf)
        for token in doc.keys():
            dot_product += query[token] * doc[token]
            doc_norm += doc[token] ** 2
        for token in query.keys():
            q_norm += query[token] ** 2
        q_norm = sqrt(q_norm)
        doc_norm = sqrt(doc_norm)

        cosine = dot_product / (q_norm*doc_norm) 
        return cosine
    

    def get_ranking(self, query: list)->list:
        q_vector = dict()
        docs_vectors = dict()

        for token in query:
            #query tf-idf vector
            q_tf = query.count(token)
            #consider case in which token is not in list
            try:
                idx = int(self.index.list_of_postings.index(token))
                df = int(self.index.list_of_postings[idx].df)
                q_vector[token] = self.tfidf(q_tf,self.N,df)
            except Exception as e:
                print(e)
                #if a term is not present in any document, it will not be considered 
                continue 
            #print("token:{} q_vector: {}".format(token, q_vector))
            #docs tf-idf vectors
            #docs_vector = index.getDocTF()[docId]
            posting = self.index.list_of_postings[idx].posting
            for d in posting.keys():
                docId = int(d)
                d_tf = posting[docId]
                if docId in docs_vectors:
                    docs_vectors[docId][token]= self.tfidf(d_tf,self.N,df)
                else:
                    docs_vectors[docId] = {}
                    docs_vectors[docId][token] = self.tfidf(d_tf,self.N,df)
                #print("docs_vectors: {}".format(len(docs_vectors[docId])))
        
        for d in docs_vectors.keys():
            doc_vector = docs_vectors[d]
            #print("q_vector: {}, doc_vector: {}".format(q_vector, doc_vector))
            cos_sim = self.cosine(q_vector, doc_vector, d)
            #print("cos_sim: {}".format(cos_sim))
            self.list_cosines.append((cos_sim,d))

        return self.list_cosines

