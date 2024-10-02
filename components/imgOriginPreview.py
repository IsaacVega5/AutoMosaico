import tkinter as tk
import customtkinter as ctk
from PIL import Image
import numpy as np

from classes.mosaico import Mosaico
from constants import IMG_TYPES
from utils import get_resize_size

from views.previewRoi import previewRoi

class ImgOriginPreview(ctk.CTkFrame):
  def __init__(self, src, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.configure(fg_color = "#23272e", corner_radius = 0)
    self.grid(row=5, column=0, columnspan=2, padx=10, pady=(5,0), sticky="nsew")

    self.type = IMG_TYPES[0]
    ratio = 1
    self.frame_width = 333
    self.src = src
    self.img = Mosaico(src, self.type)
    img_height, img_width = get_resize_size(self.img, self.frame_width)
    self.image = ctk.CTkImage(light_image=self.img.img, dark_image=self.img.img, size=(img_width, img_height))
    self.label = ctk.CTkLabel(self, text="", image=self.image)
    
    self.label.pack(fill="both", expand=True, padx=0, pady=(0,4))
    
    self.btn_frame = ctk.CTkFrame(self, fg_color="#23272e", bg_color="#23272e", corner_radius=0, width=self.frame_width)
    self.btn_frame.pack(fill="both", expand=True, padx=0, pady=0)
    
    self.select_type = ctk.CTkComboBox(self.btn_frame, values=IMG_TYPES, command=self.change_type, width=200, state="readonly")
    self.select_type.set(IMG_TYPES[0])
    self.select_type.grid(row=0, column=0, padx=(0, 2), pady=0)

    self.preview_img = ctk.CTkImage(light_image=Image.open("assets/icons/eye.png"), dark_image=Image.open("assets/icons/eye.png"), size=(20, 20))
    self.preview_btn = ctk.CTkButton(self.btn_frame, text="Previsualizar", command=self.preview, width=130, image=self.preview_img)
    self.preview_btn.grid(row=0, column=1, padx=(2, 0), pady=0)
    
    
  
  def change_type(self, value):
    self.type = value
    self.img = Mosaico(self.src, self.type)
    img_height, img_width = get_resize_size(self.img, self.frame_width)
    self.image = ctk.CTkImage(light_image=self.img.img, dark_image=self.img.img, size=(img_width, img_height))
    self.label.configure(image=self.image)
    self.master.master.type = value
  
  def preview(self):
    roi_path = self.master.master.roi_path
    
    if roi_path is None: 
      self.master.master.label.configure(text_color="#fa5252") 
      self.master.master.shake()
      return
    
    soil_points = None if self.master.master.selected_soil[0] == None else self.master.master.selected_soil
    preview_window = previewRoi(self.src, roi_path, type = self.type, origin = True, original_img_path = self.src, soil_points = soil_points)
    preview_window.after(250, preview_window.lift)