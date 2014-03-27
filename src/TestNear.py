import NearService
import Near
import Connessione

c = Connessione.Connessione()
database = c.crea_cursore()

# Il metodo statico insertNewNears lancia l'eccezione DBException per evitare 
# l'inserimento di un numero di vicini superiore a 3
try:
    NearService.NearService.insertNewNear(database, "6", "30000")
except Exception, e:
    print "Exception:", e.message

c.esegui_commit()