# coding=utf-8
import threading
from browsers_watcher import open_browser, watch
from errors_tickets_watcher import errors_tickets_window

ci_driver, cd_driver, w, h = open_browser()
browsers_watching = threading.Thread(target=watch, args=([[ci_driver, cd_driver]]))
browsers_watching.start()
errors_tickets_window(w / 2, h * 0.4 - 25, 0, h * 0.6 + 25)
