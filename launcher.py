# coding=utf-8
import sys
import os
from errors_tickets_watcher import ErrorsTicketsWindow


bundle_dir = os.path.dirname(sys.executable)
if not os.path.exists(bundle_dir + '/data.json'):
    print("\n\nPlease put data.json in same directory.")
else:
    ErrorsTicketsWindow(bundle_dir).start()