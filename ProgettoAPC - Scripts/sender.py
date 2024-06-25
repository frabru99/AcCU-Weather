import stomp, time, os, sys, genTest
from pathlib import Path



if __name__ == "__main__":
    #non vado avanti finché non è creato dump.txt
    #print(Aspetto creazione dump...)
    assert len(sys.argv) == 2, "Inserisci IP per MOM"

    while True:


        #codice utile a generare istanze di test, da eliminare poi
        """
        df = genTest.generate_data_tosend() 

        with open('entries.txt', 'w') as file:
            file.write('')
            wr = df.to_csv(index=False)
            val = wr.replace('\n','')
            file.write(val)

            s
        """

        print("\nSistema pronto a ricevere nuove misurazioni...")

        file_path = Path('dump.dat')

        while not file_path.exists():
            time.sleep(1)

        #appenaho il dump significa che entries.txt è pronto
        file = open("entries.txt", "r")

        lines = file.readlines() #leggo il file

        print(lines)

        #invio i messaggi con stomp
        conn = stomp.Connection([(str(sys.argv[1]),61613)]) #sostituire con indirizzo ip server ActiveMQ
        conn.connect(wait=True) #mi connetto 

        print("Connesso correttamente, invio i messaggi...\n")

        os.remove('dump.dat') #rimozione file di dump per prossime iterazioni

        for i in range (0,21): #invio le entries
            msg = str(lines[i])
            print("Invio messaggio " + msg)

            conn.send('/queue/entry', msg)

        with open("entries.txt", "w") as file:  #resetto il file delle entries inviate
                file.write("RowID,Temp,Umidity\n")
        

            






        






