"""
Programma per la lettura dei dati dalla porta virtuale COM3 generata dalla scheda STM32F3, con cui comunica tramite UART. 
Il programma legge le acquisizioni fatte dal sensore di temperatura inviate dalla scheda sulla porta COM3 (20 per scelta progettuale), le scrive su un file "entries.txt" 
e alla fine del processo genera un file chiamato "dump.dat", che permette l'avvio del programma "sender". 

"""


import serial



if __name__ == "__main__":
    port = 'COM3'

    c=0 #contatore utile per capire le acquisizioni scritte

    
    try:
        
        ser = serial.Serial(port, 38400) #Connessione verso la porta COM3 con baudrate 38400 (di default UART STM32). 
        
        print(f"Connesso a {ser.name} al baud rate {ser.baudrate}")  

        with open("entries.txt", "w") as file:  #scrivo all'inizio del file le feature che caratterizzano le istanze 
            file.write("RowID,Temp,Umidity\n")
        

        while True:

            while c!=20:  #sono in while finché non faccio 21 letture (1 di "flush" + 20 dati)
                
                if ser.in_waiting > 0: #se ci sono messaggi in attesa allora lo leggo 


                    line = ser.readline().decode('iso-8859-1').rstrip() #leggo e decodifico il messaggio
                    line = line.replace('\x00','') #scrematura, dei valori null 
                    line = line.replace('\x0f','') #scrematura, dei valori null 
                    line = line.replace('\r\n','') #tolgo eventuali caratteri finali

                    print(line)
                    line = line.split(',') #split sul carattere virgola
                    line= str(int(float(line[0]))) +","+str(round(float(line[1]),2))+","+str((round(float(line[2]),2))) #casting dei dati inviati
                    

                    with open("entries.txt", "a") as file: #scrivo la linea nel file 
                        file.write(str(line)+"\n")

                    
                    c=c+1; #aumento contatore 
                        
            f = open("dump.dat", "x") #crea il file 
            f.close() #chiudo per evitare errori 
            c=0


              
    except Exception as e:
        print(f"Errore durante la lettura dei dati: {e}")

    finally:
        # Chiudi la connessione alla fine
        ser.close()
        print("Connessione chiusa.")