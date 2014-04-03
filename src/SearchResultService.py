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
    
