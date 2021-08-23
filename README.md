OxyCon 2021 Active Fingerprinting With Pyppeteer Code Samples
==

Tested with python3.8

Requirements:
```
pip install -r requirements.txt
```

Timezone mocking will not work with the default chromium revision, so you need
to export this environment variable:
```
PYPPETEER_CHROMIUM_REVISION=747023
```

Proxy authentication info is contained in `proxy_auth.py` files:
```python
PROXY_URL = "http://pr.oxylabs.io:8000"
PROXY_USERNAME = "user"
PROXY_PASSWORD = "password"
```
Change these constants to your credentials.
