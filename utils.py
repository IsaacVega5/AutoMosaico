import math

def calc_dimension_ratio(img_dim_1, img_dim_2, set_dim):
  return img_dim_2 * set_dim // img_dim_1

def get_resize_size(img, resize):
    img_height, img_width = img.size()
    
    if img_height > img_width:
      img_height = calc_dimension_ratio(img_height, img_width, resize)
      img_width = resize
    else:
      img_width = calc_dimension_ratio(img_width, img_height, resize)
      img_height = resize
      
    return img_height, img_width
  
def get_name_full_from_path(path):
  return path.split("/")[-1]

def get_name_from_path(path):
  name = path.split('/')[-1]
  slices = name.split(".")
  return ".".join(slices[0:-1])
  
def replace_dot_with_comma(number):
  return number.replace('.', ',')

def resize_ratio(img_or, img_new):
  original_size = img_or.size
  new_size = img_new.size
  
  return new_size[0] / original_size[0]

def order_roi_zip(roi_zip):
  return {k: roi_zip[k] for k in sorted(roi_zip.keys())}


def get_min_and_max(figure):
  minX = min(figure[0][0], figure[1][0], figure[2][0], figure[3][0])
  minY = min(figure[0][1], figure[1][1], figure[2][1], figure[3][1])
  maxX = max(figure[0][0], figure[1][0], figure[2][0], figure[3][0])
  maxY = max(figure[0][1], figure[1][1], figure[2][1], figure[3][1])
  
  minX = math.floor(minX)
  minY = math.floor(minY)
  maxX = math.ceil(maxX)
  maxY = math.ceil(maxY)
  
  return minX, minY, maxX, maxY

def format_number(number, cifra = 3):
  return str(number).zfill(cifra)

def get_new_size(image_size, new_size):
  o_ancho, o_alto = image_size
  n_ancho, n_alto = new_size
  
  resize_ratio = min(n_alto/o_alto, n_ancho/o_ancho)
  new_width = int(o_ancho * resize_ratio)
  new_height = int(o_alto * resize_ratio)
  return new_width, new_height, resize_ratio

def ellipsis_text(text, width):
  if len(text) > width:
    return text[:width - 3] + '...'
  return text