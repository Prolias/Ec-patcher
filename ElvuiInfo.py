import requests
from LocalInfo import LocalInfo

ELVUI_API_URL = "https://www.tukui.org/api.php?ui=elvui"

class ElvuiInfo():
    def __init__(self):
        local = LocalInfo()
        self.elvui_path = local.elvui_path
        elvui_rq = self.get_data_from_api()
        self.elvui_url = elvui_rq["url"]
        self.elvui_version = elvui_rq["version"]
        self.local_version = self.get_local_version()

    def get_data_from_api(self):
        """Get data from url api and return in json format"""
        data = requests.get(ELVUI_API_URL, timeout=10)
        return data.json()

    def get_local_version(self):
        """Get the Elvui local version"""
        local_ver = ""
        with open(self.elvui_path, encoding="utf-8") as file:
            for line in file:
                if "version" in line.strip().lower():
                    local_ver = line.split(":",1)[1].strip()

        return local_ver
