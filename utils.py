import csv
import string
from tqdm.notebook import tqdm
from typing import *

from bs4 import BeautifulSoup
import nltk
import unidecode
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer

#Downloads for stopwords and punctuation
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('italian')
nltk.download('wordnet')
string.punctuation

def remove_html(text: string):
    soup = BeautifulSoup(text, "html.parser")
    cleaned_text = soup.get_text(separator=" ")
    return cleaned_text

def remove_accented_chars(text: string):
    text = unidecode.unidecode(text)
    return text

def remove_stopwords(text: string):
  output= [i for i in text.split() if i not in stopwords]
  return output

#Removing punctuation
def remove_punctuation(text: string):
  list_without_punctuation = []
  for i in text:
    if i not in string.punctuation:
      list_without_punctuation.append(i)
    else:
      list_without_punctuation.append(' ')
  string_without_punctuation = ''.join(list_without_punctuation)
  return string_without_punctuation

#Removing numbers
def remove_numbers(text: string):
  list_without_numbers = []
  for i in text:
    if i not in '0123456789':
      list_without_numbers.append(i)
    else:
      list_without_numbers.append(' ')
  string_without_numbers = ''.join(list_without_numbers)
  return string_without_numbers


def lemmatizer(text: string):
    wordnet_lemmatizer = WordNetLemmatizer()
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in text]
    return lemm_text

#Stemming

def stemming(text: string):
    italian_stemmer = SnowballStemmer('italian')
    stem_text = [italian_stemmer.stem(word) for word in text if not word.isdigit()]
    return stem_text

def preprocess(text: string, html=1, accent=1, punct=1, numb=1, stop=1, lemma=1, stem=1):
    if html==1:
        text = remove_html(text)
    if accent==1:
        text = remove_accented_chars(text)
    if punct==1:
        text = remove_punctuation(text)
    if numb==1:
        text = remove_numbers(text)
    if stop==1:
        text = remove_stopwords(text)
    if lemma==1:
        text = lemmatizer(text)
    if stem==1:
        text = stemming(text)
    return text