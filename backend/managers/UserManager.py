# from fastapi.websockets import WebSocket, WebSocketDisconnect
# from .RoomManager import RoomManager

# GLOBAL_ROOM_ID = 0
# class User:
#     websocket: WebSocket
#     name: str

# class UserManager:
#     def __init__(self) -> None:
#         self.users = []
#         self.queue = []
#         self.roomManager = RoomManager()

#     def addUser(self, name: str, websocket: WebSocket):
#         self.users.append(User(name, websocket))
#         self.queue.append(name)
#         self.clearQueue()
#         self.initHandlers(websocket)

#     def removeUser(self, name: str):
#         self.users = [user for user in self.users if user.name != name]
    
#     def clearQueue(self):
#         if (len(self.queue) < 2):
#             return
#         user1 = self.users[self.users.name == self.queue.pop()]
#         user2 = self.users[self.users.name == self.queue.pop()]

#         if (user1 is None or user2 is None):
#             return
        
#         room = self.roomManager.createRoom(user1, user2)
#         self.clearQueue()
    
#     async def initHandlers(self, websocket: WebSocket):
#         await websocket.accept()
#         try:
#             while True:
#                 data = await websocket.receive_json()
#                 event = data.get("event")
#                 if event == "offer":
#                     await self.room_manager.handle_offer(room_id, data["sdp"], user_id)
#         except WebSocketDisconnect:
#             self.room_manager.removeUser(room_id, user_id)
#             await room_manager.notify_users_in_room(room_id, {"event": "user-disconnected", "userId": user_id})

        

       



