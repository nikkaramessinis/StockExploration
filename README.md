# Install dependencies

Supported version is Python 3.10.9
The main execution file is tenchical_analysis.py
Download:
TA_Lib-0.4.29-cp310-cp310-win_amd64.whl
from: https://github.com/cgohlke/talib-build/releases
and:
```
pip install TA_Lib-0.4.29-cp310-cp310-win_amd64.whl
```
Then to install the rest of the dependencies:
```
pip3 install -r requirements.txt -U;
```
In order to make this work you need a secrets.py 
and out your api key IEX_CLOUD_API_TOKEN = "" from https://iexcloud.io/ 
.Sign in there and copy the api_token there

undervalued calculator is the main python file to run