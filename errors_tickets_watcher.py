# coding=utf-8
import json
import threading
import workdays
from appJar import gui
from datetime import datetime, date
from browsers_watcher import open_browser, watch


class ErrorsTicketsWindow(object):
    def __init__(self, bundle_dir):
        self.bundle_dir = bundle_dir
        with open(bundle_dir + '/data.json', 'r') as fr:
            data = json.load(fr)
        self.data = data
        self.dev_list = self.data['dev_list']
        self.bqa_list = self.data['bqa_list']
        self.dev_start_day = date(*self.data['dev_start_day'])
        self.bqa_start_day = date(*self.data['bqa_start_day'])
        self.dev_today = None
        self.bqa_today = None
        self.today = datetime.today().date()
        self.get_person_today()
        self.app = gui("Errors & Tickets")
        self.drag_from = None
        self.pipelines = open_browser(self.data)
        self.browsers_watching = threading.Thread(target=watch, args=[self.pipelines])
        self.browsers_watching.start()

    def get_person_today(self):
        self.today = datetime.today().date()
        dev_workdays = workdays.networkdays(self.dev_start_day, self.today) - 1
        bqa_workdays = workdays.networkdays(self.bqa_start_day, self.today) - 1
        self.dev_today = self.dev_list[dev_workdays % len(self.dev_list)]
        self.bqa_today = self.bqa_list[bqa_workdays % len(self.bqa_list)]

    def set_person_today(self):
        for dev in self.dev_list:
            self.app.setLabelBg("dev" + dev, "white")
            self.app.setLabelFg("dev" + dev, "black")
            self.app.setLabelCursor("dev" + dev, "arrow")
        for bqa in self.bqa_list:
            self.app.setLabelBg("bqa" + bqa, "white")
            self.app.setLabelFg("bqa" + bqa, "black")
            self.app.setLabelCursor("bqa" + bqa, "arrow")
        self.app.unbindKey("<ButtonPress-1>")
        self.app.unbindKey("<ButtonRelease-1>")
        self.app.setLabelBg("dev" + self.dev_today, "#535353")
        self.app.setLabelFg("dev" + self.dev_today, "white")
        self.app.setLabelBg("bqa" + self.bqa_today, "#535353")
        self.app.setLabelFg("bqa" + self.bqa_today, "white")
        self.app.setLabelDragFunction("dev" + self.dev_today, [self.drag, self.drop])
        self.app.setLabelDragFunction("bqa" + self.bqa_today, [self.drag, self.drop])

    def drag(self, widget):
        self.app.setLabelBg(widget, "white")
        self.app.setLabelFg(widget, "black")
        self.drag_from = widget

    def drop(self, widget):
        if self.drag_from[:3] == widget[:3]:
            self.app.setLabelBg(widget, "#535353")
            self.app.setLabelFg(widget, "white")
            self.app.setLabelCursor(self.drag_from, "arrow")
            self.app.unbindKey("<ButtonPress-1>")
            self.app.unbindKey("<ButtonRelease-1>")
            self.app.setLabelDragFunction(widget, [self.drag, self.drop])

            if widget[:3] == 'dev':
                dev_start = workdays.workday(self.today, -self.dev_list.index(widget[3:]))
                self.data['dev_start_day'] = [dev_start.year, dev_start.month, dev_start.day]
                self.dev_start_day = date(*self.data['dev_start_day'])
            elif widget[:3] == 'bqa':
                bqa_start = workdays.workday(self.today, -self.bqa_list.index(widget[3:]))
                self.data['bqa_start_day'] = [bqa_start.year, bqa_start.month, bqa_start.day]
                self.bqa_start_day = date(*self.data['bqa_start_day'])

            with open(self.bundle_dir + '/data.json', 'w') as fw:
                json.dump(self.data, fw)
        else:
            self.app.setLabelBg(self.drag_from, "#535353")
            self.app.setLabelFg(self.drag_from, "white")

    def update_person(self):
        self.get_person_today()
        self.set_person_today()
        self.check_browsers_alive()

    def check_browsers_alive(self):
        if not self.browsers_watching.isAlive():
            self.browsers_watching = threading.Thread(target=watch, args=[self.pipelines])
            self.browsers_watching.start()

    def start(self):
        w = self.app.topLevel.winfo_screenwidth()
        h = self.app.topLevel.winfo_screenheight()
        self.app.setGeom(int(w / 2), int(h * 0.4 - 25))
        self.app.setLocation(0, int(h * 0.6 + 10))
        self.app.setGuiPadding(50, 40)
        self.app.setFont(32)
        self.app.setPadding(10, 30)

        for i in range(len(self.dev_list)):
            self.app.addLabel("dev" + self.dev_list[i], self.dev_list[i], 0, i, 1, 1)

        for i in range(len(self.bqa_list)):
            self.app.addLabel("bqa" + self.bqa_list[i], self.bqa_list[i], 1, i, 1, 1)

        self.app.setAllLabelWidths(15)
        self.app.setAllLabelHeights(1)
        self.app.setStretch("row")
        self.app.setSticky(None)
        self.app.registerEvent(self.update_person)
        self.app.setPollTime(600000)
        self.app.go()
