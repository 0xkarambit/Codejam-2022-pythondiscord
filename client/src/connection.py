#!/usr/bin/env python

import json
import uuid
from os.path import exists
from typing import Callable, Tuple

uid = None

if exists("uid_details.txt"):
    with open("uid_details.txt", "r") as file:
        uid = int(file.read().strip())
else:
    uid = uuid.uuid1().int >> 64
    with open("uid_details.txt", "w") as file:
        file.write(str(uid))


async def authenticate(websocket):
    await websocket.send(json.dumps({"authenticate": uid}))
    response = await websocket.recv()
    if json.loads(response) == {"authenticate": True}:
        print("Authenticated")
    else:
        print("Failed to authenticate")


async def searching(websocket, call_when_done: Callable):
    await websocket.send(json.dumps({"id": uid, "searching": True}))
    response = await websocket.recv()
    match = json.loads(response).get("matches")
    if isinstance(match, int):
        print("Match found")
        call_when_done(match)


async def update_position(
    websocket, data: Tuple[int, int, int], call_when_done: Callable
):  # data is in the form (position x, position y, lives)
    await websocket.send(json.dumps({"id": uid, "position": data}))
    response = await websocket.recv()
    positions = json.loads(response).get("positions")
    if isinstance(positions, list):
        call_when_done(positions)


async def dead(websocket, call_when_done: Callable):
    await websocket.send(json.dumps({"id": uid, "dead": True}))
    response = await websocket.recv()
    lives = json.loads(response).get("lives")
    if isinstance(lives, int):
        call_when_done(lives)


async def completed(websocket, call_when_done: Callable):
    await websocket.send(json.dumps({"id": uid, "completed": True}))
    response = await websocket.recv()
    rank = json.loads(response).get("rank")
    if isinstance(rank, int):
        call_when_done(rank)


async def lost(websocket, call_when_done: Callable):
    await websocket.send(json.dumps({"id": uid, "lost": True}))
    response = await websocket.recv()
    rank = json.loads(response).get("rank")
    if isinstance(rank, int):
        call_when_done(rank)


async def leave(websocket, call_when_done: Callable):
    await websocket.send(json.dumps({"id": uid, "leave": True}))
    response = await websocket.recv()
    done = json.loads(response).get("left")
    if isinstance(done, bool) and done:
        call_when_done()
