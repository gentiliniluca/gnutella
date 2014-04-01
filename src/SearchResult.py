class SearchResult:
    
    def __init__(self, filename, filemd5, ipp2p, pp2p):
        self.filename = filename
        self.filemd5 = filemd5
        self.ipp2p = ipp2p
        self.pp2p = pp2p
        
        
    def insert(self, database):

        self.packetid = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

        database.execute("""INSERT INTO searchresult
                            (ipp2, pp2p, filemd5, filename)
                            VALUES (%s, %s, %s, %s)""",
                            (self.ipp2p, self.pp2p, self.filemd5, self.filename))
    
#    def update(self, database):
#        pass
    
    def delete(self, database):
        database.execute("""DELETE FROM packet
                            WHERE filemd5 = %s""",
                            (self.filemad5))