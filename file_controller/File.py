class File:
    file = None
    callback = None

    def __init__(self, f: None, callback=None):
        self.file = f
        self.callback = callback

    def __del__(self):
        self.file.close()

    def read(self):
        print('do read')
        return str(self.file.read())

    def close(self):
        self.file.close()


if __name__ == '__main__':
    file = File(f=open('../configs/settings.py', 'rb'))
    print(dir(open('../configs/settings.py', 'rb')))
