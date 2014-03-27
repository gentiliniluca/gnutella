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


host = "fd00:0000:0000:0000:f555:e5e7:29d7:79cf"#"::1"
porta = 3331
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
    #pulisco DB
    os.kill(os.getppid(), signal.SIGKILL)
        
    
else: #gestisco funzionalita server 
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,porta))
    s.listen(5)
    while 1:
        print("\t\t\t\t\t\t\t\t\tAttesa richiesta peer")
        client, address = s.accept()
        newpid = os.fork()
        if(newpid==0):
            try:
                s.close()
                

                stringa_ricevuta_server = client.recv(size)
                print("\t\t\t\t\t\t\t\t\tlato server ho ricevuto: "+stringa_ricevuta_server)
                if stringa_ricevuta_server== "":
                    print("\t\t\t\t\t\t\t\t\t\t\t\tsocket vuota")
                    break
                print("\t\t\t\t\t\t\t\t\tMESSAGGIO RICEVUTO:" )
                operazione=stringa_ricevuta_server[0:4]

        #operazione NEAR
                if operazione.upper()=="NEAR":
                    pktid=stringa_ricevuta_server[4:20]
                    ipp2p=stringa_ricevuta_server[20:58]
                    pp2p=stringa_ricevuta_server[58:63]
                    ttl=stringa_ricevuta_server[63:65]
                    print ("\t\t\t\t\t\t\t\t\tOperazione Near pktid: "+pktid+" ip: "+ ipp2p +" porta: " +pp2p+ " ttl: "+ttl)

                    ttl=int(ttl)-1
                    conn_db=Connessione.Connessione()
                    try:
                        pkt=PacketService.PacketService.getPacket(conn_db.crea_cursore(), pktid)
                    except:
                        print ("pkt non presente , se ttl >0 invio")
                        if(ttl>0):
                            #inserisco su db e invio a vicini tranne mittente
                            vicini= []
                            vicini = NearService.NearService.getNears(conn_db.crea_cursore(), pktid)
                            i=0
                            while i < len(vicini):
                                if(vicini[i].ipp2p!=ipp2p and vicini[i].pp2p!=pp2p):
                                    print ("inoltro near a vicini****" +" "+vicini[i].pp2p + " "+vicini[i].ipp2p)
                                    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                                    sock.connect((vicini[i].ipp2p, int(vicini[i].pp2p)) )
                                    sock.send(stringa_ricevuta_server.encode())
                                i = i+1
                            stringa_risposta="ANEA"+pktid+host+adattaStringa(5,str(porta))
                            #print(stringa_risposta)
                            
                            sockr = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                            sockr.connect((ipp2p, int(pp2p)) )
                            sockr.send(stringa_risposta.encode())
                            
                    finally:
                        conn_db.esegui_commit()
                        conn_db.chiudi_connessione()
        #fine operazione NEAR
        
        #operazione ANEA
                if operazione.upper()=="ANEA":
                    pktid=stringa_ricevuta_server[4:20]
                    ipp2p=stringa_ricevuta_server[20:58]
                    pp2p=stringa_ricevuta_server[58:63]
                    print ("\t\t\t\t\t\t\t\t\tOperazione Near pktid: "+pktid+" ip: "+ ipp2p +" porta: " +pp2p)

        


            except Exception as e: 
                print e
                print("\t\t\t\t\t\t\t\t\tErrore ricezione lato server")
            finally:
                client.close() 
                os._exit(0) 
                
        else:
            client.close()
    
    print("Terminato parte server")
            
                    


