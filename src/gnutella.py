# coding: utf-8
import socket
import os
import sys
import subprocess, signal
import Packet
import PacketService
import File
import FileService
import Connessione
import Near
import NearService

def visualizza_menu_principale():
    print("\n************************\n*  1 - Ricerca File    *\n*  2 - Ricerca vicini  *\n*  0 - Fine            *\n************************")
    out=raw_input("\n\tOperazione scelta: ")
    return out

def adattaStringa(lunghezzaFinale, stringa):
    ritorno=stringa
    for i in range(len(stringa), lunghezzaFinale):
        ritorno="0"+ritorno
    return ritorno


host = "::1"
porta = 3000
size = 1024
ttl = 2

print ("Avvio Directory distribuito")
pid=os.fork()
if(pid==0): #figlio per gestire operazioni menu
    operazione_utente=1
    while(int(operazione_utente)!=0):
        operazione_utente=visualizza_menu_principale()
        print("valore: "+ operazione_utente)
        
        #operazione ricerca vicini
        if(int(operazione_utente)==2):
            conn_db=Connessione.Connessione()
            pkt= PacketService.PacketService.insertNewPacket(conn_db.crea_cursore())
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
             
            stringa_da_trasmettere="NEAR"+pkt.packetid+host+""+adattaStringa(5,str(porta))+adattaStringa(2,str(ttl)) 
            print("valore inviato: "+stringa_da_trasmettere)
            #lettura vicini da db
            conn_db=Connessione.Connessione()
            vicini= []
            vicini = NearService.NearService.getNears(conn_db.crea_cursore(), pkt.packetid)
            i=0
            while i < len(vicini):
                print ("****" +" "+vicini[i].pp2p + " "+vicini[i].ipp2p)
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                sock.connect((vicini[i].ipp2p, int(vicini[i].pp2p)) )
                sock.send(stringa_da_trasmettere.encode())
                i = i+1
                
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
            
                     
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
            
                    


