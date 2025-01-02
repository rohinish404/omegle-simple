from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from dataclasses import dataclass
from typing import Dict, List

version = 'v1'

app = FastAPI(version=version)

origins = [
    "http://localhost:5173",
    "http://localhost:3006",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio = socketio.AsyncServer(cors_allowed_origins=[], async_mode='asgi')
socket_app = socketio.ASGIApp(sio, socketio_path='sockets')
app.mount('/', app=socket_app)


@app.get("/heartbeat")
async def check():
    return {"message": "Hello World"}


@dataclass
class User:
    socket_id: str
    name: str


@dataclass
class Room:
    user1: User
    user2: User


class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.global_room_id = 1

    async def create_room(self, user1: User, user2: User) -> str:
        room_id = str(self.global_room_id)
        self.global_room_id += 1

        self.rooms[room_id] = Room(user1=user1, user2=user2)

        # Notify both users to send offers
        await sio.emit('send-offer', {'roomId': room_id}, room=user1.socket_id)
        await sio.emit('send-offer', {'roomId': room_id}, room=user2.socket_id)

    async def on_offer(self, room_id: str, sdp: str, sender_socket_id: str):
        room = self.rooms.get(room_id)
        if not room:
            return

        receiving_user = room.user2 if room.user1.socket_id == sender_socket_id else room.user1
        await sio.emit('offer', {
            'sdp': sdp,
            'roomId': room_id
        }, room=receiving_user.socket_id)

    async def on_answer(self, room_id: str, sdp: str, sender_socket_id: str):
        room = self.rooms.get(room_id)
        if not room:
            return

        receiving_user = room.user2 if room.user1.socket_id == sender_socket_id else room.user1
        await sio.emit('answer', {
            'sdp': sdp,
            'roomId': room_id
        }, room=receiving_user.socket_id)

    async def on_ice_candidates(self, room_id: str, sender_socket_id: str, candidate: dict, candidate_type: str):
        room = self.rooms.get(room_id)
        if not room:
            return

        receiving_user = room.user2 if room.user1.socket_id == sender_socket_id else room.user1
        await sio.emit('add_ice_candidate', {
            'candidate': candidate,
            'type': candidate_type
        }, room=receiving_user.socket_id)


class UserManager:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.queue: List[str] = []
        self.room_manager = RoomManager()

    async def add_user(self, name: str, socket_id: str):
        print(f"name - {name}")
        user = User(socket_id=socket_id, name=name)
        self.users[socket_id] = user
        self.queue.append(socket_id)
        await sio.emit('lobby', room=socket_id)
        await self.clear_queue()
        self.initHandlers(socket_id)

    def remove_user(self, socket_id: str):
        if socket_id in self.users:
            del self.users[socket_id]
        if socket_id in self.queue:
            self.queue.remove(socket_id)

    async def clear_queue(self):
        print("inside clear queues")
        print(f"Queue length: {len(self.queue)}")

        if len(self.queue) < 2:
            return

        id1 = self.queue.pop()
        id2 = self.queue.pop()

        print(f"ids are {id1} {id2}")

        user1 = self.users.get(id1)
        user2 = self.users.get(id2)

        if not user1 or not user2:
            return

        print("creating room")
        await self.room_manager.create_room(user1, user2)

        await self.clear_queue()

    def initHandlers(self, sid):
        @sio.event
        async def offer(sid, data):
            print(f"data - {data}")
            await user_manager.room_manager.on_offer(
                data['roomId'],
                data['sdp'],
                sid
            )

        @sio.event
        async def answer(sid, data):
            await user_manager.room_manager.on_answer(
                data['roomId'],
                data['sdp'],
                sid
            )

        @sio.event
        async def add_ice_candidate(sid, data):
            await user_manager.room_manager.on_ice_candidates(
                data['roomId'],
                sid,
                data['candidate'],
                data['type']
            )



user_manager = UserManager()

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await user_manager.add_user("randomName", sid)


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    user_manager.remove_user(sid)
