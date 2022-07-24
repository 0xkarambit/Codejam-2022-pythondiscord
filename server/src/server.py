#!/usr/bin/env python

import asyncio
import json
import uuid

import websockets


class EventHandler:
    def __init__(self):
        self.current_room = []
        self.waiting_sockets = []
        self.active_rooms: dict[int, dict[int, int]] = {}  # Maps room UID to players.
        self.active_players: dict[
            int, int
        ] = {}  # Maps UID to room. Uses 0 if active in no room

    async def authenticate(self, uid, socket):
        self.active_players[uid] = 0
        await socket.send(json.dumps({"authenticate": True}))

    async def searching(self, uid, socket):
        self.current_room.append(uid)
        self.waiting_sockets.append(socket)
        if len(self.current_room) == 4:
            room_uid = uuid.uuid1().int >> 64
            self.active_rooms[room_uid] = {i: 0 for i in self.current_room}
            for waiting_socket in self.waiting_sockets:
                await waiting_socket.send(json.dumps({"matches": room_uid}))
            for uid in self.current_room:
                self.active_players[uid] = room_uid
            self.current_room = []
            self.waiting_sockets = []

    async def set_position(self, uid, position, socket):
        room = self.active_players[uid]
        self.active_rooms[room][uid] = position
        other_positions = []
        for other_uids in self.active_rooms[room]:
            if other_uids != uid:
                other_positions.append(self.active_rooms[room][other_uids])
        await socket.send(json.dumps({"positions": other_positions}))


event_handler = EventHandler()


async def handle_request(request: str, websocket):
    req = json.loads(request)
    match req:
        case {"authenticate": UID}:
            await event_handler.authenticate(UID, websocket)
        case {"id": UID, "searching": True}:
            await event_handler.searching(UID, websocket)
        case {"id": UID, "position": position}:
            await event_handler.set_position(UID, position, websocket)


async def echo(websocket):
    async for message in websocket:
        await handle_request(message, websocket)


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())
