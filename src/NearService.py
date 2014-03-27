import Near

class NearService:
    
    @staticmethod
    def insertNewNear(database, ipp2p, pp2p):
        near = Near.Near(None, ipp2p, pp2p)
        near.insert(database)
        return near
    
    @staticmethod
    def getNears(database, packetid):
        
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
        count = database.fetchone()
        return count