class SearchResult:
    
    def __init__(self, ipp2p,pp2p,filemd5,filename):
        self.filename = filename
        self.filemd5 = filemd5
        self.ipp2p = ipp2p
        self.pp2p = pp2p
        
        
    def insert(self, database):

    

        database.execute("""INSERT INTO searchresult
                            (ipp2p, pp2p, filemd5, filename)
                            VALUES (%s, %s, %s, %s)""",
                            (self.ipp2p, self.pp2p, self.filemd5, self.filename))
    
#    def update(self, database):
#        pass
    
    def delete(self, database):
        database.execute("""DELETE FROM searchresult""")