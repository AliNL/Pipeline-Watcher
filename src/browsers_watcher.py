# coding=utf-8
from datetime import datetime, time
from os import system
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

WORK_DAYS = [0, 1, 2, 3, 4]
TUESDAY = [1]
NOT_TUESDAY = [0, 2, 3, 4]


def open_browser(data):
    cd = webdriver.Firefox()
    cd.maximize_window()
    cd.get(data["cd_url"])
    sleep(1)
    cd.find_element_by_id('user_login').send_keys(data["cd_username"])
    cd.find_element_by_id('user_password').send_keys(data["cd_password"])
    sleep(1)
    cd.find_element_by_id('signin2').click()
    return [cd]


def get_status(pipeline, retry=5):
    try:
        status_elements = pipeline.find_elements_by_css_selector('a.pipeline_stage.failed')
        current_status = [s.get_attribute('href').split('/go/pipelines/')[1] for s in status_elements]
        return current_status
    except WebDriverException:
        if retry > 0:
            return get_status(pipeline, retry - 1)
        else:
            return []


def watch(watch_list, bundle_dir):
    last_status = []
    for pipeline in watch_list:
        this_status = get_status(pipeline)
        last_status.append(this_status)
    sleep(10)
    stand_up = False
    dev_huddle = False
    ipm = False
    late = False
    while True:
        stand_up = alarm(stand_up, 'Stand up', (9, 0), bundle_dir, NOT_TUESDAY)
        dev_huddle = alarm(dev_huddle, 'Dev huddle', (9, 29), bundle_dir, NOT_TUESDAY)
        ipm = alarm(ipm, 'IPM', (9, 44), bundle_dir, TUESDAY)
        late = alarm(late, 'Late', (9, 0), bundle_dir, TUESDAY)
        i = 0
        for pipeline in watch_list:
            current_status = get_status(pipeline)
            for status in current_status:
                if status not in last_status[i]:
                    print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"), status)
                    system('say "Pipeline Broken[[slnc 1000]]"')
                    system('say "' + status.replace("/", "[[slnc 300]]") + '"')
            last_status[i] = current_status
            i += 1
        sleep(10)


def alarm(should_alarm_today, event_name, alarm_time, bundle_dir, weekdays=WORK_DAYS):
    if datetime.now().time() < time(*alarm_time) and datetime.now().weekday() in weekdays:
        return True
    elif should_alarm_today:
        for i in range(2):
            system('afplay ' + bundle_dir + '/alarm.aiff -t 2.5 -v 10')
            system(f'say "{event_name} time[[slnc 800]]"')
        return False
    return False
