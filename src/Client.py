import Util 
import SearchResult
import SearchResultService

class Client:
    
    @staticmethod
    def visualizza_menu_principale():
        
        print("\n************************\n*  1 - Ricerca File    *\n*  2 - Ricerca vicini  *\n*  3 - Carica File     *\n*  4 - Download File   *\n*  0 - Fine            *\n************************")
        out=raw_input("\n\tOperazione scelta: ")
        if(int(out) >= 0 and int(out) <= 4):
            break
        print("Valore inserito errato! (valore compreso tra 0 e 4)")
        return out
    
    @staticmethod
    def nearHandler():
        
        conn_db = Connessione.Connessione()
        pkt = PacketService.PacketService.insertNewPacket(conn_db.crea_cursore())
        conn_db.esegui_commit()
        conn_db.chiudi_connessione()
        
        ttl = TTL
        
        stringa_da_trasmettere = "NEAR" + pkt.packetid + host + "" + Util.Util.adattaStringa(5, str(porta)) + Util.Util.adattaStringa(2, str(ttl)) 
        #print("valore inviato: "+stringa_da_trasmettere)
        
        #lettura vicini da db
        conn_db = Connessione.Connessione()
        vicini = []
        vicini = NearService.NearService.getNears(conn_db.crea_cursore())
        
        i = 0
        while i < len(vicini):
            #print("****" +" "+vicini[i].pp2p + " "+vicini[i].ipp2p)
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.connect((vicini[i].ipp2p, int(vicini[i].pp2p)))
            sock.send(stringa_da_trasmettere.encode())
            i = i + 1
            
        conn_db.esegui_commit()
        conn_db.chiudi_connessione()
        
    @staticmethod
    def downloadHandler(searchResults):
        
        i = 0
        while i < len(searchResults):
            print(i + 1+".\t"+searchResults[i].filename+"\t"+searchResults[i].ipp2p+"\t"+searchResults[i].pp2p)
            i = i + 1
        
        #il valore di choice è incrementato di uno
        choice = raw_input("Scegliere il numero del peer da cui scaricare") 
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.connect((searchResults[choice - 1].ipp2p, int(searchResults[choice - 1].pp2p)))
        sendingString = "RETR"+searchResults[choice - 1].filemd5
        sock.send(sendingString.encode())
        
        receivedString = sock.recv(10)
        if receivedString[0:4].decode() == "ARET":
            nChunk = int(receivedString[4:9].decode())
            chunk = bytes()
            chunkCounter = 0
            
            file = open(searchResults[choice - 1].filename, "wb")
            
            while chunkCounter < nChunk:
                receivedString = sock.recv(1024)
                chunk = chunk + receivedString
                
                while True:
                    if len(chunk[:5]) >=  5:
                        chunkLength = int(chunk[:5])
                    else:
                        break
                    
                    if len(chunk[5:]) >= chunkLength:
                        data = chunk[5:5 + chunkLength]
                        file.write(data)
                        chunkCounter = chunkCounter + 1
                        chunk = chunk[5 + chunkLength:]
                    else:
                        break
        
        sock.close() 
        
        #controllo correttezza del download
        myMd5 = Util.Util.md5(searchResults[choice - 1].filename)        
        if myMd5 != searchResults[choice - 1].filemd5:
            print("Errore nel download del file")  
            
    @staticmethod
    def serachHandler():
        while True:
            query_ricerca = raw_input("\n\tInserire la stringa di ricerca (massimo 20 caratteri): ")
            if(len(query_ricerca) <= 20):
                break
            print("\n\tErrore lunghezza query maggiore di 20!")
                
            query_ricerca = Util.Util.aggiungi_spazi_finali(query_ricerca)
            #print(query_ricerca)                
                
            #pulisco la tabella searchresult, questa operazione va fatta prima di ogni ricerca
            conn_db = Connessione.Connessione()
            SearchResultService.SearchResultService.delete(conn_db.crea_cursore())
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()            
            
            conn_db = Connessione.Connessione()
            pkt = PacketService.PacketService.insertNewPacket(conn_db.crea_cursore())
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
            ttl = TTL 
            stringa_da_trasmettere = "QUER" + pkt.packetid + host + "" + adattaStringa(5,str(porta)) + adattaStringa(2,str(ttl)) + query_ricerca
            
            #print("stringa inviata dal client: "+stringa_da_trasmettere)
            
            conn_db = Connessione.Connessione()
            vicini = []
            vicini = NearService.NearService.getNears(conn_db.crea_cursore())
            i = 0
            while i < len(vicini):
                #print ("****" +" "+vicini[i].pp2p + " "+vicini[i].ipp2p)
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                sock.connect((vicini[i].ipp2p, int(vicini[i].pp2p)) )
                sock.send(stringa_da_trasmettere.encode())
                i = i + 1
                
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
            
    @staticmethod
    def addFile():
        conn_db = Connessione.Connessione()
        nomefile = raw_input("Inserire il nome del file: " + LOCAL_PATH)
        nomefile = LOCAL_PATH + nomefile
        filemd5 = Util.Util.get_md5(nomefile)
        print("md5: " + filemd5 + " nome: " + nomefile)
        nomefile = aggiungi_spazi_finali(nomefile,100)
        
        file = FileService.FileService.insertNewFile(conn_db.crea_cursore(), filemd5, nomefile)
        
        conn_db.esegui_commit()
        conn_db.chiudi_connessione()
            