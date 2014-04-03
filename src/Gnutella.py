import Client 
import Server 
import Util
import os

class Gnutella:
    host = "::1"
    porta = 3331
    ttl = 2
    
    print("Avvio directory distribuita")
    
    pid = os.fork()
    if(pid == 0): #figlio per gestire operazioni menu
        operazione_utente = 1
        while(int(operazione_utente) != 0):
            operazione_utente = Client.Client.visualizza_menu_principale()
            print("Valore: " + operazione_utente)
            
            #ricerca file
            if(int(operazione_utente) == 1):            
                Client.Client.searchHandler()
            
            #ricerca vicini
            if(int(operazione_utente) == 2):            
                Client.Client.nearHandler() 
                
            #aggiunta file
            if(int(operazione_utente) == 3):            
                Client.Client.addFile()             
                       
                     
        print("Fine operazioni utente")
        #pulisco DB quando esco
        os.kill(os.getppid(), signal.SIGKILL)
        
    else: #gestisco funzionalita server 
        s = Sever.Server.initServerSocket()
        while 1:
            print("\t\t\t\t\t\t\t\t\tAttesa richiesta peer")
            client, address = s.accept()
            newpid = os.fork()
            if(newpid == 0):
                try:
                    s.close()
                                        
                    #pulizia pkt vecchi da 300 s        
                    Server.Server.expiredPacketHandler()
                                    
                    receivedString = Server.Server.readSocket(client)
                    operazione = receivedString[0:4]
                    
                    if operazione == "":
                        break
                                                            
                    #operazione NEAR
                    if operazione.upper() == "NEAR":
                        Server.Server.nearHandler(receivedString)                    
        
                    #operazione ANEA
                    if operazione.upper() == "ANEA":
                        Server.Server.addNewNear(receivedString)
                        
                    #operazione RETR
                    if operazione.upper() == "RETR":
                        Server.Server.uploadHandler(client, receivedString)

                except Exception as e: 
                    print e
                    print("\t\t\t\t\t\t\t\t\tErrore ricezione lato server")
                    
                finally:
                    client.close() 
                    stringa_ricevuta_server = ""
                    os._exit(0) 
                
            else:
                client.close()
    
        print("Terminato parte server")
    
    