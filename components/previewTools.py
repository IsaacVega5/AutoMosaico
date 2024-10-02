import customtkinter as ctk
from PIL import Image

class previewTools(ctk.CTkFrame):
  def __init__(self, parent, on_toggle_roi = None, on_toggle_remove_soil = None, on_save = None, **kwargs):
    super().__init__(parent, **kwargs)
    self.configure(fg_color="#000", corner_radius = 0)
    # Parámetros
    self.on_toggle_roi = on_toggle_roi
    self.on_toggle_remove_soil = on_toggle_remove_soil
    self.on_save = on_save
    
    # Componentes
    self.check_show_roi = ctk.BooleanVar(value=True)
    self.preview_roi = ctk.CTkCheckBox(self, text="Mostrar ROIs", variable=self.check_show_roi, command=self.handle_toggle_roi,onvalue=True, offvalue=False, height=5, font=("Consolas", 12), checkbox_height=16, checkbox_width=16, corner_radius= 0)
    self.preview_roi.pack(side="left", fill="x", padx=5, pady=5)
    
    self.check_remove_soil = ctk.BooleanVar(value=True)
    self.remove_soil = ctk.CTkCheckBox(self, text="Quitar suelo",variable=self.check_remove_soil,command=self.handle_toggle_remove_soil, onvalue=True, offvalue=False, height=5, font=("Consolas", 12), checkbox_height=16, checkbox_width=16, corner_radius= 0)
    self.remove_soil.pack(side="left", fill="x", padx=5, pady=5)
    
    save_img = ctk.CTkImage(light_image=Image.open("assets/icons/save.png"), dark_image=Image.open("assets/icons/save.png"), size=(15, 15))
    self.save_button = ctk.CTkButton(self, text="Guardar", image=save_img, command=self.save, height=16, width=50, font=("Consolas", 12), fg_color="#000", hover_color="#000")
    self.save_button.pack(side="right", fill="x", padx=0, pady=0)

  def get_roi(self):
    return self.check_show_roi.get()
  
  def get_remove_soil(self):
    return self.check_remove_soil.get()
  
  def handle_toggle_roi(self):
    if self.on_toggle_roi is not None:
      self.on_toggle_roi(value=self.check_show_roi.get())
  
  def handle_toggle_remove_soil(self):
    if self.on_toggle_remove_soil is not None:
      self.on_toggle_remove_soil()
  
  def save(self):
    if self.on_save is not None:
      self.on_save()