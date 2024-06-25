import numpy as np
import pandas as pd

def generate_data_training(n_samples):
    # Genera valori casuali per temperatura e umidità percentuale
    temperature = np.round(np.random.uniform(10, 30, n_samples), 2)
    humidity_percentage = np.round(np.random.uniform(20, 80, n_samples), 2)
    
   
    # Soglie arbitrarie per decidere i diversi stati del tempo
    sunny_condition = (temperature > 20) & (humidity_percentage < 60) #sole
    partly_sunny_condition = ((temperature >= 15) & (temperature <= 25)) & (humidity_percentage < 70) #parzialmente soleggiato
    rainy_condition = (temperature < 15) | (humidity_percentage > 70) #piovoso
    
    # Crea le etichette di classe
    labels = np.where(sunny_condition, 1, np.where(partly_sunny_condition, 2, np.where(rainy_condition, 3, 0))) #0 indica nuvoloso
    
    # Crea il DataFrame
    df = pd.DataFrame({
        'RowID': range(1, n_samples + 1),
        'Temp': temperature,
        'Umidity': humidity_percentage,
        'Class': labels
    })
    

    print(df) 
    return df


def generate_data_tosend():
        # Genera valori casuali per temperatura e umidità percentuale
        temperature = np.round(np.random.uniform(10, 30, 20), 2)
        humidity_percentage = np.round(np.random.uniform(20, 80, 20), 2)
        
      
        # Crea il DataFrame
        df = pd.DataFrame({
            'RowID': range(0, 20),
            'Temp': temperature,
            'Umidity': humidity_percentage
        })
        

        print(df) 
        return df




