import json
import requests
import logging

from src.commands_list import commands_dp, commands_mq
from src.vars import Varlist
from src.control_pm_and_room import Control
from src.sending import call_command
from config import username, password, rooms, avatar

from src.minigames.megaquiz.redirecting import RedirectingFunction as mq_redirect

logging.basicConfig(
        format="%(asctime)s %(message)s",
        level=logging.DEBUG,
)

class User():
    def __init__(self) -> None:
        self.websocket = Varlist.websocket
        self.splitMsg = ""
        self.loginDone = False
        self.control_pm_room = None

    async def login(self):
        while True:
            msg = await self.websocket.recv()
            splitMsg = str(msg).split("|")
            self.splitMsg = splitMsg
            Varlist.msgSplited = splitMsg
            if len(splitMsg) > 1:
                if splitMsg[1] == "challstr":
                    challstrStart = str(msg).find("4")
                    challstr = msg[challstrStart:]
                    postlogin = requests.post("https://play.pokemonshowdown.com/~~showdown/action.php", data={'act':'login','name':username,'pass':password,'challstr':challstr})
                    assertion = json.loads(postlogin.text[1:])["assertion"]
                    call_command(self.websocket.send(f"|/trn {username},0,{assertion}"))
                    call_command(self.websocket.send(f"|/avatar {avatar}"))

                    for room in rooms:
                        await self.websocket.send(f"|/join {room}")

                    self.loginDone = True

            if self.loginDone:
                await self.afterLogin()
                

    async def afterLogin(self):
        self.control_pm_room = Control()
        is_command = self.control_pm_room.determinate_pm_or_room()
        if is_command:
            command = Varlist.command
            if command in commands_mq:
                await mq_redirect().redirect_to_function()
            elif command in commands_dp:
                pass