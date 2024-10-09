import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
import json

import uuid

from PIL import Image

from services.jsonFiles import save_to_json, get_by_id, edit_by_id
from constants import ROI_SET_PATH

class RoiSetHeader(ctk.CTkFrame):
  # def __init__(self,id, name, image_path, roi_path, soil_points, image_type, *args, **kwargs):
  def __init__(self,id, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    self.id = id
    self.name = get_by_id(ROI_SET_PATH, id)["name"]
    # self.image_path = image_path
    # self.roi_path = roi_path
    # self.image_type = image_type
    # self.soil_points = soil_points
    
    self.configure(fg_color = "#23272e", corner_radius = 0)
    self.pack(side="top", fill="x", padx=0, pady=0)
    
    self.name_entry = ctk.CTkEntry(self, placeholder_text="Nombre", fg_color="#23272e", border_color="#23272e")
    self.name_entry.insert(0, self.name)
    self.name_entry.pack(side="left", padx=5, pady=5, fill='x', expand=True)
    
    save_img = ctk.CTkImage(light_image=Image.open("assets/icons/save.png"), dark_image=Image.open("assets/icons/save.png"), size=(20, 20))
    self.button = ctk.CTkButton(self, text="Guardar cambios", command=self.save, image=save_img, width=100)
    self.button.pack(side="right", padx=5, pady=5)
    
  def save(self):
    id = self.id
    name = self.name_entry.get()
    
    data = get_by_id(ROI_SET_PATH, id)
    data = {
      "id": str(uuid.uuid4()) if data == False else id,
      "name": name,
      "roi_path": self.master.roiSetRarImg.roi_path,
      "image_path": self.master.roiSetRarImg.img_path,
      "image_type": self.master.roiSetRarImg.img_type,
      "soil_data": json.dumps(self.master.select_soil),
      "updated_at": str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
      "created_at": data["created_at"],
    }
    if data == False:
      save_to_json(path=ROI_SET_PATH, data=data)
    else:
      edit_by_id(path=ROI_SET_PATH, id=id, data=data)
    
    self.display_save_message()
      
  def display_save_message(self):
    self.save_label = ctk.CTkLabel(self.master, text="Guardado", fg_color="#23272e", height=40, width=80)
    self.save_label.place(relx=0.5, rely=0.5, anchor="center")
    self.after(1500, self.save_label.destroy)