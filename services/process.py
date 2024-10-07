import cv2 
import numpy as np
from PIL import Image
from read_roi import read_roi_zip
from colormath.color_objects import XYZColor, sRGBColor
from colormath.color_conversions import convert_color
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

from classes.mosaico import Mosaico
from classes.roi import ROI
from services.excel import *
from constants import *
from utils import get_name_from_path, resize_ratio, order_roi_zip, get_min_and_max, get_name_full_from_path

from components.MessageBox import error


def gen_masked_img(img, roi, ratio):
  mask = np.zeros_like(img)
  
  figure = roi.get_figure(ratio)
  figure = np.array([figure], dtype=np.int32)
  
  cv2.fillPoly(mask, figure, (255, 255, 255))
  
  masked_img = cv2.bitwise_and(img, mask)
  return masked_img, mask

def generate_excel( roi_path, img_roi_path, img_list):
  
  roi_zip = read_roi_zip(roi_path)
  roi_zip = order_roi_zip(roi_zip)
  img_origin = Image.open(img_roi_path)
  
  try:
    workbook, destiny_path = create_workbook()
  except:
    return None
  
  if destiny_path is None:
    return
  
  
  # Iteramos entre las imágenes
  cont = 0
  for item in img_list:    
    type = IMG_TYPES[item['type']]
    sheet_name = f'{type} - {get_name_from_path(item["path"])}'
    worksheet = add_worksheet(workbook, sheet_name)
    
    img = Image.open(item['path'])
    ratio = resize_ratio(img_origin, img)
    
    if type == 'Termal' or type == 'OCN' or type == 'RGN':
      add_table_headers(worksheet, ['Parc.', 'Name', 'Area', 'Mean', 'Min', 'Max'])
    else:
      add_table_headers(worksheet, ['Parc.','Name', 'Intensity', 'Hue', 'Saturation', 'Lightness', '*a', '*b', '*u', '*v', 'GA%', 'GGA%', 'CSI'])
    
    row = 2
    for name in roi_zip:
    
      roi = ROI(roi_zip[name]) # <-- Obtenemos el ROI
      
      if type == 'Termal' or type == 'OCN' or type == 'RGN':
        img = np.array(img) # <-- Convertimos la imagen en un arreglo
        masked_img, mask = gen_masked_img(img, roi, ratio)
        
        area, mean, max, min = values_from_tif_img(img, mask)
        add_table_row(worksheet, row, [row-1, name, area, mean, min, max])
        
      else:
        figure = roi.get_figure(ratio)
        values = values_from_rgb_img(img, figure)
        add_table_row(worksheet, row, [row-1, name, *values])
        
      row += 1
      cont += 1
  
  saved = False
  while not saved:
    try:
      save_workbook(workbook)
      saved = True
    except Exception as e:
      msg = error(title='Error', message=f'Error al guardar el archivo Excel. \n\nVerifique que no este abierto otro archivo con el mismo nombre.\nsi el error persiste contacte con el administrador.', option_1 = "Reintentar", option_2 = "Cancelar")
      if msg.get() != 'Reintentar':
        return None
    
  
  return destiny_path

def process(roi_path, img_roi_path, img_list, progress_bar = None, soil = None):
  roi_zip = read_roi_zip(roi_path)
  roi_zip = order_roi_zip(roi_zip)
  
  results_queue = multiprocessing.Queue()
  
  img_args = [(index,img, img_roi_path, roi_zip, results_queue, soil) for index, img in enumerate(img_list)]
  
  results = []
  
  cores = multiprocessing.cpu_count()
  progress_bar.set_max(len(img_args))
  progress_bar.set(0)
  progress_bar.console_clear()
  progress_bar.console_log('Cargando imágenes...')
  with ThreadPoolExecutor(max_workers=cores) as executor:
    futures = []
    for img in img_args:
      future = executor.submit(process_img, img)
      future.add_done_callback(
        lambda f, progress_bar=progress_bar, img_path = img[1]['path']: 
          progress_bar.step(text = f'{get_name_full_from_path(img_path)}\n')
      )
      futures.append(future)
      
    for future in futures:
      future.result()
  
  results = []
  for _ in range (len(img_list)):
    result = results_queue.get()
    results.append(result)

    
  results.sort(key=lambda x: x['index'])
    
  return results

def process_img(img_args):
  index, image, img_origin_path, roi_zip, results_queue, soil = img_args
  img = Image.open(image['path'])
  type = image['type']
  img_origin = Image.open(img_origin_path)
  
  ratio = resize_ratio(img_origin, img)
  
  values = []
  mask = None
  if type == 'RGB' and soil is not None and soil[0] is not None:
    _, mask = Mosaico(image['path'], type).get_soilless_img(soil)
   
  for name in roi_zip:
    roi = ROI(roi_zip[name])
    try:
      if type == 'Termal' or type == 'OCN' or type == 'RGN':
          img = np.array(img)
          _, mask = gen_masked_img(img, roi, ratio)
          
          area, mean, max, min = values_from_tif_img(img, mask)
          values.append([roi.get_name(), area, mean, min, max])
      else:
          figure = roi.get_figure(ratio)
          values.append([roi.get_name(), *values_from_rgb_img(img, figure, mask)])
    except Exception as e:
      values = False
    
  result = {
      'index': index,
      'path': image['path'],
      'type': type,
      'values': values
  }
  results_queue.put(result)
  
  
def values_from_rgb_img(img, figure, soil_mask = None):
  minX, minY, maxX, maxY = get_min_and_max(figure)
  minHGA = MIN_H_GA
  maxHGA = MAX_H
  minSatGA = MIN_SAT / 100.0
  minHGGA = MIN_H_GGA

  R,G,B = 0, 0, 0
  count = 0
  countGA = 0
  countGGA = 0
  for y in range(minY, maxY):
    for x in range(minX, maxX):
      if soil_mask is not None:
        if soil_mask[y][x][0] == 0:
          continue
      r, g, b = img.getpixel((x, y))
      r *= INV_255
      g *= INV_255
      b *= INV_255
      
      hsi = RGB_to_HSI((r, g, b))
      
      R += r
      G += g
      B += b
      
      if (y >= figure[0][1] and y <= figure[2][1] and x >= figure[0][0] and x <= figure[2][0]):
        if (hsi[0] >= minHGA and hsi[0] <= maxHGA) :
          if (hsi[1] >= minSatGA ) :
            countGA += 1
            
            if (hsi[0] > minHGGA) :
              countGGA += 1
      
      count += 1
  if count == 0:
    return 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan'
  mean_rgb = (R/count, G/count, B/count)
  mean_hsi = RGB_to_HSI(mean_rgb)
  mean_rgb_255 = sRGBColor(mean_rgb[0], mean_rgb[1], mean_rgb[2], is_upscaled=False)

  cie_xyz = convert_color(mean_rgb_255, XYZColor, target_illuminant='d50')
  cie_xyz = (
      cie_xyz.get_value_tuple()[0],
      cie_xyz.get_value_tuple()[1],
      cie_xyz.get_value_tuple()[2]
  )

  lab = CIEXYZ_to_Lab(cie_xyz)
  luv = CIEXYZ_to_Luv(cie_xyz)

  ga = countGA/count
  gga = countGGA/count
  
  csi = ((ga - gga) / ga ) * 100 if ga != 0 else 'Nan'
  
  return mean_hsi[2], mean_hsi[0], mean_hsi[1], lab[0], lab[1], lab[2], luv[1], luv[2], ga, gga, csi
 

def values_from_tif_img(img, mask):
  values = img[mask != 0]
  values = values[~np.isnan(values)]
  
  area = int(len(values))
  mean = np.mean(values).item() if area != 0 else 'NaN'
  min = np.min(values).item() if area != 0 else 'NaN'
  max = np.max(values).item() if area != 0 else 'NaN'
  
  return area, mean, max, min

def RGB_to_HSI(rgb):
  M = 0
  m = 1
  maxI = -1
  I = 0
  H = 0
  S = 0
  
  M = max(rgb)
  m = min(rgb)
  maxI = rgb.index(M)
  
  chr = M - m
  if   chr  == 0 : H = 0
  elif maxI == 0 : H = ((rgb[1] - rgb[2]) / chr) % 6
  elif maxI == 1 : H = ((rgb[2] - rgb[0]) / chr) + 2
  elif maxI == 2 : H = ((rgb[0] - rgb[1]) / chr) + 4
  
  H = H * 60 
  
  I = (rgb[0] + rgb[1] + rgb[2]) / 3
  
  S = 0 if chr == 0 else 1 - m / I
  
  return ( H, S, I )

def RGB_to_CieXYZ(rgb):
  r = rgb[0] / 255
  g = rgb[1] / 255
  b = rgb[2] / 255
  
  # Matriz de transformación RGB a XYZ para el observador CIE 2° y el iluminante D65
  M = [[0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041]]
  
  # Aplicar la transformación lineal
  X = M[0][0] * r + M[0][1] * g + M[0][2] * b
  Y = M[1][0] * r + M[1][1] * g + M[1][2] * b
  Z = M[2][0] * r + M[2][1] * g + M[2][2] * b
  
  return (X, Y, Z)

def CIEXYZ_to_Lab(xyz):
  FXYZ = []
  
  for i in range(3):
    if xyz[i] > 0.008856:
      FXYZ.append(xyz[i] ** (1.0 / 3.0))
    else:
      FXYZ.append((7.787 * xyz[i]) + (16.0 / 116.0))
  
  L = (116.0 * FXYZ[1]) - 16.0
  a = 500.0 * (FXYZ[0] - FXYZ[1])
  b = 200.0 * (FXYZ[1] - FXYZ[2])
  
  return (L, a, b)

def CIEXYZ_to_Luv(xyz):
  u_n = 4 / (1 + 15 + 3)
  v_n = 9 / (1 + 15 + 3)
  denom = (xyz[0] + 15 * xyz[1] + 3 * xyz[2])
  
  L = 116 * (xyz[1] ** (1/3)) - 16
  U = 4 * xyz[0] / denom
  V = 9 * xyz[1] / denom
  
  U = 13 * L * (U - u_n)
  V = 13 * L * (V - v_n)
  
  return (L, U, V)

def get_max_hue(img, points):
  minX, minY = min(points[0][0], points[1][0]), min(points[0][1], points[1][1])
  maxX, maxY = max(points[0][0], points[1][0]), max(points[0][1], points[1][1])
  
  hue_list = []
  for y in range(minY, maxY):
    for x in range(minX, maxX):
      r, g, b = img.getpixel((x, y))
      r *= INV_255
      g *= INV_255
      b *= INV_255
      
      hsi = RGB_to_HSI((r, g, b))
      hue_list.append(hsi[0])
  
  media  = np.median(hue_list)
  srt = np.std(hue_list)
  umbral = media +srt
  print("MEDIA:", media)
  print("STD:", srt)
  print("UMBRAL:", umbral)
  print("HUE LIST", hue_list)
  
  filtered_list = [x for x in hue_list if x <= umbral]
  print("FILTERED LIST", filtered_list)
  return max(filtered_list)

def remove_hue_from_img(img, hue):
  for y in range(img.size[1]):
    for x in range(img.size[0]):
      r, g, b = img.getpixel((x, y))
      r *= INV_255
      g *= INV_255
      b *= INV_255
      
      hsi = RGB_to_HSI((r, g, b))
      if hsi[0] <= hue:
        img.putpixel((x, y), (0, 0, 0))
  
  return img

def RGB_to_HSI_matrix(rgb_matrix):
  hsi_matrix = np.zeros_like(rgb_matrix)
  
  for y in range(rgb_matrix.shape[0]):
    for x in range(rgb_matrix.shape[1]):
      r, g, b = rgb_matrix[y, x]
      r /= 255
      g /= 255
      b /= 255
      
      hsi = RGB_to_HSI((r, g, b))
      hsi_matrix[y, x] = hsi
  
  return hsi_matrix
