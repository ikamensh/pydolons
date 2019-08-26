from os import path, mkdir, environ, name as osname
from datetime import datetime
from json import dumps, loads
from copy import copy

DEFAULT_CONFIG = {
    'window':{
        'resolution':{'width':1366,
                      'height':768},
        'fullscreen':True,
    }
}

DEFAULT_SIZE_CONFIG = {
    'window':{
        'resolution':{'width':1024,
                      'height':768},
        'fullscreen':False
    }
}


class UserConfig(object):
    def __init__(self):
        if osname == 'nt':
            self.home = path.join('c:\\', environ['HOMEPATH'])
        else:
            self.home = environ['HOME']
        self.config_dir = path.join(self.home, 'Pydolons-dev')
        self.dev_size = None

    @property
    def default_config(self):
        global DEFAULT_CONFIG
        return dumps(DEFAULT_CONFIG)

    def readSetting(self):
        config = path.join(self.config_dir, 'config.json')
        self.updateOldConfig(config)
        if path.exists(self.config_dir):
            if path.isdir(self.config_dir):
                if path.exists(config):
                    with open(config, 'r') as f:
                        raw_config = f.read()
                    self.read_config = loads(raw_config)
                else:
                    self.create_default()
            else:
                self.create_default()
        else:
            self.create_default()

    def saveSetting(self):
        config = path.join(self.config_dir, 'config.json')
        raw_config = dumps(self.read_config)
        with open(config, 'w') as f:
            f.write(raw_config)

    def create_default(self):
        global DEFAULT_CONFIG
        if not path.exists(self.config_dir):
            mkdir(self.config_dir)
        config = path.join(self.config_dir, 'config.json')
        raw_config = self.default_config
        self.read_config = copy(DEFAULT_CONFIG)
        with open(config, 'w') as f:
            f.write(raw_config)

    def setSize(self, size):
        self.read_config['window']['resolution']['width'] = size[0]
        self.read_config['window']['resolution']['height'] = size[1]

    def updateOldConfig(self, config):
        new_dt = datetime.fromtimestamp(1566853815.7816741)
        config_dt = datetime.fromtimestamp(path.getmtime(config))
        if new_dt >= config_dt:
            self.create_default()
# if __name__ == '__main__':
#     cfg = Settings()
#     cfg.readSetting()
#     print(cfg.read_config)
#     cfg.saveSetting(DEFAULT_SIZE_CONFIG)
#     print(cfg.read_config)

