import SearchResult

class SearchResultService:
    global EXPIREDTIME 
    EXPIREDTIME = 300
    
    @staticmethod
    def insertNewSearchResult(database,ipp2p,pp2p,filemd5,filename):
        sr = SearchResult.SearchResult(ipp2p,pp2p,filemd5,filename)
        sr.insert(database)
        return sr
    
   
    
    
    @staticmethod
    def delete( database):
        database.execute("""DELETE FROM searchresult""")
    
