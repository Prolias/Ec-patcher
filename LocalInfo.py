class LocalInfo():
    def __init__(self):
        self.path = self.get_install_path()
        self.elvui_path = rf"{self.path}ElvUI\ElvUI_Mainline.toc"

    def get_install_path(self):
        """Get installation path from install_path.ini"""
        with open('install_path.ini', encoding="utf-8") as file:
            path = ""
            for line in file:
                if "wow_path" in line:
                    strt_path = line.split('=', 1)[1].replace('"', '').strip()
                    path = strt_path + r'\_retail_\Interface\AddOns\\'

        return path
