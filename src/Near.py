class Near:
    def __init__(self, nearid, ipp2p, pp2p):
        self.nearid = nearid
        self.ipp2p = ipp2p
        self.pp2p = pp2p
    
    def insert(self, database):
        
        database.execute("""INSERT INTO near
                            (ipp2p, pp2p)
                            VALUES (%s, %s)""",
                            (self.ipp2p, self.pp2p))
    
#    def update(self, database):
#        
#        database.execute("""UPDATE near
#                            SET ipp2p = %s, pp2p = %s
#                            WHERE nearid = %s""",
#                            (self.ipp2p, self.pp2p, self.nearid))
    
    def delete(self, database):
        
        database.execute("""DELETE FROM near
                            WHERE nearid = %s""",
                            (self.nearid))
