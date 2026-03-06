#!/usr/bin/python
# -*- coding: utf-8 -*-

from .menus_list.mainhelpers import SystemInfo
from .menus_list.compat import compat_urlopen, compat_Request, PY3, readFromFile
from .menus_list.Console import Console

import os
from threading import Timer
from Components.ActionMap import NumberActionMap
from Components.Sources.StaticText import StaticText
from Components.Sources.List import List
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Console import Console as iConsole
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS
from Screens.Screen import Screen
from Plugins.Extensions.ServerEagleSat.__init__ import Version, Panel

class ServerEagleSat(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session

        # -------------------------
        # SKIN
        # -------------------------
        self.skin = readFromFile("/skins_list/mainmenu-fhd.xml")
        self.setTitle(_("ServerEagleSat"))

        # -------------------------
        # CORE
        # -------------------------
        self.iConsole = iConsole()
        self.indexpos = None
        self.system_info = SystemInfo()

        # -------------------------
        # ACTION MAPS
        # -------------------------
        self["NumberActions"] = NumberActionMap(
            ["NumberActions"],
            {'0': self.keyNumberGlobal}
        )

        self["shortcuts"] = NumberActionMap(
            ["ShortcutActions", "WizardActions", "ColorActions", "HotkeyActions"],
            {
                "ok": self.keyOK,
                "cancel": self.exit,
                "back": self.exit,
                "red": self.iptv,
                "info": self.infoKey,
                "green": self.cccam,
                "yellow": self.grid,
                "blue": self.scriptslist,
            }
        )

        # ===== SIDE BARS =====
        self["left_bar"] = Label("\n".join(list("Version " + Version)))
        self["right_bar"] = Label("\n".join(list("By ElieSat")))

        # ===== COLOR BUTTONS =====
        self["key_red"] = Label("Iptv Adder")
        self["key_green"] = Label("Cccam Adder")
        self["key_yellow"] = Label("News")
        self["key_blue"] = Label("Scripts")

        # -------------------------
        # MENU
        # -------------------------
        self.list = []
        self["menu"] = List(self.list)
        self.mList()

        # -------------------------
        # LABELS
        # -------------------------
        labels = ["MemoryLabel", "SwapLabel", "FlashLabel", "gstreamerLabel",
                  "pythonLabel", "CPULabel", "ipLabel", "macLabel",
                  "HardwareLabel", "ImageLabel", "KernelLabel",
                  "EnigmaVersionLabel", "driverLabel", "internetLabel"]
        text = [_("Ram:"), _("Swap:"), _("Flash:"), _("Gst:"), _("Py:"), _("Prc:"),
                _("IP address:"), _("Mac Address:"), _("Hdw:"), _("Img:"), _("Krn:"), _("Upd:"), _("Drv:"), _("Internet:")]

        for l, t in zip(labels, text):
            self[l] = StaticText(t)

        # -------------------------
        # VALUE FIELDS
        # -------------------------
        values = ["memTotal", "swapTotal", "flashTotal", "device", "gstreamer", "python",
                  "Hardware", "Image", "CPU", "Kernel", "ipInfo", "macInfo", "EnigmaVersion",
                  "driver", "internet"]

        for v in values:
            self[v] = StaticText()

        # -------------------------
        # FOOTER
        # -------------------------
        self["Version"] = Label(_("V" + Version))
        self["Panel"] = Label(_(Panel))

        # -------------------------
        # BOX ICON
        # -------------------------
        self["boxicon"] = Pixmap()
        self.onLayoutFinish.append(self.loadBoxIcon)

        # -------------------------
        # LOAD SYSTEM INFO
        # -------------------------
        self.system_info.memInfo(self)
        self.system_info.FlashMem(self)
        self.system_info.devices(self)
        self.system_info.mainInfo(self)
        self.system_info.cpuinfo(self)
        self.system_info.getPythonVersionString(self)
        self.system_info.getGStreamerVersionString(self)
        self.system_info.network_info(self)
        self.system_info.intInfo(self)

        # -------------------------
        # AUTO UPDATE CHECK
        # -------------------------
        Timer(0.5, lambda: self.system_info.update_me(self)).start()

    # -------------------------
    # MENU LIST
    # -------------------------
    def mList(self):
        self.list = []
        items = [
            ("Add reader", 1, _("كتابة اشتراك شيرينج و اضافة ريدر")),
            ("Live oscam status", 2, _("إدارة   الاوسكام ايميو و عرض الريدارات")),
            ("Live ncam status", 3, _("اداة الانكام ايميو و عرض الريدرات")),
            ("Live softcam file", 4, _("ادارة ملف السوفتكام و عرض المفاتيح و الشغرات")),
            ("Download install emus", 5, _("تنزيل و تثبيت الايميوهات")),
            ("Download install softcam", 6, _("تنزيل و تثبيت ملف السوفتكام")),
            ("Remove emus", 7, _("حذف الايميوهات يالكامل")),
            ("Show emus files", 8, _("تصفح ملفات الايميوهات")),
            ("Show log file", 9, _("عرض ملف اللوج")),
            ("Show expiracy date", 10, _("عرض عدد الايام المتبقية للاشتراك")),
            ("About", 11, _("About"))
        ]

        for item_name, item_id, item_desc in items:
            img_path = "Extensions/ServerEagleSat/icons_list/menu/{}.png".format(item_name)
            img = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, img_path))
            self.list.append((_(item_name), item_id, item_desc, img))

        if getattr(self, "indexpos", None) is not None:
            self["menu"].setIndex(self.indexpos)
        self["menu"].setList(self.list)

    # -------------------------
    # BOX ICON LOADING
    # -------------------------
    def loadBoxIcon(self):
        try:
            hostname_file = "/etc/hostname"
            box_name = "default"
            if os.path.exists(hostname_file):
                with open(hostname_file, "r") as f:
                    content = f.read().strip()
                    if content:
                        box_name = content.lower()

            icon_folder = resolveFilename(SCOPE_PLUGINS, "Extensions/ServerEagleSat/icons_list/boxicons/")
            icon_file = os.path.join(icon_folder, f"{box_name}.png")
            default_icon = os.path.join(icon_folder, "default.png")

            if not fileExists(icon_file):
                print(f"Box icon not found for '{box_name}', using default")
                icon_file = default_icon

            pixmap = LoadPixmap(cached=True, path=icon_file)
            if pixmap:
                self["boxicon"].instance.setPixmap(pixmap)
                self["boxicon"].show()
                print(f"Box icon loaded: {icon_file}")
            else:
                print(f"Failed to load pixmap: {icon_file}")

        except Exception as e:
            print("Error loading box icon:", e)

    # -------------------------
    # KEYS
    # -------------------------
    def keyOK(self, item=None):
        self.indexpos = self["menu"].getIndex()
        if item is None:
            item = self["menu"].getCurrent()[1]
        self.select_item(item)

    def select_item(self, item):
        pass

    def keyNumberGlobal(self, number):
        if number == 0:
            self.session.open(Console, _("Updating ElieSatPanelList, please wait..."), [
                "wget --no-check-certificate https://raw.githubusercontent.com/eliesat/eliesatpanel/main/installer.sh -qO - | /bin/sh"
            ])

    def exit(self):
        self.close()

    def iptv(self):
        pass

    def cccam(self):
        pass

    def grid(self):
        pass

    def scriptslist(self):
        pass

    def infoKey(self):
        self.session.open(Console, _("Please wait..."), [
            "wget --no-check-certificate https://gitlab.com/eliesat/scripts/-/raw/main/check/_check-all.sh -qO - | /bin/sh"
        ])
