# Pipeline-Watcher
For PSA Team internal

## Set up steps:
1. Install Chrome, latest version
1. Put "chromedriver" in "/usr/local/bin" or add its dirctory to PATH
1. Put "data.json" in same directory with "Pipeline Watcher"
1. Make alias for "Pipeline Watcher" on desktop
1. Run


## data.json
```json
{"cd_url": "Pipeline url",
 "cd_username": "Pipeline username",
 "cd_password": "pipeline password", 
 "dev_list": ["dev list in utf8 format"], 
 "bqa_list": ["bqa list in utf8 format"], 
 "dev_start_day": [2018, 12, 2], 
 "bqa_start_day": [2018, 12, 27], 
 "host_start_day": [2018, 12, 2], 
 "holidays": ["2018-12-30", "2018-12-31", "2019-01-01", "2019-02-04", "2019-02-05", "2019-02-06", "2019-02-07", "2019-02-08", "2019-02-09", "2019-02-10", "2019-04-05", "2019-04-06", "2019-04-07", "2019-05-01", "2019-06-07", "2019-06-08", "2019-06-09", "2019-09-13", "2019-09-14", "2019-09-15", "2019-10-01", "2019-10-02", "2019-10-03", "2019-10-04", "2019-10-05", "2019-10-06", "2019-10-07"], 
 "extraworkdays": ["2018-12-10", "2018-12-29", "2019-02-02", "2019-02-03", "2019-09-29", "2019-10-12"]}
```
