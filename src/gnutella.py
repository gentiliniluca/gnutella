# coding: utf-8
import socket
import os
import sys
import subprocess, signal

def visualizza_menu():
    print("\n************************\n*  1 - Ricerca File    *\n*  2 - Ricerca vicini  *\n*  0 - Fine            *\n************************")
    out=raw_input("\n\tOperazione scelta: ")
    return out


host = "::1"
porta = 3000
size = 1024

print ("Avvio Directory distribuito")
pid=os.fork()
if(pid==0): #figlio per gestire operazioni menu
    operazione_utente=1
    while(int(operazione_utente)!=0):
        operazione_utente=visualizza_menu()
        print("valore: "+ operazione_utente)
        
    print("fine operazioni utente")
    os.kill(os.getppid(), signal.SIGKILL)
        
    
else: #gestisco funzionalita server 
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,porta))
    s.listen(5)
    while 1:
        print("Attesa richiesta peer")
        client, address = s.accept()
        newpid = os.fork()
        if(newpid==0):
            try:
                s.close()

                stringa_ricevuta = client.recv(size)
                if stringa_ricevuta== "":
                    print("\t\tsocket vuota")
                    break
                print("\tMESSAGGIO RICEVUTO:" )
                operazione=stringa_ricevuta[0:4]

                #operazione Login
                if operazione.upper()=="LOGI":
                    ipp2p=stringa_ricevuta[4:43]
                    pp2p=stringa_ricevuta[43:48]
                    print ("\t\tOperazione Login ipp2p: "+ipp2p+" porta: "+pp2p)

                    print("\t\tRestituisco: "+"ALGI"+sessionID)
                    client.send("ALGI"+sessionID)



            except Exception as e: 
                print e
                print("Errore ricezione")
            finally:
                client.close() 
                os._exit(0) 
                
        else:
            client.close()
    
    print("Terminato parte server")
            
                    


