import Packet

class PacketService:
    global EXPIREDTIME 
    EXPIREDTIME = 300
    
    @staticmethod
    def insertNewPacket(database, packetid):
        packet = Packet.Packet(packetid, None)
        packet.insert(database)
        return packet
    
    @staticmethod
    def getPacket(database, packetid):
        database.execute("""SELECT packetid, created_at
                            FROM packet
                            WHERE packetid = %s""",
                            packetid)
        packetid, created_at = database.fetchone()
        packet = Packet.Packet(packetid, created_at)
        return packet
    
    @staticmethod
    def deleteExpiredPacket(database):
        database.execute("""DELETE FROM packet
                            WHERE UNIX_TIMESTAMP() - UNIX_TIMESTAMP(created_at) > %s""",
                            (EXPIREDTIME))