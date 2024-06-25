"""
Macchina Server: Permette di ricevere i messaggi inviati, scriverli in un file csv e avviare una classificazione basata su un modello 
Sub Vector Machine per indicare se la giornata risulta soleggiata o nuvolosa in base a temperatura e umidità (istanze) e le scrive su file.

"""


import time, stomp, os
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import genTest
from scatter import scat


def getPredictions(model):

    #leggo il test
    urlTest = "received.csv"
    test = pd.read_csv(urlTest)  #prendo il csv 

    predictions = model.predict(test) #Le predizioni

    c = np.count_nonzero(predictions) #Conto quanti 1 ho

    
    print(predictions)

    ids = test["RowID"]
    temp=test["Temp"]
    umidity=test["Umidity"]

    with open("predictions.csv", "w") as file:
            file.write(f"Temp,Umidity,ClassP\n")

    #for per la scrittura su file delle predizioni
    for inst,t,u,pred in zip(ids,temp, umidity,predictions):

        with open("predictions.csv", "a") as file:
            file.write(f"{t},{u},{pred}\n")

    scat()
    

    
    
           





def training(model): #Funzione di training
    df = genTest.generate_data_training(800) #genero i file di test 

    #training del modello

    train = df.drop('Class', axis=1).values 
    validation = df['Class'].values 


    scaler = StandardScaler()
    train_scaled = scaler.fit_transform(train)

    # Dividere i dati in set di addestramento e test
    X_train, X_test, y_train, y_test = train_test_split(train, validation, test_size=0.3, random_state=42)
    model.fit(X_train, y_train) #fit sul training e validation

    # Valutare il modello
    predictions = model.predict(X_test) 
    print(classification_report(y_test, predictions))




class MyListener(stomp.ConnectionListener): #definizione del listener 
    
    def __init__(self, conn, model): #costruttore, passo la connessione, utile per ricevere il messaggio e il modello trainato
        self.model = model
        self.c=0
        self.conn=conn

    def on_message(self, frame):
        self.c = self.c+1 #incremento variabile contatore

        #Ricezione del messaggio
        if self.c == 1:
            with open('received.csv', 'w') as file:
                file.write('')

            print("Messaggio ricevuto: " + frame.body)
            file = open("received.csv", "a") #scrittura su file 
            file.write(frame.body)
            file.close() 
            
        else:
            print("Messaggio ricevuto: " + frame.body)
            file = open("received.csv", "a")
            file.write(frame.body)
            file.close()

            if self.c == 21: #se sono arrivato alla fine, predico in base alle mkisurazioni
                print("Comincio la predizione...")
                getPredictions(self.model) 
                self.c=0 #azzero contatore





if __name__ == "__main__":
    
    model = SVC(kernel='linear', C=1.0, shrinking=True) #instanzio il modello da utilizzare 

    training(model) #funzione di training del modello

    conn = stomp.Connection([('127.0.0.1', 61613)]) #connessione con il middleware utilizzato (Activemq)

    conn.set_listener('MyList', MyListener(conn, model)) #listener del ricevente, mi specifica cosa succede 
    conn.connect(wait=True) 

    conn.subscribe(destination='/queue/entry', id=1, ack='auto') #sottoscrivo il server alla queue creata sul middleware

    print("Modello pronto, posso ricevere messaggi...")

    while True:
        time.sleep(30)

    
        



