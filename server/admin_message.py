import random
import v
import datetime


def get_time():
    nu = datetime.datetime.now()
    datum = nu.strftime("%d %B %Y")
    tijd = nu.strftime("%H:%M")
    return datum, tijd


v.get()


class admin_message():
    def __init__(self, name, start_message, owner, sort):
        self.marked_by = []
        self.sort = sort
        self.read = []
        list = []
        for a in v.admin_messages:
            list.append(a.id)
        self.id = random.randint(0, 100000000)
        while self.id in list:
            self.id = random.randint(0, 100000000)
        self.name = name
        self.messages = []
        self.owner = owner
        self.add_message(self.owner, start_message)
        self.tijd, self.datum = get_time()
        self.create_time = self.tijd+" "+self.datum

    def save(self):
        data = {
            "marked_by": self.marked_by,
            "sort": self.sort,
            "name": self.name,
            "messages": self.messages,
            "owner": self.owner,
            "read": self.read,
            "create_time": self.create_time
        }
        return data

    def load(self, data):
        self.name = data["name"]
        self.owner = data["owner"]
        self.marked_by = data["marked_by"]
        self.sort = data["sort"]
        self.messages = data["messages"]
        self.read = data["read"]
        self.create_time = data["create_time"]

    def send(self, message):
        for c in v.clients:
            if c.data["name"] == self.owner or c.data["admin"] == 1 or c.data["moderator"] == 1:
                c.send(message)

    def play_sound(self, soundname, who):
        for c in v.clients:
            if who == "admin" and c.data["admin"] == 1 or c.data["moderator"] == 1 and who == "admin":
                c.send("play_sound staffmsgstaff"+soundname+".ogg 0 0 0 1 0")
            elif c.data["name"] == self.owner and who == "owner":
                c.send("play_sound staffmsgplayer"+soundname+".ogg 0 0 0 1 0")
#   else:
#    c.send("play_sound staffmsg"+soundname+".ogg 0 0 0 1 0")

    def add_message(self, name, text):
        tijd, datum = get_time()
        self.messages.append(name+": "+text+": Sent on "+tijd+" "+datum)


def get_admin_messages_index(id):
    for p in v.admin_messages:
        if p.id == id:
            return v.admin_messages.index(p)


def select_admin_messages(sort, player_name):
    final = []
    for a in v.admin_messages:
        if sort != "" and a.sort != sort:
            continue
        if player_name != "" and a.owner != player_name:
            continue
        final.append(a)
    return final
