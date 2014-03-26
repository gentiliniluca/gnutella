class File:
    def __init__(self, fileid, filemd5, filename):
        self.fileid = fileid
        self.filemd5 = filemd5
        self.filename = filename
    
    def insert(self, database):
        
        database.execute("""INSERT INTO file
                            (filemd5, filename)
                            VALUES (%s, %s)""",
                            (self.filemd5, self.filename))
    
    def update(self, database):
        
        database.execute("""UPDATE file
                            SET filename = %s, filemd5 = %s
                            WHERE fileid = %s""",
                            (self.filename, self.filemd5, self.fileid))
    
    def delete(self, database):
        
        database.execute("""DELETE FROM file
                            WHERE fileid = %s""",
                            (self.fileid))
