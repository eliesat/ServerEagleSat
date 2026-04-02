#!/usr/bin/python
# -*- coding: utf-8 -*-

from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap


class Eagle4(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)

        self.skin = """
        <screen name="Blank1" position="center,center" size="600,200" title="Blank1">
            <widget name="text" position="20,60" size="560,80" font="Regular;40" halign="center" />
        </screen>
        """

        self["text"] = Label("ServerEagleSat")

        print("ServerEagleSat")

        # -------------------------
        # EXIT / BACK CONTROL
        # -------------------------
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions", "WizardActions"],
            {
                "cancel": self.close,
                "back": self.close,
                "ok": self.close
            },
            -1
        )