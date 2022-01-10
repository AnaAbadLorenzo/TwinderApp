import pickle

import pandas as pd
import os
import pathlib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report

def run():

    """importar el dataset"""

    fn_dataset = os.path.join(pathlib.Path(__file__).parent.resolve(), 'archive', 'tweet_emotions.csv')
    print(40 * "*")
    print(fn_dataset)
    print(40 * "*")
    trainingData = pd.read_csv(fn_dataset)

    print(trainingData)

    """Tokenizar and stopwords removal"""

    nltk.download('punkt')
    nltk.download('stopwords')

    ps = PorterStemmer()

    preprocessedText = []

    for row in trainingData.itertuples():
        text = word_tokenize(row[3])  ## indice de la columna que contiene el texto
        ## Remove stop words
        stops = set(stopwords.words("english"))
        text = [ps.stem(w) for w in text if not w in stops and w.isalnum()]
        text = " ".join(text)

        preprocessedText.append(text)

    preprocessedData = trainingData
    preprocessedData['processed_text'] = preprocessedText

    len(preprocessedData.index)
    print(preprocessedData)
    print(preprocessedData['sentiment'].value_counts())

    """Bag of Words"""

    bagOfWordsModel = TfidfVectorizer()
    bagOfWordsModel.fit(preprocessedData['processed_text'])
    textsBoW= bagOfWordsModel.transform(preprocessedData['processed_text'])
    print("Finished")

    print(textsBoW.shape)
    """Support Vector Machine trainee"""

    svc = svm.SVC(kernel='linear') #Modelo de clasificación

    X_train = textsBoW #Documentos
    Y_train = preprocessedData['sentiment'] #Etiquetas de los documentos
    svc.fit(X_train, Y_train) #Entrenamiento

    fn_svc = os.path.join(pathlib.Path(__file__).parent.resolve(), 'archive', 'model.sav')
    pickle.dump(svc, open(fn_svc,'wb'))

    fn_bow = os.path.join(pathlib.Path(__file__).parent.resolve(), 'archive', 'bag.sav')
    pickle.dump(bagOfWordsModel, open(fn_bow, 'wb'))

    print("Model saved on \""+ os.path.join(pathlib.Path(__file__).parent.resolve(), 'archive', 'bag.sav') +"\" properly")

def getResult(tweets, fn_svc=os.path.join(pathlib.Path(__file__).parent.resolve(), 'archive', 'model.sav'),
              fn_bow=os.path.join(pathlib.Path(__file__).parent.resolve(), 'archive', 'bag.sav')):    # REVISAR
    print("************ Inicio del método ************")
    misTweets = tweets
    ps = PorterStemmer()
    preprocessedText = []

    print("*** Tokenizando tweets ***")
    for row in misTweets:
        text = word_tokenize(row)  ## indice de la columna que contiene el texto
        ## Remove stop words
        stops = set(stopwords.words("english"))
        text = [ps.stem(w) for w in text if not w in stops and w.isalnum()]
        text = " ".join(text)

        preprocessedText.append(text)

    preprocessedData = pd.DataFrame()
    preprocessedData['processed_text'] = preprocessedText

    print("*** Cargando SVC entrenada y su modelo de Bag Of Words ***")
    loaded_svc = pickle.load(open(fn_svc, 'rb'))

    bagOfWordsModel = pickle.load(open(fn_bow, 'rb'))

    textsBoW = bagOfWordsModel.transform(preprocessedData['processed_text'])

    X_data = textsBoW  # Documentos

    predictions = loaded_svc.predict(X_data)  # Se almacenan las predicciones del clasificador

    print("************ Fin del método ************")
    return predictions

if __name__ == '__main__':
    run()