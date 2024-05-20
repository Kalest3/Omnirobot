import asyncio

from src.vars import Varlist

websocket = Varlist.websocket

def call_command(command):
    try:
        asyncio.get_event_loop().is_running()
    except RuntimeError:
        return asyncio.run(command)
    return asyncio.gather(command)

def respondRoom(message, room):
    try:
        asyncio.get_event_loop().is_running()
    except RuntimeError:
        return asyncio.run(websocket.send(f"{room}|{message}"))
    return asyncio.gather(websocket.send(f"{room}|{message}"))

def respondPM(user, message):
    try:
        asyncio.get_event_loop().is_running()
    except RuntimeError:
        return asyncio.run(websocket.send(f"|/pm {user}, {message}"))
    return asyncio.gather(websocket.send(f"|/pm {user}, {message}"))

def respond(msgType, message, user=None, room=None):
    if msgType == "pm":
        respondPM(user, message, websocket)
    elif msgType == "room":
        respondRoom(message, websocket, room)