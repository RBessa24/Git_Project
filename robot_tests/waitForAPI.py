# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2023-04-22 18:08:29
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2023-04-24 09:48:39
import requests
import time
import os

endpoint_url = os.getenv("WAIT_FOR_ENDPOINT_URL")

start_time = time.time()
timeout = 300  # 5 minutes in seconds
poll_interval = 10  # 10 seconds between each poll

while True:
    print(f"\nQuerying '{endpoint_url}'...")
    try:
        response = requests.get(endpoint_url)
        if response.status_code == 200:
            print("Endpoint returned HTTP 200!")
            break
        else:
            print(f"Endpoint returned HTTP {response.status_code}. Retrying...")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}. Retrying...")

    elapsed_time = time.time() - start_time
    if elapsed_time >= timeout:
        print("Timeout exceeded. Exiting...")
        exit(1)

    time.sleep(poll_interval)