import ini


class Config:
    filename: str
    data: dict

    def __init__(self, filename: str, data: dict = None):
        self.filename = filename

        if data is not None:
            self.data = data

    def get(self, section: str, key: str) -> str:
        return self.data[section][key]

    def set(self, section: str, key: str, value: object):
        self.data[section][key] = value

    def read(self):
        with open(self.filename, 'r', encoding='utf-8') as fp:
            self.data = ini.parse(fp.read())

    def write(self):
        with open(self.filename, 'w', encoding='utf-8') as fp:
            fp.write(ini.stringify(self.data))
