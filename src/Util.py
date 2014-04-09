import hashlib

class Util:
    
    global HOST
<<<<<<< HEAD
    HOST = "fd00:0000:0000:0000:ac39:bcc5:55fd:c66e"
    global PORT
    PORT = 3333
=======
    HOST = "fd00:0000:0000:0000:6860:dec1:27e9:6403"#1dd3:234b:b49a:d734"
    global PORT
    PORT = 3332
>>>>>>> e70d3eb37057dbf05c5cb69af9faa3ac2cd9adff
    
    global USERNAME
    USERNAME = "p2pAdmin"
    global PASSWORD
<<<<<<< HEAD
    PASSWORD = "p2pAdmin"
=======
    PASSWORD = "lorenzo91"
>>>>>>> e70d3eb37057dbf05c5cb69af9faa3ac2cd9adff
    
    global TTL
    TTL = 3
    
    global MAX_NEARS
    MAX_NEARS = 2
    
    global LOCAL_PATH #percorso file condivisi
    LOCAL_PATH = "/home/lorenzo/Desktop/gnutella/src/FileCondivisi/"
    
    @staticmethod
    def adattaStringa(lunghezzaFinale, stringa):
        
        ritorno = stringa
        for i in range(len(stringa), lunghezzaFinale):
            ritorno = "0" + ritorno
        return ritorno
    
    @staticmethod
    def md5(filename):
        
        md5 = hashlib.md5()
        file = open(filename, "rb")
        while True:
           data = file.read(1024)
           md5.update(data)
           
           if len(data) < 1024:
               break
           
        return md5.digest() 
    
    @staticmethod
    def riempi_stringa(stringa,lunghezza):
        return Util.aggiungi_asterischi_finali(stringa,lunghezza)
        #return Util.aggiungi_spazi_finali(stringa,lunghezza)
    
    @staticmethod
    def aggiungi_spazi_finali(stringa, lunghezza):
        
        i = len(stringa)
        while i < lunghezza:
            stringa = stringa + ' '
            i = i + 1
        return stringa
    
    @staticmethod
    def aggiungi_asterischi_finali(stringa, lunghezza):
        
        i = len(stringa)
        while i < lunghezza:
            stringa = stringa + '*'
            i = i + 1
        return stringa
    
    @staticmethod
    def elimina_spazi_iniziali_finali(stringa):
        
        ritorno = ""
        ritorno2 = ""
        lettera = False
        lettera2 = False
        for i in range (0, len(stringa)):
            if(stringa[i] != " " or lettera == True):
                ritorno = ritorno + stringa[i]
                lettera = True
       
        ritorno = ritorno[::-1]
    
        for i in range (0,len(ritorno)):
            if(ritorno[i]!=" " or lettera2==True):
                ritorno2=ritorno2+ritorno[i]
                lettera2 = True
    
        return ritorno2[::-1]
    
    @staticmethod
    def elimina_asterischi_iniziali_finali(stringa):
        
        ritorno = ""
        ritorno2 = ""
        lettera = False
        lettera2 = False
        for i in range (0, len(stringa)):
            if(stringa[i] != "*" or lettera == True):
                ritorno = ritorno + stringa[i]
                lettera = True
       
        ritorno = ritorno[::-1]
    
        for i in range (0,len(ritorno)):
            if(ritorno[i]!="*" or lettera2==True):
                ritorno2=ritorno2+ritorno[i]
                lettera2 = True
    
        return ritorno2[::-1]
    
    @staticmethod
    def get_md5(filename):
        md5 = hashlib.md5()
        with open(filename,"rb") as f:
            while True:
                data = f.read(1024)
                md5.update(data)
                if len(data) < 1024:
                    break
        md5_res = md5.digest()
        return md5_res
    
    
