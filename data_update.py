# !/usr/bin/env python3
# coding=utf-8
# =============================================================================
# Author: Luke Etherington
# Email: sc18lge@leeds.ac.uk
# Module: COMP3932 - Synoptic project
# Supervisor: Nick Efford
#
# Visualising Data Security Incidents using VCDB
#
# data_update.py
# used to automatically update the local copy of the VCBD data by fetching current data from the VCDB GitHub repo
# =============================================================================


import io
import timeit
import zipfile

import requests

URL = "https://github.com/vz-risk/VCDB/blob/master/data/joined/vcdb.json.zip?raw=true"

## Fetches up to date json data from VCDB github repo and writes to data file
def update_zip_file():
    response = requests.get(URL)
    if response.status_code == 200:
        zfile = zipfile.ZipFile(io.BytesIO(response.content))
        zfile.extractall("./data/")
    return response.status_code


# if __name__ == "__main__":
#     start = timeit.default_timer()
#     update_zip_file()
#     print(timeit.default_timer() - start)
