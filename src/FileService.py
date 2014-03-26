import File

class FileService:
    
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