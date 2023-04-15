# Use these functions to make an asynchronous POST request to the server

import requests
import asyncio
# You must install ctime_binding to have this method in your python path
from ctime_binding import get_c_time

# Send a post request
def log_time(code):
    # Get the time from the c binding
    now = get_c_time()

    asyncio.run(_log_time(code, now[0], now[1]))

# async helper methodd
async def _log_time(code, sec, usec):
    # Send a post request
    url = "http://localhost:4560/report"

    time_stamp = {
        "identifier": code,
        "time": {
            "sec": sec,
            "usec": usec
        }
    }
    print("LOGGING IN PYTHON: ", time_stamp)

    requests.post(url, json = time_stamp)

