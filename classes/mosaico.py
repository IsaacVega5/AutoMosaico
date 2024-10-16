from PIL import Image, ImageDraw
import cv2
import numpy as np
from customtkinter import CTkImage
from read_roi import read_roi_zip
from classes.roi import ROI
import math

class Mosaico():
  def __init__(self, path, type = 'RGB'):
    self.path = path
    self.type = type
    
    if self.type == 'Termal':
      self.img = self.termal()
    elif self.type == 'OCN':
      self.img = self.ocn()
    elif self.type == 'RGN':
      self.img = self.rgn()
    else:
      self.img = self.rgb()
    self.soilless_img = None
    
  def __str__(self):
    return self.path, self.type
  
  def __repr__(self):
    return self.path, self.type
  
  def rgb(self):
    return Image.open(self.path)
  
  def size(self):
    height, width = self.img.size
    size = (height, width)
    return size
  
  def termal(self):
    img = Image.open(self.path).convert('L')
    img = np.array(img)
    img = cv2.convertScaleAbs(img, alpha=3, beta=1)
    
    color_map = cv2.COLORMAP_JET
    img_color = cv2.applyColorMap(img, color_map)
    
    im_pillow = Image.fromarray(cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB))
    return im_pillow
  
  def ocn(self):
    img = Image.open(self.path)
    img_array = np.array(img)
    img_normalized = cv2.normalize(img_array, None, -255, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    img = Image.fromarray(img_normalized)
    return img.convert('RGB')

  def rgn(self):
    img = Image.open(self.path)
    img_array = np.array(img)
    img_normalized = cv2.normalize(img_array, None, -255, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    img = Image.fromarray(img_normalized)
    return img.convert('RGB')
  
  def draw_roi(self, roi_path, ratio):
    img = self.img
    roi_zip = read_roi_zip(roi_path)
    
    for roi in roi_zip:
      roi = ROI(roi_zip[roi])
      figure = roi.get_figure(ratio=ratio)
      
      # figure = resize_figure(figure, ratio)
      
      width = math.floor(4 * ratio)
      img_draw = ImageDraw.Draw(img)
      img_draw.line(
        (figure[0], figure[1], figure[2], figure[3], figure[0]),
        fill = 'black' if self.type == 'Termal' else 'yellow', 
        width = width
      )
    return img
  
  def resize_ratio(self, img_to_compare):
    original_size = img_to_compare.size
    new_size = self.img.size
    
    return new_size[0] / original_size[0]
  
  def get_soilless_img(self, soil_points):
    if isinstance(soil_points, str):
      mask = Image.open(soil_points)
      mask = np.array(mask)
      mask = cv2.resize(mask, self.img.size)
      mask = np.where(mask > 0, 1, 0)
      
    else:    
      mask = self.generate_mask_from_tile(soil_points)
      
    if len(mask.shape) == 3:
      mask = mask[:, :, 0]
    
    image_array = np.array(self.img)
    masked_img = np.zeros(image_array.shape, dtype=np.uint8)
    masked_img[:, :, 0] = image_array[:, :, 0] * mask
    masked_img[:, :, 1] = image_array[:, :, 1] * mask
    masked_img[:, :, 2] = image_array[:, :, 2] * mask
    self.soilless_img = Image.fromarray(masked_img)
    return self.soilless_img, mask
  
  def generate_mask_from_tile(self, points):
    img_path = self.path
    
    x1, y1 = min(points[0][0], points[1][0]), min(points[0][1], points[1][1])
    x2, y2 = max(points[0][0], points[1][0]), max(points[0][1], points[1][1])
    
    aerial_image = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED) # <- utilizamos este método para evitar problemas con caracteres especiales
    img_matrix = np.array(aerial_image)
    soil_image = img_matrix[int(y1):int(y2), int(x1):int(x2)] # <- este es el problema, no se puede leer la imagen si no se le indica el formato RGB, por eso se hace un reshape y se le indica que es RGBA, para que el procesamiento de la imagen sea correcto. Por ejemplo: img_matrix[y1:y2, x1:x2]

    soil_image_tiled = np.tile(soil_image, (aerial_image.shape[0] // soil_image.shape[0] + 1, aerial_image.shape[1] // soil_image.shape[1] + 1, 1))
    soil_image_tiled = soil_image_tiled[:aerial_image.shape[0], :aerial_image.shape[1], :]

    hsv_aereal = cv2.cvtColor(aerial_image, cv2.COLOR_RGB2HSV)

    hsv_tiled = cv2.cvtColor(soil_image_tiled, cv2.COLOR_RGB2HSV)
    hsv_tiled = cv2.GaussianBlur(hsv_tiled, (5, 5), 0)
    
    diff = cv2.absdiff(hsv_aereal, hsv_tiled)

    umbral = 1 if np.mean(diff) < 20 else 10

    mask = np.where(diff < umbral, 0, 1).astype(np.uint8)
    
    return mask