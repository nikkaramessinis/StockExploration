# Install dependencies

Supported Python version: 3.10.9

## How to install talib
Download:
TA_Lib-0.4.29-cp310-cp310-win_amd64.whl (WINDOWS only)
https://github.com/cgohlke/talib-build/releases


```
pip install TA_Lib-0.4.29-cp310-cp310-win_amd64.whl
```

## Install other dependencies
```
pip3 install -r requirements.txt -U;
```

## From Nick:
In order to make this work you need a secrets.py 
and out your api key IEX_CLOUD_API_TOKEN = "" from https://iexcloud.io/ 
.Sign in there and copy the api_token there

undervalued calculator is the main python file to run

## How to start the app

To run the app, you can use the following command:
```
python3 main.py
```

Entry point of the app is `main.py`

This will use `config/setting.yaml` to run commands.

Supported commands:
1. fetch_stocks (multiple stocks are supported)
2. run_strategy (multiple strategies are supported)
3. email_alerts (multiple recipients are supported)

e.g
```
run_commands:               # command to run in order
  - fetch_stocks
  - run_strategy
  - email_alerts
stocks:                     # list of stocks to use
  - AAPL
  - MSFT
  - GOOG
display_dashboard: true           # display all the graphs and tables in html format
strategies:                 # list of strategies to run (in order)
  - name: technical_analysis
email_alerts:
  enabled: true             # enable/disable email alerts
  recipients:               # list of recipients
    - "example1@gmail.com"
    - "example2@gmail.com"
```


## How to setup email alerts

create a secrets.py inside config dir and add the following information:

GMAIL_ADDRESS=""

GMAIL_PASSWORD=""
