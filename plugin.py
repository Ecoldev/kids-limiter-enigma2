# -*- coding: utf-8 -*-
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Components.ServiceEventTracker import ServiceEventTracker
from enigma import eTimer, iPlayableService, eServiceReference
import re
import json
import os
from datetime import datetime


LIMIT = 1200
SAVE_FILE = "/etc/enigma2/kids_time.json"

CHANNEL_TO_SWITCH = "1:0:1:3ABD:514:13E:820000:0:0:0:"


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
        return {"date": "", "time_seconds": 0}

    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)

        if "time" in data and "time_seconds" not in data:
            data["time_seconds"] = data.pop("time")

        if "time_seconds" not in data or not isinstance(data["time_seconds"], int):
            data["time_seconds"] = 0

        if "date" not in data:
            data["date"] = ""

        return data

    except Exception as e:
        print("[KidsLimiter] load error:", e)
        return {"date": "", "time_seconds": 0}


def save_time(data):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("[KidsLimiter] save error:", e)


class KidsLimiter(object):

    def __init__(self, session):
        import time

        self.lastSave = 0
        self.last_block_time = 0
        self.session = session
        self.onClose = []
        self.blocking = False
        self.popupShown = False
        self.limitReached = False
        self.switchScheduled = False

        self.lastBlockedRef = None   # 🔥 brakowało

        self.zapTimer = eTimer()
        self.data = load_time()
        self.today = datetime.now().strftime("%Y-%m-%d")

        if self.data["date"] != self.today:
            self.data = {"date": self.today, "time_seconds": 0}
            save_time(self.data)

        if self.data.get("time_seconds", 0) >= LIMIT:
            self.limitReached = True

        self.timer = eTimer()
        self.timer.callback.append(self.checkTime)

        self.tracker = ServiceEventTracker(
            screen=self,
            eventmap={
                iPlayableService.evStart: self.serviceStarted
            }
        )

        self.timer.start(2000, True)


    def scheduleSwitch(self):
        import time

        if self.switchScheduled:
            return

        now = time.time()

        if now - self.last_block_time < 3:
            return

        self.last_block_time = now
        self.switchScheduled = True

        def delayed():
            self.switchScheduled = False
            self.forceSwitchChannel()

        self.zapTimer = eTimer()
        self.zapTimer.callback.append(delayed)
        self.zapTimer.start(1000, False)


    def serviceStarted(self):
        refObj = self.session.nav.getCurrentlyPlayingServiceReference()
        if not refObj:
            return

        ref = refObj.toString()

        if ref == CHANNEL_TO_SWITCH:
            self.blocking = False
            self.switchScheduled = False
            self.lastBlockedRef = None   # 🔥 reset
            return


    def forceSwitchChannel(self):
        try:
            refObj = self.session.nav.getCurrentlyPlayingServiceReference()
            if not refObj:
                return

            ref = refObj.toString()

            service = self.session.nav.getCurrentService()
            if not service:
                return

            info = service.info()
            if not info:
                return

            name = info.getName()
            if not name:
                return

            #
            if not is_kid_channel(name, ref):
                print("[KidsLimiter] Not kid channel anymore - skip")
                self.blocking = False
                return

            target = eServiceReference(CHANNEL_TO_SWITCH)

            
            if ref == CHANNEL_TO_SWITCH:
                return

            print("[KidsLimiter] SWITCHING TO SAFE CHANNEL")
            self.session.nav.playService(target)

        except Exception as e:
            print("[KidsLimiter] SWITCH ERROR:", e)


    def checkTime(self):
        import time

        today = datetime.now().strftime("%Y-%m-%d")

        refObj = self.session.nav.getCurrentlyPlayingServiceReference()
        if not refObj:
            return

        ref = refObj.toString()

        if ref == CHANNEL_TO_SWITCH:
            return

        if self.data.get("time_seconds", 0) >= LIMIT:
            self.limitReached = True

        service = self.session.nav.getCurrentService()
        if not service:
            return

        info = service.info()
        if not info:
            return

        name = info.getName()
        if not name:
            return

        isKid = is_kid_channel(name, ref)

        if self.data.get("date") != today:
            self.data = {"date": today, "time_seconds": 0}
            self.limitReached = False
            self.popupShown = False
            self.blocking = False
            self.lastBlockedRef = None
            self.lastSave = 0
            save_time(self.data)

        if self.limitReached:
            if isKid:
                if not self.blocking:
                    print("[KidsLimiter] BLOCK KID CHANNEL")
                    self.blocking = True
                    self.scheduleSwitch()
            else:

                self.blocking = False
            return

        if not isKid:
            self.popupShown = False
            self.blocking = False
            self.lastBlockedRef = None
            return

        self.data["time_seconds"] += 2

        if time.time() - self.lastSave > 10:
            save_time(self.data)
            self.lastSave = time.time()

        limitNow = self.data["time_seconds"] >= LIMIT

        if limitNow and not self.limitReached:
            self.limitReached = True
            self.scheduleSwitch()
            return

        if limitNow and not self.popupShown:
            self.popupShown = True
            self.session.open(
                MessageBox,
                "Limit dzienny dla dzieci osiągnięty!",
                MessageBox.TYPE_INFO
            )


def autostart(session, **kwargs):
    session.kidsLimiter = KidsLimiter(session)


def Plugins(**kwargs):
    return [
        PluginDescriptor(
            where=PluginDescriptor.WHERE_SESSIONSTART,
            fnc=autostart
        )
    ]