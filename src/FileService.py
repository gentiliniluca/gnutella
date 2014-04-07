import File

class FileService:
    
    @staticmethod
    def insertNewFile(database, filemd5, filename):
        
        try:
            file = FileService.getFile(database, filename)
        except:
            file = File.File(None, filemd5, filename)
            file.insert(database)
        
        return file
    
    @staticmethod
    def getFile(database, filename):
        
        database.execute("""SELECT fileid, filemd5, filename
                            FROM file
                            WHERE filename = %s""",
                            (filename))
        
        fileid, filemd5, filename = database.fetchone()
        
        file = File.File(fileid, filemd5, filename)
        
        return file
    
    @staticmethod
    def getFileMD5(database, filemd5):
        
        database.execute("""SELECT fileid, filemd5, filename
                            FROM file
                            WHERE filemd5 = %s""",
                            (filemd5))
        
        fileid, filemd5, filename = database.fetchone()
        
        file = File.File(fileid, filemd5, filename)
        
        return file
    
    @staticmethod
    def getFiles(database, searchString):
        
        searchString = "%" + searchString.upper() + "%"
        
        database.execute("""SELECT fileid, filemd5, filename
                            FROM file
                            WHERE filename LIKE %s""",
                            searchString)
        
        files = []
        
        try:
            while True:
                fileid, filemd5, filename = database.fetchone()
                file = File.File(fileid, filemd5, filename)
                files.append(file)
        except:
            pass
        
        return files