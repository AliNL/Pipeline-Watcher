# coding=utf-8
from datetime import datetime, time
from os import system
from time import sleep
import re
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

WORK_DAYS = [0, 1, 2, 3, 4]
TUESDAY = [1]
NOT_TUESDAY = [0, 2, 3, 4]


def watch(watch_list, bundle_dir):
    stand_up = False
    dev_huddle = False
    ipm = False
    late = False
    while True:
        stand_up = alarm(stand_up, 'Stand up', (9, 45), bundle_dir, NOT_TUESDAY)
        dev_huddle = alarm(dev_huddle, 'Dev huddle', (15, 59), bundle_dir, NOT_TUESDAY)
        ipm = alarm(ipm, 'IPM', (9, 44), bundle_dir, TUESDAY)
        late = alarm(late, 'Late', (9, 15), bundle_dir, TUESDAY)


def alarm(should_alarm_today, event_name, alarm_time, bundle_dir, weekdays=WORK_DAYS):
    if datetime.now().time() < time(*alarm_time) and datetime.now().weekday() in weekdays:
        return True
    elif should_alarm_today:
        for i in range(2):
            system('afplay ' + bundle_dir + '/alarm.aiff -t 2.5 -v 10')
            system(f'say "{event_name} time[[slnc 800]]"')
        return False
    return False
