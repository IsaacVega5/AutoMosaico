import customtkinter as ctk
import types
from CTkToolTip import CTkToolTip
from PIL import Image

from utils import get_name_full_from_path
from classes.mosaico import Mosaico
from constants import IMG_TYPES

from views.previewRoi import previewRoi
from components.MessageBox import warning

class ImageSelected(ctk.CTkFrame):
  def __init__(self, image_path, type, index, soil_data = None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.configure(fg_color = "#23272e", corner_radius = 0)
    
    self.image_path = image_path
    self.name = get_name_full_from_path(self.image_path)
    self.type = type
    self.index = index
    self.soil_data = soil_data

    cut_name = self.name if len(self.name) < 20 else self.name[:20] + "..."
    self.label_name = ctk.CTkLabel(self, text=cut_name, height=20)
    self.label_name.grid(row=0, column=0, columnspan=2, padx=(5,0), pady=5)
    self.label_name_tooltip = CTkToolTip(self.label_name, message = self.name, bg_color = "#23272e", corner_radius = 0)
    
    self.image = Mosaico(self.image_path, self.type)
    self.image = ctk.CTkImage(light_image=self.image.img,
                              dark_image=self.image.img,
                              size=(150, 100))
    
    self.label_img = ctk.CTkLabel(self, image=self.image, text="")
    self.label_img.grid(row=1, column=0,columnspan=2, padx=(0,2), pady=1)
    self.label_img_tooltip = CTkToolTip(self.label_img, message = self.image_path, bg_color = "#23272e", corner_radius = 0)
    
    self.select_type = ctk.CTkComboBox(self, values=IMG_TYPES, state="readonly", command=self.change_type, width=150)
    self.select_type.set(self.type)
    self.select_type.grid(row=2, column=0, columnspan=2, padx=0, pady=1)
    
    self.eye_icon = ctk.CTkImage(light_image=Image.open("assets/icons/eye.png"), dark_image=Image.open("assets/icons/eye.png"), size=(20, 20))
    self.preview_button = ctk.CTkButton(self, text="Previsualizar", command=self.preview, image=self.eye_icon, width=110)
    self.preview_button.grid(row=3, column=0, padx=(5,2), pady=2)
    
    self.trash_icon = ctk.CTkImage(light_image=Image.open("assets/icons/trash.png"), dark_image=Image.open("assets/icons/trash.png"), size=(20, 20))
    self.delete_button = ctk.CTkButton(self, text="", command=self.delete, image=self.trash_icon, width=25, fg_color="#fa5252", hover_color="#ff6a53")
    self.delete_button.grid(row=3, column=1, padx=(1,4), pady=2)
    
    
  def change_type(self, value):
    self.type = value
    
    self.image = Mosaico(self.image_path, self.type)
    self.image = ctk.CTkImage(light_image=self.image.img,
                              dark_image=self.image.img,
                              size=(150, 100))
    self.label_img.configure(image=self.image)
    
    self.master.master.master.master.master.change_img_type_by_index(self.index, self.type)
    
  def preview(self):
    preview = previewRoi(
        img_path=self.image_path, 
        roi_path=self.master.master.master.master.master.roi, 
        type = self.type,
        original_img_path = self.master.master.master.master.master.img,
        soil=self.soil_data())

    preview.after(250, preview.lift)
  
  def delete(self):
    alert = warning(title="Eliminar imagen", message="¿Seguro/a que desea eliminar esta imagen", option_1="Eliminar", option_2="Cancelar")
    if alert.get() == "Cancelar":
      return
    
    self.master.master.master.master.master.delete_img_by_index(self.index)