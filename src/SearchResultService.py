import SearchResult
import sys

class SearchResultService:
    global EXPIREDTIME 
    EXPIREDTIME = 300
    
    @staticmethod
    def insertNewSearchResult(database,ipp2p,pp2p,filemd5,filename):
        
        try:
            sr = SearchResultService.getSearchResult(database, ipp2p, pp2p, filemd5, filename)
        
        except:
            sr = SearchResult.SearchResult(ipp2p,pp2p,filemd5,filename)
            sr.insert(database)
        
        return sr
    
    @staticmethod
    def getSearchResult(database, ipp2p, pp2p, filemd5, filename):
        
        database.execute("""SELECT ipp2p, pp2p, filemd5, filename
                            FROM searchresult
                            WHERE ipp2p = %s AND pp2p = %s AND filemd5 = %s AND filename = %s""",
                            (ipp2p, pp2p, filemd5, filename))
        
        ipp2p, pp2p, filemd5, filename = database.fetchone()
        
        searchResult = SearchResult.SearchResult(ipp2p, pp2p, filemd5, filename)
        
        return searchResult
    
    @staticmethod
    def getSearchResults(database):
        database.execute("""SELECT ipp2p, pp2p, filemd5, filename
                            FROM searchresult""")
       
        searchResults = []
        try:
            while True:
                ipp2p, pp2p, filemd5, filename = database.fetchone()
                searchResult = SearchResult.SearchResult(ipp2p, pp2p, filemd5, filename)
                searchResults.append(searchResult)
               
        except:
            pass
        
        return searchResults
    
    @staticmethod
    def delete( database):
        database.execute("""DELETE FROM searchresult""")
