# coding=utf-8
import json
import threading
import workdays
from appJar import gui
from datetime import datetime, date, timedelta
from browsers_watcher import open_browser, watch

(MON, TUE, WED, THU, FRI, SAT, SUN) = range(7)


def networkdays_without_tuesday(start_date, end_date):
    weekends = (SAT, SUN, TUE)
    delta_days = (end_date - start_date).days + 1
    full_weeks, extra_days = divmod(delta_days, 7)
    num_workdays = (full_weeks + 1) * (7 - len(weekends))
    for d in range(1, 8 - extra_days):
        if (end_date + timedelta(d)).weekday() not in weekends:
            num_workdays -= 1
    return num_workdays


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
        self.host_start_day = date(*self.data['host_start_day'])
        self.dev_today = 0
        self.bqa_today = 0
        self.host_today = 0
        self.today = None
        self.app = gui("Errors & Tickets")
        self.w = self.app.topLevel.winfo_screenwidth()
        self.h = self.app.topLevel.winfo_screenheight()
        self.pipelines = open_browser(self.data, self.w, self.h)
        self.browsers_watching = threading.Thread(target=watch, args=[self.pipelines, self.bundle_dir])
        self.browsers_watching.start()

    def save_person_today(self):
        with open(self.bundle_dir + '/data.json', 'w') as fw:
            json.dump(self.data, fw)
        return True

    def get_person_today(self):
        self.today = datetime.today().date()
        dev_workdays = workdays.networkdays(self.dev_start_day, self.today) - 1
        bqa_workdays = workdays.networkdays(self.bqa_start_day, self.today) - 1
        host_workdays = networkdays_without_tuesday(self.host_start_day, self.today) - 1
        self.dev_today = dev_workdays % len(self.dev_list)
        self.bqa_today = bqa_workdays % len(self.bqa_list)
        self.host_today = host_workdays % (len(self.dev_list) + len(self.bqa_list))

        if self.dev_today == 0 and self.data['dev_start_day'][2] != self.today.day:
            self.data['dev_start_day'] = [self.today.year, self.today.month, self.today.day]
            self.dev_start_day = date(*self.data['dev_start_day'])

        if self.bqa_today == 0 and self.data['bqa_start_day'][2] != self.today.day:
            self.data['bqa_start_day'] = [self.today.year, self.today.month, self.today.day]
            self.bqa_start_day = date(*self.data['bqa_start_day'])

        if self.host_today == 0 and self.data['host_start_day'][2] != self.today.day:
            self.data['host_start_day'] = [self.today.year, self.today.month, self.today.day]
            self.bqa_start_day = date(*self.data['host_start_day'])

        self.save_person_today()

    def set_person_today(self):
        for dev in self.dev_list:
            self.app.setLabelBg(dev, "white")
            self.app.setLabelFg(dev, "black")

        for bqa in self.bqa_list:
            self.app.setLabelBg(bqa, "white")
            self.app.setLabelFg(bqa, "black")

        host = self.dev_list[self.host_today] \
            if self.host_today < len(self.dev_list) \
            else self.bqa_list[self.host_today - len(self.dev_list)]

        self.app.setLabelBg(self.dev_list[self.dev_today], "#535353")
        self.app.setLabelFg(self.dev_list[self.dev_today], "white")
        self.app.setLabelBg(self.bqa_list[self.bqa_today], "#535353")
        self.app.setLabelFg(self.bqa_list[self.bqa_today], "white")
        self.app.setLabelFg(host, "#FFBA00")

    def move_dev_list(self, btn):
        self.dev_today = (self.dev_today + 1) % len(self.dev_list)
        dev_start = workdays.workday(self.today, -self.dev_today)
        self.data['dev_start_day'] = [dev_start.year, dev_start.month, dev_start.day]
        self.dev_start_day = date(*self.data['dev_start_day'])
        self.set_person_today()

    def move_bqa_list(self, btn):
        self.bqa_today = (self.bqa_today + 1) % len(self.bqa_list)
        bqa_start = workdays.workday(self.today, -self.bqa_today)
        self.data['bqa_start_day'] = [bqa_start.year, bqa_start.month, bqa_start.day]
        self.bqa_start_day = date(*self.data['bqa_start_day'])
        self.set_person_today()

    def move_host_list(self, btn):
        self.host_today = (self.host_today + 1) % (len(self.dev_list) + len(self.bqa_list))
        host_start = workdays.workday(self.today, -self.host_today)
        self.data['host_start_day'] = [host_start.year, host_start.month, host_start.day]
        self.host_start_day = date(*self.data['host_start_day'])
        self.set_person_today()

    def update_person(self):
        self.get_person_today()
        self.set_person_today()
        self.check_browsers_alive()

    def check_browsers_alive(self):
        if not self.browsers_watching.isAlive():
            self.browsers_watching = threading.Thread(target=watch, args=[self.pipelines, self.bundle_dir])
            self.browsers_watching.start()

    def start(self):
        self.app.setGeom(int(self.w / 2), int(self.h * 0.4 - 25))
        self.app.setLocation(0, int(self.h * 0.6 + 10))
        self.app.setGuiPadding(50, 40)
        self.app.setFont(32)
        self.app.setPadding(10, 30)
        i = j = 0

        for i in range(len(self.dev_list)):
            self.app.addLabel(self.dev_list[i], self.dev_list[i], 0, i, 1, 1)

        for j in range(len(self.bqa_list)):
            self.app.addLabel(self.bqa_list[j], self.bqa_list[j], 1, j, 1, 1)

        self.app.addLabel("help", """按 d 移动Dev\n按 b 移动BA/QA\n按 h 移动Host""", 1, j + 1, i - j, 1)
        self.app.setLabelFg("help", "#A6A6A6")
        self.app.getLabelWidget("help").config(font=12)

        self.app.setAllLabelWidths(15)
        self.app.setAllLabelHeights(1)
        self.app.setStretch("row")
        self.app.setSticky(None)
        self.app.bindKey('<d>', self.move_dev_list)
        self.app.bindKey('<b>', self.move_bqa_list)
        self.app.bindKey('<h>', self.move_host_list)
        self.app.setStopFunction(self.save_person_today)
        self.app.registerEvent(self.update_person)
        self.app.setPollTime(600000)
        self.app.go()
