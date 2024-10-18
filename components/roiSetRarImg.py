import tkinter as tk
import customtkinter as ctk
from CTkToolTip import CTkToolTip
from CTkTable import CTkTable
from PIL import Image
from read_roi import read_roi_zip

from views.previewRoi import previewRoi
from classes.mosaico import Mosaico
from utils import get_resize_size, get_name_full_from_path, ellipsis_text, get_new_size

from constants import IMG_TYPES

class RoiSetRarImg(ctk.CTkFrame):
  def __init__(self, img_path, roi_path,img_type, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    self.img_path = img_path
    self.roi_path = roi_path
    self.img_type = img_type
    
    self.pack(side="top", fill="both", expand=True)
    
    # Imagen
    self.img_frame = ctk.CTkFrame(self)
    self.img_frame.grid(row=0, column=0, padx=0, pady=0)
    
    img_name = get_name_full_from_path(self.img_path)
    self.path_img_entry = ctk.CTkEntry(self.img_frame, width=175)
    self.path_img_entry.insert(0, self.img_path)
    self.path_img_entry.configure(state="readonly")
    self.path_img_entry.grid(row=0, column=0, padx=(5,1), pady=(0,2))
    
    self.edit_img_button = ctk.CTkButton(self.img_frame,width=15, text="", command=self.edit_img, image=ctk.CTkImage(light_image=Image.open("assets/icons/edit.png"), dark_image=Image.open("assets/icons/edit.png"), size=(20, 20)))
    self.edit_img_button.grid(row=0, column=1, padx=(1,5), pady=(0,2))
    
    self.img = Mosaico(self.img_path, self.img_type)
    self.preview_img_size = (210, 75)
    img_width, img_height, _ = get_new_size(self.img.size(), self.preview_img_size)
    
    self.image = ctk.CTkImage(light_image=self.img.img,
                              dark_image=self.img.img,
                              size=(img_width, img_height))
    
    self.label = ctk.CTkLabel(self.img_frame, image=self.image, text="", bg_color="#23272e", width=self.preview_img_size[0], height=self.preview_img_size[1])
    self.label.grid(row=1, column=0, padx=5, pady=2, columnspan=2)
    
    self.name_tooltip = CTkToolTip(self.path_img_entry, message = self.img_path, bg_color = "#23272e", corner_radius = 0)
    self.img_tooltip = CTkToolTip(self.label, message = img_name, bg_color = "#23272e", corner_radius = 0)
    
    self.select_type = ctk.CTkComboBox(self.img_frame, values=IMG_TYPES, width=175, state="readonly", command=self.change_type)
    self.select_type.set(self.img_type)
    self.select_type.grid(row=2, column=0, padx=(5,1), pady=2, columnspan=1)
    
    self.preview_btn =ctk.CTkButton(self.img_frame,width=15, text="", command=self.preview, image=ctk.CTkImage(light_image=Image.open("assets/icons/eye.png"), dark_image=Image.open("assets/icons/eye.png"), size=(20, 20)))
    self.preview_btn.grid(row=2, column=1, padx=(1,5), pady=2)
    
    self.preview_btn_tooltip = CTkToolTip(self.preview_btn, message = "Vista previa", bg_color = "#23272e", corner_radius = 0)
    
    # TableData
    self.table_frame = ctk.CTkFrame(self, bg_color="#23272e")
    self.table_frame.grid(row=0, column=1, padx=0, pady=(8,0))
    
    table_name = get_name_full_from_path(self.roi_path)
    self.roi_path_entry = ctk.CTkEntry(self.table_frame, width=296)
    self.roi_path_entry.insert(0, self.roi_path)
    self.roi_path_entry.configure(state="readonly")
    self.roi_path_entry.grid(row=0, column=0, padx=0, pady=0)
    self.roi_path_tooltip = CTkToolTip(self.roi_path_entry, message = self.roi_path, bg_color = "#23272e", corner_radius = 0)
    
    self.roi_path_edit_button = ctk.CTkButton(self.table_frame, text="", width=20, command=self.edit_roi, image=ctk.CTkImage(light_image=Image.open("assets/icons/edit.png"), dark_image=Image.open("assets/icons/edit.png"), size=(20, 20)))
    self.roi_path_edit_button.grid(row=0, column=1, padx=(2,0), pady=0)
    
    roi = read_roi_zip(self.roi_path)
    values = [['Nombre', 'Vertices X', 'Vertices Y']]
    for name in list(roi)[:3]:
      values.append([name, ellipsis_text(str(roi[name]['x']).replace("[", "").replace("]", ""), 20), 
                     ellipsis_text(str(roi[name]['y']).replace("[", "").replace("]", ""), 20)])
      
    self.table = CTkTable(master=self.table_frame, column=3, row=4, values=values, width=10, colors=["#282c34", "#282c34"], hover_color='#404754', header_color="#23272e", padx=0, pady=0, font=("Roboto", 11))
    self.table.grid(row=1, column=0, padx=0, pady=5, columnspan=2)
    self.table_tooltip = CTkToolTip(self.table, message = table_name, bg_color = "#23272e", corner_radius = 0)
  
  def change_type(self, value):
    self.img_type = value
    self.img = Mosaico(self.img_path, value)
    img_width, img_height, _ = get_new_size(self.img.size(), self.preview_img_size)
    self.image = ctk.CTkImage(light_image=self.img.img,
                              dark_image=self.img.img,
                              size=(img_width, img_height))
    self.label.configure(image=self.image)
    self.master.master.master.master.type = value
    
  def edit_img(self):
    file_path = tk.filedialog.askopenfilename(filetypes=(("Imágenes", "*.png;*.jpg;*.tif;*.tiff"),))
    if file_path is None or file_path == "" : return
    
    self.img_path = file_path
    self.master.master.master.master.img = self.img_path
    
    self.path_img_entry.configure(state="normal")
    self.path_img_entry.delete(0, ctk.END)
    self.path_img_entry.insert(0, self.img_path)
    self.path_img_entry.configure(state="readonly")
    
    self.img = Mosaico(self.img_path, self.img_type)
    img_height, img_width = get_resize_size(self.img, 210)
    self.image = ctk.CTkImage(light_image=self.img.img,
                              dark_image=self.img.img,
                              size=(img_width, img_height))
    self.label.configure(image=self.image)
    
    self.name_tooltip.configure(message = self.img_path)
    name = get_name_full_from_path(self.img_path)
    self.img_tooltip.configure(message = name)
    
  def edit_roi(self):
    file_path = tk.filedialog.askopenfilename(filetypes=(("Archivo zip", "*.zip"),))
    if file_path is None or file_path == "" : return
    
    self.roi_path = file_path
    self.master.master.master.master.roi = self.roi_path
    
    self.roi_path_entry.configure(state="normal")
    self.roi_path_entry.delete(0, ctk.END)
    self.roi_path_entry.insert(0, self.roi_path)
    self.roi_path_entry.configure(state="readonly")
    
    roi = read_roi_zip(self.roi_path)
    values = [['Nombre', 'Vertices X', 'Vertices Y']]
    for name in list(roi)[:3]:
      values.append([name, ellipsis_text(str(roi[name]['x']).replace("[", "").replace("]", ""), 20), 
                     ellipsis_text(str(roi[name]['y']).replace("[", "").replace("]", ""), 20)])
    self.table.update_values(values)
    
    self.roi_path_tooltip.configure(message = self.roi_path)
    self.table_tooltip.configure(message = get_name_full_from_path(self.roi_path))
    
  def preview(self):
    preview = previewRoi(
      img_path=self.img_path, 
      roi_path=self.roi_path, 
      type = self.img_type, 
      origin = True, 
      original_img_path = self.img_path,
      soil=self.master.master.master.master.select_soil)
  
    preview.after(250, preview.lift)
    