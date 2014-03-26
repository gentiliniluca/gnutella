import string
import random

class Packet:
    
    def __init__(self, packetid, created_at):
        self.packetid = packetid
        self.created_at = created_at
    
    def insert(self, database):
        
        self.packetid = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        
        database.execute("""INSERT INTO packet
                            (packetid)
                            VALUES (%s)""",
                            (self.packetid))
    
#    def update(self, database):
#        pass
    
    def delete(self, database):
        database.execute("""DELETE FROM packet
                            WHERE packetid = %s""",
                            (self.packetid))