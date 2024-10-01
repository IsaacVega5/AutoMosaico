import customtkinter as ctk
from PIL import Image

from components.MessageBox import warning

from controllers.roiSetController import get_by_id, delete_by_id

class RoiSetElement(ctk.CTkFrame):
  def __init__(self, id, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.configure(fg_color="#23272e", corner_radius = 0)
    self.data = get_by_id(id)
    
    self.image_frame = ctk.CTkFrame(self, fg_color="#23272e", width=40, height=40)
    self.image_frame.grid(row=0, column=0, padx=0, pady=0)
    
    self.data_frame = ctk.CTkButton(self, fg_color="#23272e", hover_color="#23272e", command=self.on_click, text="", width=350)
    self.data_frame.grid(row=0, column=1, padx=0, pady=0, sticky="w")
    
    self.date_frame = ctk.CTkFrame(self, fg_color="#23272e")
    self.date_frame.grid(row=0, column=2, padx=0, pady=0, sticky="e")
    
    self.btn_frame = ctk.CTkFrame(self, fg_color="#23272e", width=30, height=30)
    self.btn_frame.grid(row=0, column=3, padx=(10,0), pady=0, sticky="e")
    
    self.roi_icon = Image.open("assets/icons/rar-file.png")
    self.roi_icon = ctk.CTkImage(light_image=self.roi_icon, dark_image=self.roi_icon, size=(40, 40))
    self.label_img = ctk.CTkButton(self.image_frame, image=self.roi_icon, text="", bg_color="#23272e", fg_color="#23272e", hover_color="#23272e", command=self.on_click, width=40, height=40)
    self.label_img.pack()
    
    self.cut_name = self.data["name"]
    self.cut_name = self.cut_name[:45] + "..." if len(self.data["name"]) > 45 else self.data["name"]
    self.name = ctk.CTkButton(self.data_frame, text=self.cut_name, font=("Arial", 13, "bold"), command=self.on_click, fg_color="#23272e", hover_color="#23272e", anchor="w", height=20).grid(row=1, column=0, padx=0, pady=0, sticky="w")
    self.type = ctk.CTkButton(self.data_frame, text=self.data["image_type"], font=("Arial", 11, "normal"), command=self.on_click, fg_color="#23272e", hover_color="#23272e", anchor="w", height=5).grid(row=2, column=0, padx=(5,0), pady=0, sticky="w")
    
    self.updated_date = ctk.CTkLabel(self.date_frame, text=self.data["updated_at"], font=("Arial", 11, "normal"), anchor="w", height=5).grid(row=0, column=0, padx=0, pady=0, sticky="w")
    self.creation_date = ctk.CTkLabel(self.date_frame, text=self.data["created_at"], font=("Arial", 11, "normal"), anchor="w", height=5).grid(row=2, column=0, padx=0, pady=0, sticky="w")
    
    delete_icon = Image.open("assets/icons/trash-red.png")
    delete_icon = ctk.CTkImage(light_image=delete_icon, dark_image=delete_icon, size=(15, 15))
    self.delete_btn = ctk.CTkButton(self.btn_frame, text="", fg_color="#23272e", hover_color="#23272e", command=self.delete, width=30, height=30, image=delete_icon)
    self.delete_btn.grid(row=0, column=0, padx=0, pady=0)
    
  
  def on_click(self):
    self.master.master.master.master.master.master.view_roi_set(self.data["id"])
    
  
  def delete(self):
    alert = warning(title="Eliminar imagen", message="¿Seguro/a que desea eliminar este Roi set?", option_1="Eliminar", option_2="Cancelar")
    if alert.get() == "Cancelar":
      return
    
    delete_by_id(self.data["id"])
    self.master.master.list_frame_render()