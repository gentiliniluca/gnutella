import Near
import DBException

class NearService:
    
    global MAXNEARS 
    MAXNEARS = 3
    
    @staticmethod
    def insertNewNear(database, ipp2p, pp2p):
        
        try:
            near = NearService.getNear(database, ipp2p, pp2p)
        except:            
            if NearService.getNearsCount(database) < MAXNEARS:
                near = Near.Near(None, ipp2p, pp2p)
                near.insert(database)
            else:
                raise DBException.DBException("Max nears number reached!")        
        return near
    
    @staticmethod
    def getNear(database, ipp2p, pp2p):
        
        database.execute("""SELECT nearid, ipp2p, pp2p
                            FROM near
                            WHERE ipp2p = %s AND pp2p = %s""",
                            (ipp2p, pp2p))
        
        nearid, ipp2p, pp2p = database.fetchone()
        
        near = Near.Near(nearid, ipp2p, pp2p)
        
        return near
    
    @staticmethod
    def getNears(database):
        
        database.execute("""SELECT nearid, ipp2p, pp2p
                            FROM near""")
        
        nears = []
        
        try:
            while True:
                nearid, ipp2p, pp2p = database.fetchone()
                near = Near.Near(nearid, ipp2p, pp2p)
                nears.append(near)
        except:
            pass
                
        return nears
    
    @staticmethod
    def getNearsCount(database):
        database.execute("""SELECT count(*)
                            FROM near""")
        count, = database.fetchone()
        return count