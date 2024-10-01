from read_roi import read_roi_zip

class roi_zip:
    def __init__(self, path):
        self.path = path

    def read(self):
        roi = read_roi_zip(self.path)
        return roi