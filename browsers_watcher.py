# coding=utf-8
import json
import os
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def open_browser(bundle_dir):
    with open(bundle_dir + '/data.json', 'r') as f:
        data = json.load(f)
    ci = webdriver.Firefox()
    ci.maximize_window()
    w = ci.get_window_size()['width']
    h = ci.get_window_size()['height']
    ci.set_window_size(w / 2, h * 0.6)
    ci.set_window_position(0, 0)
    ci.get('https://goci.psa.thoughtworks.net/go/pipelines')
    time.sleep(1)
    ci.find_element_by_id('user_login').send_keys(data["ci_username"])
    ci.find_element_by_id('user_password').send_keys(data["ci_password"])
    ci.find_element_by_id('signin2').click()

    cd = webdriver.Firefox()
    cd.set_window_size(w / 2, h)
    cd.set_window_position(w / 2 + 1, 0)
    cd.get('https://gocd.thoughtworks.net/go/pipelines')
    time.sleep(1)
    cd.find_element_by_id('user_login').send_keys(data["cd_username"])
    cd.find_element_by_id('user_password').send_keys(data["cd_password"])
    cd.find_element_by_id('signin2').click()
    return ci, cd, w, h


def get_status(pipeline, retry=5):
    url_length = len(pipeline.current_url) + 1
    try:
        status_elements = pipeline.find_elements_by_css_selector('a.stage')
        current_status = [s.get_attribute('href')[url_length:] for s in status_elements
                          if 'Fail' in s.find_element_by_css_selector('div.stage_bar').get_attribute('title')]
        return current_status
    except WebDriverException:
        if retry > 0:
            return get_status(pipeline, retry - 1)
        else:
            return []


def watch(watch_list):
    last_status = []
    for pipeline in watch_list:
        this_status = get_status(pipeline)
        last_status.append(this_status)
    time.sleep(10)
    while True:
        i = 0
        for pipeline in watch_list:
            current_status = get_status(pipeline)
            for status in current_status:
                if status not in last_status[i]:
                    print(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()), status)
                    os.system('say "Pipeline Broken[[slnc 1000]]"')
                    os.system('say "' + status.replace("/", "[[slnc 300]]") + '"')
            last_status[i] = current_status
            i += 1
        time.sleep(10)
