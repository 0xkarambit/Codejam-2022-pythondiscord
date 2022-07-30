#!/usr/bin/env python

import json
import uuid
from os.path import exists
from typing import Callable, List, Union

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


async def update_data(
    websocket, data: List[Union[int, int, bool, str]], call_when_done: Callable
):  # data is in the form (position x, position y, is_dead, animation_state)
    await websocket.send(json.dumps({"id": uid, "data": data}))
    response = await websocket.recv()
    positions = json.loads(response).get("data")
    if isinstance(positions, list):
        call_when_done(positions)


async def leave(websocket, call_when_done: Callable):
    await websocket.send(json.dumps({"id": uid, "leave": True}))
    response = await websocket.recv()
    done = json.loads(response).get("left")
    if isinstance(done, bool) and done:
        call_when_done()
