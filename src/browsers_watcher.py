# coding=utf-8
from datetime import datetime, time
from time import sleep
from os import system
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def open_browser(data, w, h):
    # ci = webdriver.Chrome()
    # ci.set_window_size(w / 2, h * 0.6)
    # ci.set_window_position(0, 0)
    # ci.get('https://goci.psa.thoughtworks.net/go/pipelines')
    # sleep(1)
    # ci.find_element_by_id('user_login').send_keys(data["ci_username"])
    # ci.find_element_by_id('user_password').send_keys(data["ci_password"])
    # ci.find_element_by_id('signin2').click()

    cd = webdriver.Firefox()
    # cd.set_window_size(w / 2, h)
    # cd.set_window_position(w / 2 + 1, 0)
    cd.maximize_window()
    cd.get('https://gocd.thoughtworks.net/go/pipelines')
    sleep(1)
    cd.find_element_by_id('user_login').send_keys(data["cd_username"])
    cd.find_element_by_id('user_password').send_keys(data["cd_password"])
    sleep(1)
    cd.find_element_by_id('signin2').click()
    return [cd]


def get_status(pipeline, retry=5):
    url_length = len(pipeline.current_url) + 1
    try:
        status_elements = pipeline.find_elements_by_css_selector('a.stage')
        current_status = [s.get_attribute('href')[url_length:] for s in status_elements
                          if 'Fail' in s.find_element_by_css_selector('div.stage_bar').get_attribute('title')]
        psa_status = [s for s in current_status if not s.startswith('Identity') and not s.startswith('GoFigure')]
        return psa_status
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
    while True:
        stand_up = alarm(stand_up, 'Stand up', (9, 0), bundle_dir)
        dev_huddle = alarm(dev_huddle, 'Dev huddle', (9, 29), bundle_dir)
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


def alarm(should_alarm_today, event_name, alarm_time, bundle_dir):
    if datetime.now().time() < time(*alarm_time) and datetime.now().weekday() < 5:
        return True
    elif should_alarm_today:
        for i in range(2):
            system('afplay ' + bundle_dir + '/alarm.aiff -t 2.5 -v 10')
            system(f'say "{event_name} time[[slnc 800]]"')
        return False
    return False
