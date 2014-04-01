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
    
    while True:
        print("\n************************\n*  1 - Ricerca File    *\n*  2 - Ricerca vicini  *\n*  3 - Carica File     *\n*  0 - Fine            *\n************************")
        out=raw_input("\n\tOperazione scelta: ")
        if(int(out)>=0 and int(out)<=3):
            break
        print("Valore inserito errato! (valore compreso tra 0 e 3)")
    return out

def aggiungi_spazi_finali(stringa):
    i=len(stringa)
    while i<20:
        stringa=stringa+' '
        i=i+1
    return stringa

def adattaStringa(lunghezzaFinale, stringa):
    ritorno=stringa
    for i in range(len(stringa), lunghezzaFinale):
        ritorno="0"+ritorno
    return ritorno

def elimina_spazi_iniziali_finali(stringa):
    ritorno=""
    ritorno2=""
    lettera=False
    lettera2=False
    for i in range (0,len(stringa)):
        if(stringa[i]!=" " or lettera==True):
            ritorno=ritorno+stringa[i]
            lettera = True
   
    ritorno= ritorno[::-1]   

    for i in range (0,len(ritorno)):
        if(ritorno[i]!=" " or lettera2==True):
            ritorno2=ritorno2+ritorno[i]
            lettera2 = True

    return ritorno2[::-1]

host = "0000:0000:0000:0000:0000:0000:0000:0001" #"fd00:0000:0000:0000:f555:e5e7:29d7:79cf"#"::1"
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
        
        #operazione ricerca
        
        if(int(operazione_utente)==1):
            
            while True:
                query_ricerca=raw_input("\n\tInserire la stringa di ricerca (massimo 20 caratteri): ")
                if(len(query_ricerca)<=20):
                    break
                print("\n\tErrore lunghezza query maggiore di 20!")
            
            query_ricerca=aggiungi_spazi_finali(query_ricerca)
            print(query_ricerca)    
            
            
            conn_db=Connessione.Connessione()
            pkt= PacketService.PacketService.insertNewPacket(conn_db.crea_cursore())
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
            ttl=2
            stringa_da_trasmettere="QUER"+pkt.packetid+host+""+adattaStringa(5,str(porta))+adattaStringa(2,str(ttl))+query_ricerca
            
            #print("stringa inviata dal client: "+stringa_da_trasmettere)
            
            conn_db=Connessione.Connessione()
            vicini= []
            vicini = NearService.NearService.getNears(conn_db.crea_cursore())
            i=0
            while i < len(vicini):
                #print ("****" +" "+vicini[i].pp2p + " "+vicini[i].ipp2p)
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                sock.connect((vicini[i].ipp2p, int(vicini[i].pp2p)) )
                sock.send(stringa_da_trasmettere.encode())
                i = i+1
                
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
            
        
        #operazione ricerca vicini
        if(int(operazione_utente)==2):
            conn_db=Connessione.Connessione()
            pkt= PacketService.PacketService.insertNewPacket(conn_db.crea_cursore())
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
            ttl=2
            stringa_da_trasmettere="NEAR"+pkt.packetid+host+""+adattaStringa(5,str(porta))+adattaStringa(2,str(ttl)) 
            #print("valore inviato: "+stringa_da_trasmettere)
            #lettura vicini da db
            conn_db=Connessione.Connessione()
            vicini= []
            vicini = NearService.NearService.getNears(conn_db.crea_cursore())
            i=0
            while i < len(vicini):
                #print ("****" +" "+vicini[i].pp2p + " "+vicini[i].ipp2p)
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                sock.connect((vicini[i].ipp2p, int(vicini[i].pp2p)) )
                sock.send(stringa_da_trasmettere.encode())
                i = i+1
                
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
            
                     
    print("fine operazioni utente")
    #pulisco DB quando esco
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
        #pulizia pkt vecchi da 300 s
                conn_db=Connessione.Connessione()
                PacketService.PacketService.deleteExpiredPacket(conn_db.crea_cursore())
                conn_db.esegui_commit()
                conn_db.chiudi_connessione()
        #fine pulizia pkt vecchi
                
                stringa_ricevuta_server = client.recv(size)
                print("\t\t\t\t\t\t\t\t\tlato server ho ricevuto: "+stringa_ricevuta_server)
                if stringa_ricevuta_server== "":
                    print("\t\t\t\t\t\t\t\t\t\t\t\tsocket vuota")
                    break
                print("\n\t\t\t\t\t\t\t\t\tMESSAGGIO RICEVUTO:" )
                operazione=stringa_ricevuta_server[0:4]

        #operazione NEAR
                if operazione.upper()=="NEAR":
                    pktid=stringa_ricevuta_server[4:20]
                    ipp2p=stringa_ricevuta_server[20:59]
                    pp2p=stringa_ricevuta_server[59:64]
                    ttl=stringa_ricevuta_server[64:66]
                    print ("\t\t\t\t\t\t\t\t\tOperazione Near pktid: "+pktid+" ip: "+ ipp2p +" porta: " +pp2p+ " ttl: "+ttl)

                    ttl=int(ttl)-1
                    conn_db=Connessione.Connessione()
                    try:
                        pkt=PacketService.PacketService.getPacket(conn_db.crea_cursore(), pktid)
                    except:
                        print ("\t\t\t\t\t\t\t\t\tpkt non presente , se ttl >0 invio")
                        if(ttl>=0):
                            # invio a vicini tranne mittente
                            vicini= []
                            vicini = NearService.NearService.getNears(conn_db.crea_cursore())
                            i=0
                            while i < len(vicini):
                                if(vicini[i].ipp2p!=ipp2p and vicini[i].pp2p!=pp2p):
                                    print ("\t\t\t\t\t\t\t\t\tinoltro near a vicini****" +" "+vicini[i].pp2p + " "+vicini[i].ipp2p)
                                    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                                    sock.connect((vicini[i].ipp2p, int(vicini[i].pp2p)) )
                                    stringa_ricevuta_server="NEAR"+pktid+ipp2p+adattaStringa(5, str(pp2p))+adattaStringa(2,str(ttl))
                                    sock.send(stringa_ricevuta_server.encode())
                                    #chiudere socket????? sock.cloese()
                                i = i+1
                            stringa_risposta="ANEA"+pktid+host+adattaStringa(5,str(porta))
                            print("\t\t\t\t\t\t\t\t\trispondo con "+stringa_risposta)
                            
                            sockr = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                            sockr.connect((ipp2p, int(pp2p)) )
                            sockr.send(stringa_risposta.encode())
                            sockr.close()
                            
                    finally:
                        conn_db.esegui_commit()
                        conn_db.chiudi_connessione()
        #fine operazione NEAR
        
        #operazione ANEA
                if operazione.upper()=="ANEA":
                    pktid=stringa_ricevuta_server[4:20]
                    ipp2p=stringa_ricevuta_server[20:59]
                    pp2p=stringa_ricevuta_server[59:64]
                    print ("\t\t\t\t\t\t\t\t\tOperazione Anea pktid: "+pktid+" ip: "+ ipp2p +" porta: " +pp2p)
                    #inserisco su db il vicino con ipp2p e porta
                    
                    try:
                        conn_db=Connessione.Connessione()
                        vicino=NearService.NearService.insertNewNear(conn_db.crea_cursore(), ipp2p,pp2p)
                    except:
                        print("\t\t\t\t\t\t\t\t\tInserimento di vicino non effettuato")
                    finally:
                        conn_db.esegui_commit()
                        conn_db.chiudi_connessione()
        #fine operazione ANEA
        
        #operazione QUER
                if operazione.upper()=="QUER":
                    pktid=stringa_ricevuta_server[4:20]
                    ipp2p=stringa_ricevuta_server[20:59]
                    pp2p=stringa_ricevuta_server[59:64]
                    ttl=stringa_ricevuta_server[64:66]
                    ricerca=elimina_spazi_iniziali_finali(stringa_ricevuta_srever[66:86])
                    ttl=int(ttl)-1
                    conn_db=Connessione.Connessione()
                    try:
                        pkt=PacketService.PacketService.getPacket(conn_db.crea_cursore(), pktid)
                    except:
                        if(ttl>=0):
                            conn_db=Connessione.Connessione()
                            files= []
                            files = FileService.FileService.getFiles(conn_db.crea_cursore(),ricerca)
                            i=0
                            while i < len(files):
                                print ("\t\t\t\t\t\t\t\t\tinoltro file al richiedente****" +" "+files[i].filemd5 + " "+files[i].filename)

                                stringa_risposta="AQUE"+pktid+host+adattaStringa(5, str(porta))+files[i].filemd5+files[i].filename
                                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                                sock.connect((ipp2p, int(pp2p)) )
                                sock.send(stringa_risposta) #attenzione enconde
                                sock.close()

                            conn_db.esegui_commit()
                            conn_db.chiudi_connessione()


                            vicini= []
                            vicini = NearService.NearService.getNears(conn_db.crea_cursore())
                            i=0
                            while i < len(vicini):
                                if(vicini[i].ipp2p!=ipp2p and vicini[i].pp2p!=pp2p):
                                    print ("\t\t\t\t\t\t\t\t\tinoltro QUER a vicini****" +" "+vicini[i].pp2p + " "+vicini[i].ipp2p)
                                    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                                    sock.connect((vicini[i].ipp2p, int(vicini[i].pp2p)) )
                                    stringa_ricevuta_server="QUER"+pktid+ipp2p+adattaStringa(5, str(pp2p))+adattaStringa(2,str(ttl))
                                    sock.send(stringa_ricevuta_server.encode())
                                    #chiudere socket????? sock.cloese()
                                i = i+1
                    finally:
                        conn_db.esegui_commit()
                        conn_db.chiudi_connessione()
                        
        
        #fine operazione QUER
        
        
        #operazione AQUE
                if operazione.upper()=="AQUE":
                    print("")
        
        
        
        
        #fine operazione AQUE
         
        

            except Exception as e: 
                print e
                print("\t\t\t\t\t\t\t\t\tErrore ricezione lato server")
            finally:
                client.close() 
                stringa_ricevuta_server=""
                os._exit(0) 
                
        else:
            client.close()
    
    print("Terminato parte server")
            
