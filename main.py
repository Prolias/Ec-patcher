"""Get information on ElvUI version and update if necessary"""

import os
import zipfile as zipF
import requests
from tqdm import tqdm

ELVUI_API_URL = "https://api.tukui.org/v1/addon/elvui"

def get_install_path():
    """Get installation path from install_path.ini"""
    with open('install_path.ini', encoding="utf-8") as file:
        path = ""
        for line in file:
            if "wow_path" in line:
                strt_path = line.split('=', 1)[1].replace('"', '').strip()
                path = strt_path + r'\_retail_\Interface\AddOns\\'

    return path

def get_data_from_api(url):
    """Get data from url api and return in json format"""
    data = requests.get(url, timeout=10)
    return data.json()

def get_local_version(url):
    """Get the Elvui local version"""
    local_ver = ""
    with open(rf'{url}ElvUI\ElvUI_Mainline.toc', encoding="utf-8") as file:
        for line in file:
            if "version" in line.strip().lower():
                local_ver = line.split(":",1)[1].strip()

    return local_ver

def update(download_url):
    """Download the file and return it"""
    res = requests.get(download_url, timeout=10)
    total_size = int(res.headers["Content-Length"])
    downloaded = 0
    chunksize = 1024
    bars = total_size // chunksize
    # savefile = download_url.split("/")[-1]
    savefile = f'v{elvui_version}.zip'
    with open(savefile, "wb") as file:
        for chunk in tqdm(res.iter_content(chunk_size=chunksize),
        total=bars, unit="kB", ncols=80, desc=savefile, leave=True):
            file.write(chunk)
            downloaded += chunksize

    return savefile

def upgrade(input_file):
    """Unzip the archive in the installation path"""
    with zipF.ZipFile(input_file, 'r') as archive:
        archive.extractall(get_install_path())

    cleanup(input_file)

def cleanup(input_file):
    """Cleanup the file in current folder"""
    try:
        os.remove(input_file)
    except OSError as err:
        print(f"Error: {err.filename} - {err.strerror}.")


if __name__ == '__main__':
    try:
        local_version = get_local_version(get_install_path())
        print(f'Version locale : {local_version} \n')

        print('Récupération des données de Elvui en cours...\n')

        elvui_rq = get_data_from_api(ELVUI_API_URL)

        elvui_version = elvui_rq["version"]
        elvui_url = elvui_rq["url"]

        print(f'Version de ElvUI : {elvui_version}')

        if elvui_version > local_version:
            print("Mise à jour requise")
            print("Téléchargement en cours : ")
            upgrade(update(elvui_url))

        else:
            print("A jour!")
    except Exception as e:
        print("Problème à l'éxécution.")
        print(e)
    finally:
        input("Press any key to continue...")
