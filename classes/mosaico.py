from PIL import Image, ImageDraw
import cv2
import numpy as np
from customtkinter import CTkImage
from read_roi import read_roi_zip
from classes.roi import ROI
import math 
from services.process import generate_mask_from_tile

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
    mask = generate_mask_from_tile(self.path, soil_points)
    image_array = np.array(self.img)
    masked_img = np.zeros(image_array.shape, dtype=np.uint8)
    masked_img[:, :, 0] = image_array[:, :, 0] * mask[:, :, 0]
    masked_img[:, :, 1] = image_array[:, :, 1] * mask[:, :, 0]
    masked_img[:, :, 2] = image_array[:, :, 2] * mask[:, :, 0]
    self.soilless_img = Image.fromarray(masked_img)
    return self.soilless_img, mask