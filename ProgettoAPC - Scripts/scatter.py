import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pandas as pd
import numpy as np

# Dati di esempio


def scat():

    file = pd.read_csv('predictions.csv')


    temp = file["Temp"]
    umid = file["Umidity"]
    pred = file["ClassP"]

    # Caricare l'immagine da usare come marker
    img = mpimg.imread('cloudy.png')  # Assicurati che l'immagine sia nel formato supportato (es. PNG)

    imgsun = mpimg.imread('sun.png')

    imgrainy = mpimg.imread('rainy.png')

    imgsuncloud = mpimg.imread('sun-cloud.png')


    # Creare una figura e un asse
    fig, ax = plt.subplots()

    # Creare lo scatter plot con marker vuoti (per evitare punti di default)
    ax.scatter(temp, umid, alpha=0)  # alpha=0 rende i punti invisibili


    # Calcola la regressione lineare
    coefficients = np.polyfit(temp, umid, 1)
    polynomial = np.poly1d(coefficients)


    # Disegna la linea di regressione
    x_line = np.linspace(min(temp), max(temp), 100)
    y_line = polynomial(x_line)
    ax.plot(x_line, y_line, color='blue', linewidth=2)



    # Aggiungere l'immagine ai punti
    for i,j,z  in zip(pred,temp,umid):
        if i == 0:
            imagebox = OffsetImage(img, zoom=0.1)  # Regola lo zoom a seconda della dimensione dell'immagine
            ab = AnnotationBbox(imagebox, (j,z), frameon=False)
            ax.add_artist(ab)
        elif i == 1: 
            imagebox = OffsetImage(imgsun, zoom=0.1)  # Regola lo zoom a seconda della dimensione dell'immagine
            ab = AnnotationBbox(imagebox, (j,z), frameon=False)
            ax.add_artist(ab)
        elif i == 2:
            imagebox = OffsetImage(imgsuncloud, zoom=0.1)  # Regola lo zoom a seconda della dimensione dell'immagine
            ab = AnnotationBbox(imagebox, (j,z), frameon=False)
            ax.add_artist(ab)
        else:
            imagebox = OffsetImage(imgrainy, zoom=0.1)  # Regola lo zoom a seconda della dimensione dell'immagine
            ab = AnnotationBbox(imagebox, (j,z), frameon=False)
            ax.add_artist(ab)



    plt.xlabel('Temperature')
    plt.ylabel('Umidity')
    plt.title('Predizioni')
    plt.show()


