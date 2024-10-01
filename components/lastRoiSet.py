import customtkinter as ctk
from CTkToolTip import CTkToolTip
from PIL import Image

from components.MessageBox import warning

from controllers.roiSetController import get_by_id, delete_by_id
from classes.mosaico import Mosaico

class LastRoiSet(ctk.CTkFrame):
  def __init__(self, id,  *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    self.configure(fg_color="#23272e", corner_radius = 0)
    self.pack(side="top", fill="both", expand=True, padx=10, pady=(0,10))
    
    self.data = get_by_id(id)
    
    self.image_frame = ctk.CTkFrame(self, fg_color="#23272e")
    self.image_frame.pack(side="left", padx=(0,0), pady=4)
    
    self.data_frame = ctk.CTkButton(self, fg_color="#23272e", hover_color="#23272e", command=self.on_click, text="", width=350)
    self.data_frame.pack(side="left", fill="x", padx=0, pady=0)
    
    self.btn_frame = ctk.CTkFrame(self, fg_color="#23272e", width=30, height=30)
    self.btn_frame.pack(side="right", padx=0, pady=0, fill="y")
    
    self.image = Mosaico(self.data["image_path"], self.data["image_type"])
    self.image = ctk.CTkImage(light_image=self.image.img,
                              dark_image=self.image.img,
                              size=(150, 100))
    self.label_img = ctk.CTkButton(self.image_frame, image=self.image, text="", bg_color="#23272e", fg_color="#23272e", hover_color="#23272e", command=self.on_click)
    self.label_img.pack()
    
    self.cut_name = self.data["name"][:45] + "..." if len(self.data["name"]) > 45 else self.data["name"]
    self.name_label = ctk.CTkButton(self.data_frame, text=self.cut_name, font=("Arial", 13, "bold"), command=self.on_click, fg_color="#23272e", hover_color="#23272e", anchor="w")
    self.name_label.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    
    self.type_label = ctk.CTkButton(self.data_frame, text=self.data["image_type"], command=self.on_click, fg_color="#23272e", hover_color="#23272e", anchor="w").grid(row=1, column=0, padx=0, pady=0, sticky="w")
    self.update_label = ctk.CTkButton(self.data_frame, text="Ultima modificación: " + self.data["updated_at"], command=self.on_click, fg_color="#23272e", hover_color="#23272e", anchor="w", height=20).grid(row=2, column=0, padx=0, pady=0, sticky="w")
    self.creation_label = ctk.CTkButton(self.data_frame, text="Fecha de creación: " + self.data["created_at"], command=self.on_click, fg_color="#23272e", hover_color="#23272e", anchor="w", height=20).grid(row=3, column=0, padx=0, pady=0, sticky="w")
    
    trash_icon = ctk.CTkImage(light_image=Image.open("assets/icons/trash-red.png"),dark_image=Image.open("assets/icons/trash-red.png"), size=(15, 15))
    self.delete_btn = ctk.CTkButton(self.btn_frame, text="", fg_color="#23272e", hover_color="#23272e", command=self.delete, width=30, height=30, image=trash_icon)
    self.delete_btn.pack()
    self.delete_btn_tooltip = CTkToolTip(self.delete_btn, message="Eliminar")
    
    self.img_tooltip = CTkToolTip(self.label_img, message=self.data["image_path"])
    self.name_tooltip = CTkToolTip(self.name_label, message=self.data["name"])
    
  def on_click(self):
    self.master.master.master.master.master.view_roi_set(self.data["id"])
    
  def delete(self):
    alert = warning(title="Eliminar imagen", message="¿Seguro/a que desea eliminar este Roi set?", option_1="Eliminar", option_2="Cancelar")
    if alert.get() == "Cancelar":
      return
    
    delete_by_id(self.data["id"])
    self.master.master.master.master.master.view_home()