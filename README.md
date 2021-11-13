# Search-Engine
Project made as assignment for the Data Mining course (winter 2021).
To lunch the program use the command: python main.py.

In the main I just get the path for the tsv file (docs/jobs.tsv) containing all the jobs announcements I scraped in the first Homework, build the index, open it again (as if the search happened later in a second moment) and then start the search engine.

All the code needed to build and mantain the inverted index is in the inverted_index.py file, where I defined three classes: PostingList, DocsTF and InvertedIndex. 
PostingList contains, stored in a dictionary, all the couples {docId:tf} relative to a certain word and the total number of documents that have this token. I defined methods that are used to update the postings list, load a posting from somewhere else (the posting is given as input to the function) and I also defined other methods that are useful for debugging (get a particular attribute, print the postings etc).
I use the DocsTF class to store the term frequencies for the tokens that are present in each document. Also in this case a dictionary is used to access the TF of documents in a fast way. The methods that are more relevant are computeTF(), that uses a Counter to get the TFs for the document from the list of words, and writeDocTF(), which has as a task to write in each row of a tsv file the docId of a document and the corresponding dictionary of {words:TF}.
The last class for this file is InvertedIndex. This is the most important class of the three since it has to do all the work. It stores a list of the postings lists for all the tokens that are present in the announcements, plus other useful values for the index (total number of documents, number of words, number of tokens in each document and so on). Once an object of this class is created, we can populate it using two different methods: 

- buildIndex() reads the tsv file that stores all the jobs announcements, preprocess the fields we are interested in (title, description and location), create the PostingList needed for the tokens, populate the DocsTF object and, at the end, write everything on files (one for the inverted index, one for the DocTF and one for the useful values). The index.tsv file has one column for the words, one for the document frequency and a third one for the postings lists; the docs\_tf.tsv file has just two column, one for the docId and one for the dictionary which stores the term frequencies; the index_values.tsv stores in three columns the number of documents, the total number of words and a dictionary with the length of the documents;
- openIndex() instead, loads all the data we need from the tsv files mentioned above and then creates and populates the right objects (for posting lists and so on). The module used to read the dictionaries is <i>ast</i>, that, thanks to the utility function literal_eval(), doesn't have problems with the types of the fields of the dictionaries while reading it (json.loads() gave several problems with this part).


The preprocessing of the announcements is done by functions defined into utils.py. I implemented functions to clean the textual data from html elements, accented chars, stopwords, punctuation and numbers and there are also two functions devoted to apply stemming and lemmatization to the tokens. By calling the function preprocess() I can decide which actions, from the ones listed above, perform on the strings. At the end I decided to use all the previous functions, except for lemmatizer() and remove_accented_chars() because the stemmer does a better job than the lemmatizer and it makes little sense to use both accented_chars() and the stemmer, but I kept them in the code anyway. The libraries used to perform such operations are: <i>BeautifulSoup</i>, <i>nltk</i> and <i>unidecode</i>.

At this point the inverted index is created (or uploaded) and we can use the actual search engine. After calling the search() function we can type a query (or 'q' to quit) which is going to be preprocessed and then given as input to the Ranking class that is going to produce a list of documents that have at least one of the words that were typed by the user and the scores for such documents. The ranking class is defined into the cosine.py file. The ranking class' major methods is get_ranking() that, given a query, for each of its token, computes the tf-idf values for both the query and the documents, the normalization of the two vectors and then the cosine similarity using these values. The tf-idf used here has the following formula: tf_-idf = 1+log(tf)*log(N/df), where N is the total number of documents. The norm of the documents is computed through compute_doc_norm(), that reads from the doc_tfs.tsv file the row related to the considered docId. In the end, the cosine() method computes the dot product between the query vector and the document vector (which has only the TFs values for the terms that are present in the query, i.e. I didn't compute or retrieve all the TFs values, since they were going to be multiplied by zero) and normalizes by dividing by the product of the two norms. Once the cosine values are computed and stored in a list, we are back into the main and here a heap is used to get the best 5 documents for our query, of which we print the docId and the link field.

Some examples of queries and results:

- Simple query of one common word:
![rome_q](https://user-images.githubusercontent.com/49344669/141647224-a86645bf-3010-4b0f-838e-ce533518225b.jpeg)

- Query of a word not present in the index:

![seneca_q](https://user-images.githubusercontent.com/49344669/141647227-a062baa0-60d6-47d3-96e3-d894a3b29b50.jpeg)

- Longer query:
![design_q](https://user-images.githubusercontent.com/49344669/141647221-2b13235b-d3fa-448e-bd98-534624ab191a.jpeg)

- Short query of an uncommon word:
![able_q](https://user-images.githubusercontent.com/49344669/141647282-bd24a281-bded-441a-9fab-7b462672fdb9.jpeg) 

- Query taken from one description of a job:
![long_query](https://user-images.githubusercontent.com/49344669/141647222-7f141066-db27-4cca-bb52-43252e93e96d.jpeg)

In the last image there are lots of results for the query composed by a whole announcement and it could seem surprising that so many of them have very high score (>=0.90), but this fact can be explained by pointing out that jobs.csv has a lot of similar announcements (or even duplicates as in this case).
