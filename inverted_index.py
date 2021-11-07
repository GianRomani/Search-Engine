from utils import *
import ast

class PostingList:
    """
    class for a single posting list, relative to the token self.word
    """
    def __init__(self, word: string):
        self.word = word
        self.df = 0 #document frequency -> how many documents have this token
        self.posting = dict() #{docId:tf}

    def putDoc(self, docId: int):
        """We receive as input theinteger defining the doc to put in the postings list if not already present, 
            otherwise increment the TF

        Args:
            docId (int): integer defining which doc to consider
        """
        if docId not in self.posting:
            self.posting[docId] = 1
            self.df += 1
        else:
            self.posting[docId] += 1

    def loadDoc(self, df:int, posting:dict):
        """to load and populate a posting list from a file we need the df and the postings list

        Args:
            df (int): document frequency -> how many documents have this token
            posting (dict): posting list {docId:tf}
        """
        self.df = df
        self.posting = posting

    def __str__(self) -> string:
        return "Word: %s, df: %s -> posting list: %s" %(self.word, self.df, self.posting)

    def getDocTF(self,docId: int) -> int:
        if self.posting[docId]:
            return self.posting[docId]
        else:
            return 0

    def getDocs(self) -> dict:
        return self.posting
    
    def __eq__(self, other) -> bool:
        return (self.word == other)

class DocsTF:
    """Class used to save for each document the TFs for the tokens
    """
    def __init__(self):
        self.docs_dict = dict()

    def computeTF(self, words:list) -> dict:
        """Use a Counter to obtain the TF of the tokens from the list words

        Args:
            words (list): list of tokens from description, title and location of the announcements

        Returns:
            dict: {token:TF}
        """
        counter = Counter(words)
        return counter

    def addDoc(self, docId:int, list_of_words:list):
        self.docs_dict[docId] = self.computeTF(list_of_words)

    #load from the docs_tfs.tsv file
    def loadDoc(self, docId:int, tfs:dict):
        self.docs_dict[int(docId)] = tfs

    def writeDocTF(self, path:str):
        """Write ona tsv file the data about TF of tokens into documents 

        Args:
            path (str): path of the file where to write
        """
        self.path = path
        with open(self.path, 'w') as f:
            writer = csv.writer(f, delimiter='\t')
            header = ["docId", "tf_dict"]
            writer.writerow(header)
            for id,tfs in self.docs_dict.items():
                data = []
                data.append(id) 
                data.append(dict(tfs))
                writer.writerow(data)
        f.close()

class InvertedIndex:
    """Class that implements the Inverted index and all its functionalities
    """
    def __init__(self):
        self.list_of_postings=[]
        self.doc_len = dict()
        self.docs_number = 0
        self.word_number = 0
        self.docsTF = DocsTF() 

    def addPosting(self, posting: PostingList):
        """Add a new posting to the list of postings of the inverted index

        Args:
            posting (PostingList): PostingList object containing a word and dict {docId:TF}
        """
        self.list_of_postings.append(posting)

    def searchWord(self, word: str) -> PostingList:
        """Check if there is already a posting list for a certain word

        Args:
            word (str): token 

        Returns:
            PostingList: PostingList if the token was already knew, None otherwise
        """
        for pos in self.list_of_postings:
            if pos.word == word:
                return pos
        return None        

    def addSingleWord(self, word: str, docId: int):
        """Add a single word to the posting if this is not know, otherwise just add a new document to the token's posting

        Args:
            word (str): token to be added
            docId (int): document wheer the token is present
        """
        posting = self.searchWord(word)
        if not posting:
            newPosting = PostingList(word)
            self.addPosting(newPosting)
            newPosting.putDoc(docId)
        else:
            posting.putDoc(docId)
        self.word_number += 1

    def addWords(self, words: list, docId: int):
        for word in words:
            self.addSingleWord(word, docId)

    def sortIndex(self) -> list:
        """Sort index before writing it in a file

        Returns:
            list: sorted version of the list of postings
        """
        return sorted(self.list_of_postings, key=lambda x: x.word)

    def writeIndexOnFile(self):
        """
        Write the index on index.tsv
        """
        ordered_list = self.sortIndex()
        header=["word", "df", "posting list"]
        with open(self.path_index, 'w') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(header)
            for post in ordered_list:
                data = []
                data.append(post.word) 
                data.append(post.df)
                data.append(post.posting)
                writer.writerow(data)
        f.close()    

    def writeValuesOfIndex(self):
        """
        Write on the files that keeps interesting values of the index
        """
        header=["docs_number", "word_number", "doc_len"]
        with open(self.path_index_values, 'w') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(header)
            data = []
            data.append(self.docs_number) 
            data.append(self.word_number)
            data.append(self.doc_len)
            writer.writerow(data)
        f.close()

    def buildIndex(self, path: str):
        """Build an inverted inde from the jobs.tsv file

        Args:
            path (str): path to where we want to locate all the files
        """
        self.path_docs = path + "jobs.tsv"
        self.path_doc_tfs = path + "doc_tfs.tsv"
        self.path_index = path + "index.tsv"
        self.path_index_values = path + "index_values.tsv"
        with open(self.path_docs, 'r') as f:
            read_tsv = csv.reader(f, delimiter="\t")
            next(read_tsv) #just the head
            for i,row in enumerate(read_tsv):
                try:
                    doc_id = i+2
                    title = preprocess(row[0]) #title
                    self.addWords(title, doc_id)
                    description = preprocess(row[1]) #description
                    self.addWords(description, doc_id)
                    location = preprocess(row[2])  #location
                    self.addWords(location, doc_id)
                    self.doc_len[doc_id] = len(title) + len(description) + len(location) 
                    self.docs_number += 1
                    bag_of_words = title+description+location
                    self.docsTF.addDoc(doc_id,bag_of_words)
                except Exception as e:
                    print(e)
                    break  
        f.close()
        #now save everything in the files
        self.writeIndexOnFile()
        self.writeValuesOfIndex()
        self.docsTF.writeDocTF(self.path_doc_tfs)
        print("Index built with success!")

    def getDocTF(self)->dict:
      return self.docsTF.docs_dict

    def openIndex(self, path:str):
        """Load the data from the files created by buildIndex() in a new index

        Args:
            path (str): path to location of the files
        """
        self.path_docs = path + "jobs.tsv"
        self.path_doc_tfs = path + "doc_tfs.tsv"
        self.path_index = path + "index.tsv"
        self.path_index_values = path + "index_values.tsv"
        #Load the index
        with open(self.path_index, 'r') as f_index:
            read_tsv = csv.reader(f_index, delimiter="\t")
            next(read_tsv) #just the head
            for i,row in enumerate(read_tsv):
                try:
                    word = row[0]
                    df = int(row[1])
                    posting = ast.literal_eval(row[2])
                    newPosting = PostingList(word)
                    newPosting.loadDoc(df, posting)
                    self.addPosting(newPosting)
                except Exception as e:
                    print(e)
                    break  
        f_index.close()
        #Load useful information of the index
        with open(self.path_index_values, 'r') as f_values:
            read_tsv = csv.reader(f_values, delimiter="\t")
            next(read_tsv) #just the head
            for i,row in enumerate(read_tsv):
                try:
                    self.docs_number = int(row[0])
                    self.word_number = int(row[1])
                    self.doc_len = ast.literal_eval(row[2])
                except Exception as e:
                    print(e)
                    break  
        f_values.close()
        #Load the DocTfs file
        with open(self.path_index_values, 'r') as f_docsTfs:
            read_tsv = csv.reader(f_docsTfs, delimiter="\t")
            next(read_tsv) #just the head
            for i,row in enumerate(read_tsv):
                try:
                    docId = int(row[0])
                    doc_tfs= ast.literal_eval(row[1])
                    self.docsTF.loadDoc(docId, doc_tfs)
                except Exception as e:
                    print(e)
                    break  
        f_docsTfs.close()
        print("Inverted index loaded successfully!")
        

    def printIndex(self, number=0):
        if number == 0:
            for post in self.list_of_postings:
                print(post)
                print()
        else:
            for i in range(number):
                print(self.list_of_postings[i])
                print()