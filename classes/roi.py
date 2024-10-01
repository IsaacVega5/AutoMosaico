from read_roi import read_roi_file

class ROI:
  def __init__(self, object):
    self.data = object

  def get_name(self):
    name = self.data['name']
    return name
  
  def coords(self):
    x = self.data['x']
    y = self.data['y']
    
    return x, y
  
  def get_figure(self, ratio = 1):
    figure = (
      (self.data['x'][0] * ratio, self.data['y'][0] * ratio),
      (self.data['x'][1] * ratio, self.data['y'][1] * ratio),
      (self.data['x'][2] * ratio, self.data['y'][2] * ratio),
      (self.data['x'][3] * ratio, self.data['y'][3] * ratio),
    )
    return figure
  
  def get_vertices(self, ratio = 1):
    vertices = {
      'x': [self.data['x'][0] * ratio, self.data['x'][1] * ratio, self.data['x'][2] * ratio, self.data['x'][3] * ratio],
      'y': [self.data['y'][0] * ratio, self.data['y'][1] * ratio, self.data['y'][2] * ratio, self.data['y'][3] * ratio]
    }
    return vertices