# coding=utf-8
import os

from src.errors_tickets_watcher import ErrorsTicketsWindow

# bundle_dir = os.path.dirname(sys.executable)
bundle_dir = '.'
if not os.path.exists(bundle_dir + '/data.json'):
    print("\n\nPlease put data.json in same directory.")
else:
    ErrorsTicketsWindow(bundle_dir).start()
