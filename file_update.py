import requests, zipfile, io

URL = "https://github.com/vz-risk/VCDB/blob/master/data/joined/vcdb.json.zip?raw=true"

def update_zip_file():
    response = requests.get(URL)
    if response.status_code == 200:
        zfile = zipfile.ZipFile(io.BytesIO(response.content))
        zfile.extractall("D:/Documents/UNI/COMP3932 - Synoptic Project/repo/data")
    return response.status_code

if __name__ == "__main__":
    update_zip_file()