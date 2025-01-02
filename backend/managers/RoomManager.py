# GLOBAL_ROOM_ID = 1

# class RoomManager:
#     def __init__(self):
#         self.rooms = {}

#     def generate(self):
#         return GLOBAL_ROOM_ID + 1
    
#     def createRoom(self, user1, user2):
#         roomId = self.generate()
#         self.rooms.set(str(roomId), {user1, user2})

#         user1.websocket.send_json({"event": "send-offer", "room": roomId})

#     def onOffer(self, roomId: str, sdp: str):
#         user2 = self.rooms.get(roomId)["user2"]
#         user2.websocket.send_json({"event": "offer", "sdp": sdp})

#     def onAnswer(self, roomId: str, sdp: str):
#         user1 = self.rooms.get(roomId)["user1"]
#         user1.websocket.send_json({"event": "offer", "sdp": sdp})

