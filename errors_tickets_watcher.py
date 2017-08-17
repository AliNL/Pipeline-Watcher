# coding=utf-8
import json
from datetime import datetime, date
import workdays

from appJar import gui


def get_person_today(data):
    dev_list = data['dev_list']
    bqa_list = data['bqa_list']
    dev_start_day = date(*data['dev_start_day'])
    bqa_start_day = date(*data['bqa_start_day'])

    today = datetime.today().date()
    dev_workdays = workdays.networkdays(dev_start_day, today) - 1
    bqa_workdays = workdays.networkdays(bqa_start_day, today) - 1

    dev_today = dev_list[dev_workdays % len(dev_list)]
    bqa_today = bqa_list[bqa_workdays % len(bqa_list)]
    return dev_today, bqa_today


def errors_tickets_window(w, h, x, y):
    drag_from = None
    today = datetime.today().date()
    with open('data.json', 'r') as fr:
        data = json.load(fr)
    dev_list = data['dev_list']
    bqa_list = data['bqa_list']

    def set_person_today(dev_today, bqa_today):
        for dev0 in dev_list:
            app.setLabelBg("dev" + dev0, "white")
            app.setLabelFg("dev" + dev0, "black")
            app.setLabelCursor("dev" + dev0, "arrow")
        for bqa0 in bqa_list:
            app.setLabelBg("bqa" + bqa0, "white")
            app.setLabelFg("bqa" + bqa0, "black")
            app.setLabelCursor("bqa" + bqa0, "arrow")

        app.setLabelBg(dev_today, "#535353")
        app.setLabelFg(dev_today, "white")
        app.setLabelBg(bqa_today, "#535353")
        app.setLabelFg(bqa_today, "white")
        app.setLabelDragFunction(dev_today, [drag, drop])
        app.setLabelDragFunction(bqa_today, [drag, drop])

    def drag(widget):
        app.setLabelBg(widget, "white")
        app.setLabelFg(widget, "black")
        global drag_from
        drag_from = widget

    def drop(widget):
        global drag_from
        if drag_from[:3] == widget[:3]:
            app.setLabelBg(widget, "#535353")
            app.setLabelFg(widget, "white")
            app.setLabelCursor(drag_from, "arrow")
            app.unbindKey("<ButtonPress-1>")
            app.unbindKey("<ButtonRelease-1>")
            app.setLabelDragFunction(widget, [drag, drop])

            if widget[3:] in dev_list:
                dev_start = workdays.workday(today, -dev_list.index(widget[3:]))
                data['dev_start_day'] = [dev_start.year, dev_start.month, dev_start.day]
            elif widget[3:] in bqa_list:
                bqa_start = workdays.workday(today, -bqa_list.index(widget[3:]))
                data['bqa_start_day'] = [bqa_start.year, bqa_start.month, bqa_start.day]

            with open('data.json', 'w') as fw:
                json.dump(data, fw)

        else:
            app.setLabelBg(drag_from, "#535353")
            app.setLabelFg(drag_from, "white")

    def update_person():
        dev_today, bqa_today = get_person_today(data)
        set_person_today("dev" + dev_today, "bqa" + bqa_today)

    app = gui("Errors & Tickets")
    app.setGeom(int(w), int(h))
    app.setLocation(int(x), int(y))
    app.setGuiPadding(50, 40)
    app.setFont(32)
    app.setPadding(10, 30)

    i = 0
    for dev in dev_list:
        app.addLabel("dev" + dev, dev, 0, i, 1, 1)
        i += 1

    i = 0
    for bqa in bqa_list:
        app.addLabel("bqa" + bqa, bqa, 1, i, 1, 1)
        i += 1

    app.setAllLabelWidths(15)
    app.setAllLabelHeights(1)
    app.setStretch("row")
    app.setSticky(None)
    app.registerEvent(update_person)
    app.setPollTime(600000)
    app.go()
