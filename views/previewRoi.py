import customtkinter as ctk
import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from CTkTable import CTkTable
from PIL import  Image, ImageTk
import cv2
import numpy as np
from read_roi import read_roi_zip
import os

from components.MessageBox import check
from components.previewTools import previewTools

from classes.mosaico import Mosaico
from classes.roi import ROI

from constants import SOIL_MASK_TYPE
from utils import get_new_size, get_resize_size, resize_ratio, order_roi_zip
from services.process import values_from_rgb_img, gen_masked_img, values_from_tif_img, get_max_hue

w_height, w_width = 1500, 1500

class previewRoi(ctk.CTkToplevel):
  def __init__(self, img_path, roi_path, type = 'RGB', origin = False, original_img_path = None, soil = None, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.after(250, lambda: self.iconbitmap('assets/map.ico'))
    self.roi_path = roi_path
    self.type = type
    self.origin = origin
    self.original_img_path = original_img_path
    self.selected_roi = None
    self.img_path = img_path
    self.soil = soil
    self.scale = 1
    
    self.img_origin_roi = Image.open(self.original_img_path)
    self.title(f'ROI Preview - {type} - {img_path}')
    
    self.img = Mosaico(img_path, type)
    
    #Calculamos el ratio antes de ajustar dimensiones
    if self.origin:
      self.ratio = 1
    else:
      self.ratio = self.img.resize_ratio(self.img_origin_roi)
    
    self.soil_mask = None
    to_draw = self.img.img
    if soil != None and soil['type'] == SOIL_MASK_TYPE[0]:
      if soil['value'] is not None and soil['value'][0] is not None and soil['value'][1] is not None:
        new_soil = [[ int(value * self.ratio) for value in values ] for values in soil['value']] # <- Ajustamos las coordenadas con el ratio
        
        to_draw, self.soil_mask= self.img.get_soilless_img(new_soil)
    elif soil != None and soil['type'] == SOIL_MASK_TYPE[1]:
      if len(soil['value']) > 0 and os.path.exists(soil['value']):
        to_draw, self.soil_mask = self.img.get_soilless_img(soil['value'])
    elif soil['type'] == SOIL_MASK_TYPE[2]:
      to_draw, self.soil_mask = self.img.get_soilless_img(soil['value'])
  
    max_width = self.winfo_screenwidth() * 0.8
    max_height = self.winfo_screenheight() * 0.8
    
    # ajustar dimensiones
    height, width, _ = get_new_size(self.img.size(), (max_height, max_width))
    self.img_height, self.img_width = get_resize_size(self.img, height)
    
    to_draw = to_draw.resize((self.img_width, self.img_height))
    self.img_tk = ImageTk.PhotoImage(to_draw)
    self.canvas = ctk.CTkCanvas(self, width=self.img_width, height=self.img_height)
    self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
    self.canvas.configure(highlightthickness=0)
    self.canvas.pack()
    
    self.update()
    self.check_show_roi = ctk.BooleanVar(value=True)  
    
    self.tools = previewTools(self, on_toggle_roi=self.draw_roi, on_toggle_remove_soil=self.update_img, on_save=self.save_img)
    self.tools.pack(fill=tk.X)
    
    if self.type == 'RGB':
      self.roi_color = {'normal':'yellow', 'active':'red'}
      values = [['Parc.','Name', 'Intensity', 'Hue', 'Saturation', 'Lightness', '*a', '*b', '*u', '*v', 'GA%', 'GGA%', 'CSI'],
                []]
    else:
      self.roi_color = {'normal':'black', 'active':'red'} if self.type == 'Termal' else {'normal':'yellow', 'active':'red'}
      values = [['Parc.', 'Name', 'Area', 'Mean', 'Min', 'Max'],
                []]
    
    self.table = CTkTable(master=self,column=len(values[0]), row=2, values=values, corner_radius=0, padx=0, pady=0, colors=["#282c34", "#282c34"], hover_color='#404754', header_color="#23272e")
    self.table.edit_column(1, width=200)
    self.table.pack(expand=True, fill="both")
    
    old_width, _ = self.img_origin_roi.size
    self.ratio = self.img_width / old_width
    
    # Agregar botones en canvas
    self.roi = read_roi_zip(self.roi_path)
    self.roi = order_roi_zip(self.roi)
    # self.draw_image()
    self.draw_roi(self.tools.get_roi())
    min_width = 800 if self.type == 'RGB' else 400
    window_width = self.img_width if self.img_width > min_width else min_width
    self.geometry(f"{window_width}x{self.img_height + 50 + 25}")
    self.resizable(False, False)
    self.canvas.bind("<MouseWheel>", self.on_scroll)
    self.canvas.bind("<B1-Motion>", self.on_move)
  
  def on_scroll(self, e : tk.EventType.MouseWheel):
    self.scale += e.delta / 120
    s_width, s_height = self.img_width * self.scale, self.img_height * self.scale
    if s_width <= 0 or s_height <= 0:
      return
    print(s_width, s_height)
    self.img_tk = ImageTk.PhotoImage(self.img.img.resize((int(s_width), int(s_height))))
    self.canvas.delete('all')
    self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)
    
    
    self.draw_roi(self.tools.get_roi() )
  
  def on_move(self, e : tk.EventType.Motion):
    print(e)
    self.canvas.scan_mark(e.x, e.y)
    self.canvas.scan_dragto(e.x, e.y, gain=1)
  
  def draw_roi(self, value = None):
    self.canvas.delete('all')
    self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)
    if not value:
      return
    for roi in self.roi.values():
      current_roi = ROI(roi)
      figure = current_roi.get_figure(self.ratio)
      
      btn = self.canvas.create_polygon(
        figure[0][0], figure[0][1], 
        figure[1][0], figure[1][1], 
        figure[2][0], figure[2][1], 
        figure[3][0], figure[3][1], 
        fill="",
        outline=self.roi_color['normal'],
        width=1
      )
    
      self.canvas.tag_bind(btn, "<Button-1>", lambda event, roi = current_roi, btn = btn: self.select_roi(event, roi, btn))
      self.canvas.tag_bind(btn, "<Enter>", lambda event, roi = current_roi, btn = btn: self.canvas.config(cursor="hand2"))
      self.canvas.tag_bind(btn, "<Leave>", lambda event, roi = current_roi, btn = btn: self.canvas.config(cursor=""))
  
  def select_roi (self,event, roi, btn):
    if self.selected_roi is not None: 
      try:
        self.canvas.itemconfig(self.selected_roi, outline=self.roi_color['normal'])
      except:
        pass
      
    try:  
      self.selected_roi = self.canvas.find_closest(event.x, event.y)[0]
      self.canvas.itemconfig(self.selected_roi, outline=self.roi_color['active'])
      
      self.process_roi(roi)
    except:
      try:
        self.canvas.itemconfig(self.selected_roi, outline=self.roi_color['normal'])
      except:
        pass
      self.selected_roi = None
  
  def process_roi(self, roi):
    img_origin = Image.open(self.original_img_path)
    img = Image.open(self.img_path)
    ratio = resize_ratio(img_origin, img)
    
    roi_zip = read_roi_zip(self.roi_path)
    roi_zip = order_roi_zip(roi_zip)
    row = list(roi_zip.keys()).index(roi.get_name()) + 1
    
    if self.type == 'RGB':
      figure = roi.get_figure(ratio)
      mask = None
      if self.soil_mask is not None and self.tools.get_remove_soil():
        mask = self.soil_mask
      try:
        values = [round(value, 4) if isinstance(value, float) else value for value in values_from_rgb_img(img, figure, mask)]
      except Exception as e: print(e)
      self.table.delete_row(1)
      self.table.add_row([row, roi.get_name()] + [f'{value:.4f}' if isinstance(value, (int, float)) else value for value in values])
    
    else :
      img = np.array(img) # <-- Convertimos la imagen en un matriz
      _, mask = gen_masked_img(img, roi, ratio)
      if self.soil_mask is not None and self.tools.get_remove_soil():
        soil_mask = np.where(self.soil_mask > 0, 1, 0)
        mask = np.where(mask > 0, 1, 0)
        mask = cv2.bitwise_and(mask, soil_mask)
      
      area, mean, max, min = values_from_tif_img(img, mask)
      self.table.delete_row(1)
      self.table.add_row([row, roi.get_name(), area, f'{mean:.4f}', f'{min:.4f}', f'{max:.4f}'])
  
  def update_img(self):
    if self.tools.get_remove_soil(): 
      img = self.img.soilless_img
    else:
      img = self.img.img
    img = img.resize((self.img_width, self.img_height))
    self.img_tk = ImageTk.PhotoImage(img)
    self.draw_roi( self.tools.get_roi() )
  
  def save_img(self):
    img_path = self.img.path
    save_path = asksaveasfilename(
      initialdir = os.path.dirname(img_path),
      title = "Select file",
      filetypes = (("jpg files","*.jpg"),("all files","*.*")),
      defaultextension = ".jpg"
    )
    if self.tools.get_remove_soil(): 
      img = self.img.soilless_img
    else:
      img = self.img.img
    img.save(save_path)
    msg = check(title="Exito", message=f"La imagen se guardó correctamente en:\n{save_path}", option_1 = "Aceptar", option_2 = "Abrir")
    if msg.get() == "Abrir":
      os.startfile(save_path)
    