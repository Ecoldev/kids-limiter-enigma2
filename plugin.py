from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Components.ServiceEventTracker import ServiceEventTracker
from enigma import eTimer, iPlayableService, eServiceReference
import re
import json
import os
from datetime import datetime


LIMIT = 1200   # 20 min
SAVE_FILE = "/etc/enigma2/kids_time.json"

#TVP1 HD
TVP1_REF = "1:0:1:3ABD:514:13E:820000:0:0:0:"


KIDS_REFS = [
    "1:0:1:3:1964:13E:820000:0:0:0:",
    "1:0:1:1CB6:1CE8:71:820000:0:0:0:",
    "1:0:1:1CB5:1CE8:71:820000:0:0:0:",
    "1:0:1:2938:1EDC:71:820000:0:0:0:",
    "1:0:19:10E5:3E8:13E:820000:0:0:0:",
    "1:0:1:9:1964:13E:820000:0:0:0:",
    "1:0:1:E:1964:13E:820000:0:0:0:",
    "1:0:1:13FC:5DC:13E:820000:0:0:0:",
    "1:0:19:10E4:3E8:13E:820000:0:0:0:",
    "1:0:1:3D5F:2C88:13E:820000:0:0:0:",
    "1:0:1:1CB7:1CE8:71:820000:0:0:0:",
    "1:0:16:7D9:22C4:13E:820000:0:0:0:",
    "1:0:1:3ACD:514:13E:820000:0:0:0:",
    "1:0:1:32E0:190:13E:820000:0:0:0:",
    "1:0:1:428E:2BC0:13E:820000:0:0:0:",
    "1:0:1:4280:2BC0:13E:820000:0:0:0:",
    "1:0:19:4530:30D4:13E:820000:0:0:0:",
    "1:0:19:213F:3070:13E:820000:0:0:0:",
]


KIDS_CHANNELS = [
    "CBeebies", "TVP ABC", "Cartoon Network", "Cartoonito",
    "Boomerang", "Nickelodeon", "Nicktoons", "Nick Jr",
    "Disney Channel", "Disney Junior", "Disney XD",
    "BabyTV", "ducktv", "MiniMini", "TeleTOON",
    "JimJam", "Da Vinci"
]


def normalize(name):
    name = name.lower()
    name = name.replace("hd", "")
    name = name.replace("+", "")
    name = name.replace(".", "")
    name = re.sub(r'[^a-z0-9 ]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def is_kid_channel(name, ref):
    if ref in KIDS_REFS:
        return True

    name_norm = normalize(name)
    for kid in KIDS_CHANNELS:
        if normalize(kid) in name_norm:
            return True

    return False




def load_time():
    if not os.path.exists(SAVE_FILE):
        return {"date": "", "time": 0}

    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"date": "", "time": 0}


def save_time(data):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("[KidsLimiter] save error:", e)


class KidsLimiter(object):

    def __init__(self, session):

        self.session = session
        self.onClose = []

        self.data = load_time()
        self.today = datetime.now().strftime("%Y-%m-%d")

        if self.data["date"] != self.today:
            self.data = {"date": self.today, "time": 0}

        self.popupShown = False

        self.timer = eTimer()
        self.timer.callback.append(self.checkTime)

        self.tracker = ServiceEventTracker(
            screen=self,
            eventmap={
                iPlayableService.evStart: self.serviceStarted
            }
        )

        print("[KidsLimiter] INIT daily time:", self.data["time"])

        self.timer.start(2000, True)


    def serviceStarted(self):

        service = self.session.nav.getCurrentService()
        if not service:
            return

        info = service.info()
        if not info:
            return

        name = info.getName()
        ref = self.session.nav.getCurrentlyPlayingServiceReference().toString()

        if not name or not ref:
            return

        print("[KidsLimiter] channel:", name)
        print("[KidsLimiter] ref:", ref)

        if is_kid_channel(name, ref):
            print("[KidsLimiter] KIDS CHANNEL DETECTED")
        else:
            print("[KidsLimiter] normal channel")


    def forceTVP1(self):
        print("[KidsLimiter] SWITCH TO TVP1:", TVP1_REF)

        try:
            self.session.nav.stopService()
        except:
            pass

        self.session.nav.playService(eServiceReference(TVP1_REF))


    def checkTime(self):

        service = self.session.nav.getCurrentService()
        if not service:
            return

        info = service.info()
        if not info:
            return

        name = info.getName()
        ref = self.session.nav.getCurrentlyPlayingServiceReference().toString()

        if not name or not ref:
            return

        
        if self.data["time"] >= LIMIT:
            if is_kid_channel(name, ref):
                print("[KidsLimiter] HARD BLOCK → TVP1")
                self.forceTVP1()
                self.timer.start(2000, True)
                return

        if is_kid_channel(name, ref):

            self.data["time"] += 2
            save_time(self.data)

            print("[KidsLimiter] daily time:", self.data["time"])

            if self.data["time"] >= LIMIT and not self.popupShown:
                self.popupShown = True

                print("[KidsLimiter] LIMIT REACHED → BLOCKING")

                self.session.open(
                    MessageBox,
                    "Limit dzienny dla dzieci osiągnięty!",
                    MessageBox.TYPE_INFO
                )

                self.forceTVP1()

        else:
            self.popupShown = False

        self.timer.start(2000, True)


def autostart(session, **kwargs):

    print("[KidsLimiter] START")

    session.kidsLimiter = KidsLimiter(session)


def Plugins(**kwargs):

    return [
        PluginDescriptor(
            where=PluginDescriptor.WHERE_SESSIONSTART,
            fnc=autostart
        )
    ]