from config import prefix
from src.vars import Varlist
from src.commands_list import aliases, allCommands, allCommands_keys

from showdown.utils import name_to_id

class Control():
    def __init__(self) -> None:
        self.msgSplited = Varlist.msgSplited
        self.content = ""
        self.msgType = ""
        self.commandParams = []
        self.room = ""

    def determinate_pm_or_room(self):
        if len(self.msgSplited) > 4:
            if self.msgSplited[1] == "pm":
                sender = self.msgSplited[2][1:]
                senderID = name_to_id(sender)
                self.content = self.msgSplited[4]
                self.msgType = "pm"
            elif self.msgSplited[1] == "c:":
                sender = self.msgSplited[3][1:]
                senderID = name_to_id(sender)
                self.content = self.msgSplited[4]
                self.msgType = "room"
            else:
                return
        else:
            return

        Varlist.sender = sender
        Varlist.senderID = senderID
        Varlist.content = self.content
        Varlist.msgType = self.msgType

        is_command = self.determinate_is_a_command()
        if not is_command:
            is_invite = self.determinate_is_a_invite()
            if not is_invite:
                return
            else:
                return is_invite
        else:
            return is_command

    def determinate_is_a_command(self):
        if self.content[0] == prefix:
            command = name_to_id(self.content.split(" ")[0].strip()[1:])
            self.commandParams = self.content.replace(f"{prefix}{command}", "").strip().split(",")
            self.commandParams = [param.strip() for param in self.commandParams]
        else:
            return

        if command in aliases:
            command = aliases[command]

        if command in allCommands_keys:
            Varlist.command = command
            Varlist.commandParams = self.commandParams
        else:
            return
        
        need_room = allCommands[command]['need_room']
        
        if need_room:
            self.identify_room()

        return "COMMAND"
    
    def identify_room(self):
        if self.msgType == "room":
            self.room = self.msgSplited[0].strip()
            if not self.room:
                self.room = "lobby"
            else:
                self.room = self.room[1:]

        elif self.msgType == "pm":
            self.room = name_to_id(self.commandParams[0])
        
        Varlist.room = self.room
    
    def determinate_is_a_invite(self):
        invite = self.content.split(" ")

        if invite[0] == "/invite":
            return "INVITE"
        else:
            return