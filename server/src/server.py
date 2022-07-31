#!/usr/bin/env python

import asyncio
import json
import uuid

import websockets


class EventHandler:
    def __init__(self):
        self.current_room = []
        self.waiting_sockets = []
        self.active_rooms: dict[int, dict[str, int]] = {}  # Maps room UID to players.
        self.active_players: dict[
            int, int
        ] = {}  # Maps UID to room. Uses 0 if active in no room

    async def authenticate(self, uid, socket):
        self.active_players[uid] = 0
        await socket.send(json.dumps({"authenticate": True}))

    async def searching(self, uid, socket):
        self.current_room.append(uid)
        self.waiting_sockets.append(socket)
        if len(self.current_room) == 2:
            room_uid = uuid.uuid1().int >> 64
            self.active_rooms[room_uid] = {
                i: {
                    "position x": 0,
                    "position y": 0,
                    "is_dead": False,
                    "animation_state": "idle",
                    "is_done": False
                }
                for i in self.current_room
            }
            for waiting_socket in self.waiting_sockets:
                await waiting_socket.send(json.dumps({"matches": room_uid}))
            for uid in self.current_room:
                self.active_players[uid] = room_uid
            self.current_room = []
            self.waiting_sockets = []

    async def set_data(
        self, uid, position1, position2, is_dead, animation_state, socket
    ):
        room = self.active_players[uid]
        self.active_rooms[room][uid]["position x"] = position1
        self.active_rooms[room][uid]["position y"] = position2
        self.active_rooms[room][uid]["is_dead"] = is_dead
        self.active_rooms[room][uid]["animation_state"] = animation_state
        other_positions = []
        for other_uids in self.active_rooms[room]:
            if other_uids != uid:
                other_positions.append(
                    tuple(self.active_rooms[room][other_uids].values())
                )
        await socket.send(json.dumps({"data": other_positions}))

    async def leave_room(self, uid, socket):
        room = self.active_players[uid]
        self.active_rooms[room][uid]["is_done"] = True
        self.active_players[uid] = 0
        if all(self.active_players[i] == 0 for i in self.active_rooms[room]):
            del self.active_rooms[room]
        await socket.send(json.dumps({"left": True}))


event_handler = EventHandler()


async def handle_request(request: str, websocket):
    req = json.loads(request)
    match req:
        case {"authenticate": UID}:
            await event_handler.authenticate(UID, websocket)
        case {"id": UID, "searching": True}:
            await event_handler.searching(UID, websocket)
        case {"id": UID, "data": [position1, position2, is_dead, animation_state]}:
            await event_handler.set_data(
                UID, position1, position2, is_dead, animation_state, websocket
            )
        case {"id": UID, "leave": True}:
            await event_handler.leave_room(UID, websocket)


async def start(websocket):
    async for message in websocket:
        await handle_request(message, websocket)


async def main():
    async with websockets.serve(start, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())
