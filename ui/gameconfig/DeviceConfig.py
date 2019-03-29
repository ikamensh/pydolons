from PySide2.QtWidgets import QDesktopWidget


class DeviceConfig:
    RESOLUTIONS = ((800, 600),
                   (1024, 768),
                   (1280, 800),
                   (1280, 1024),
                   (1280, 720),
                   (1360, 768),
                   (1366, 768),
                   (1440, 900),
                   (1536, 864),
                   (1600, 900),
                   (1680, 1050),
                   (1920, 1200),
                   (1920, 1080),
                   (2560, 1080),
                   (2560, 1440),
                   (3440, 1440),
                   (3840, 2160))

    def __init__(self, cfg):
        self.setUpScreen()
        cfg.dev_size = self.dev_size
        cfg.resolutions = self.RESOLUTIONS
        pass

    def setUpScreen(self):
        """
        :atribute ava_size  - доступный размер
        :atribute dev_size  - размер устройства
        :atribute ava_ha_size  - доступный размер деленый на 2
        :atribute dev_size  - размер устройства деленый на 2
        """
        self.desktop = QDesktopWidget()
        self.dev_size = self.desktop.screenGeometry(
        ).width(), self.desktop.screenGeometry().height()
        self.device_resolution = self.dev_size[0], self.dev_size[1]
        if self.device_resolution not in self.RESOLUTIONS:
            self.device_resolution = self.RESOLUTIONS[0]

    def updateScreenSize(self, w, h):
        self.dev_size = (w, h)

    def get_all_size(self):
        import csv
        self.RESOLUTIONS
        res = []
        temp = []
        for w, h in self.RESOLUTIONS:
            temp.append(w)
            temp.append(h)
        res.append(temp)
        for step in range(16, 257, 4):
            temp = []
            for w, h in self.RESOLUTIONS:
                temp.append(int(w / step))
                temp.append(int(h / step))
            res.append(temp)

        with open('file_input', "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in res:
                writer.writerow(line)
