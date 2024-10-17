import customtkinter as ctk
import uuid
import tkinter as tk
from datetime import datetime
from PIL import Image
import json

from views.selectSoil import SelectSoil

from components.imgOriginPreview import ImgOriginPreview
from components.selectionPop import SelectionPop
from services.jsonFiles import save_to_json

from constants import ROI_SET_PATH, IMG_TYPES, SOIL_MASK_TYPE


class NewRoi(ctk.CTkFrame):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.configure(fg_color="#282c34", corner_radius = 0)
    
    self.roi_path = None
    self.img_roi_path = None
    self.type = IMG_TYPES[0]
    self.data_soil = {
      "type": SOIL_MASK_TYPE[0],
      "value": [None, None]
    }
    
    self.frame = ctk.CTkFrame(self)
    self.frame.place(relx=0.5, rely=0.5, anchor="center")
    self.frame.configure(fg_color="#23272e", corner_radius = 0)

    self.title = ctk.CTkLabel(self.frame, text="Nuevo roi set", font=ctk.CTkFont(size=15, weight="bold"))
    self.title.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")
    
    self.img_x = ctk.CTkImage(light_image=Image.open("assets/icons/x.png"), dark_image=Image.open("assets/icons/x.png"), size=(20, 20))
    self.button = ctk.CTkButton(self.frame, text="", command=self.destroy, fg_color="#23272e", hover_color="#23272e", image=self.img_x, height=25, width=25)
    self.button.grid(row=0, column=1, padx=10, pady=(10,0), sticky="e")
    
    self.label = ctk.CTkLabel(self.frame, text="Ingrese la ruta del archivo roi.zip *")
    self.label.grid(row=1, column=0, padx=10, pady=(0,0), sticky="w")
    
    self.entry = ctk.CTkEntry(self.frame, placeholder_text="C:/ruta/a/roi.zip", width=250)
    self.entry.configure(state='disabled')
    self.entry.grid(row=2, column=0, padx=(10, 2), pady=(0,0))
    
    self.roi_btn = ctk.CTkButton(self.frame, text="Seleccionar", command=self.select_roi, fg_color="#1a7ecf", hover_color="#209bff", width=60)
    self.roi_btn.grid(row=2, column=1, padx=(2, 10), pady=(0,0))

    self.img_label = ctk.CTkLabel(self.frame, text="Seleccione la imagen original del roi *", compound="left")
    self.img_label.grid(row=3, column=0, padx=(10, 2), pady=(5,0), sticky="w")
    
    self.img_entry = ctk.CTkEntry(self.frame, placeholder_text="C:/ruta/a/imagen.png", width=250)
    self.img_entry.configure(state='disabled')
    self.img_entry.grid(row=4, column=0, padx=(10, 2), pady=0)
    
    self.img_btn = ctk.CTkButton(self.frame, text="Seleccionar", command=self.select_img, fg_color="#1a7ecf", hover_color="#209bff", width=60)
    self.img_btn.grid(row=4, column=1, padx=(2, 10), pady=0)
    
    self.soil_label = ctk.CTkLabel(self.frame, text="Seleccione un area de suelo de la imagen")
    self.soil_entry = ctk.CTkEntry(self.frame, placeholder_text="No se ha seleccionado un area de suelo", width=250)
    self.soil_entry.configure(state='disabled')
    
    self.soil_btn = ctk.CTkButton(self.frame, text="Seleccionar", command=self.select_soil, fg_color="#1a7ecf", hover_color="#209bff", width=60)
    
    self.save_btn = ctk.CTkButton(self.frame, text="Aceptar", command=self.save, width=130)
    self.save_btn.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="e")
    
  def select_soil(self):
    select_type = SelectionPop(self, title="Tipo de método", text="Seleccione el tipo de Método que desea usar", alternatives=SOIL_MASK_TYPE)
    if not select_type.get(): return
    res = select_type.get()['alternatives']
    
    if res == SOIL_MASK_TYPE[0]:
      selectSoil = SelectSoil(master=self, img_path=self.img_roi_path, select_soil=self.data_soil["value"] if self.data_soil["type"] == SOIL_MASK_TYPE[0] else None)
      selectSoil.after(250, selectSoil.lift)
      self.wait_window(selectSoil)
      if selectSoil.points is None: return
      self.data_soil["value"] = selectSoil.points
      self.data_soil["type"] = SOIL_MASK_TYPE[0]
      self.soil_entry.configure(state='normal')
      self.soil_entry.delete(0, ctk.END)
      self.soil_entry.insert(0, str(selectSoil.points[0]) + ", " + str(selectSoil.points[1]))
      self.soil_entry.configure(state='disabled')
    elif res == SOIL_MASK_TYPE[1]:
      path = tk.filedialog.askopenfilename(filetypes=(("Imágenes", "*.png;*.jpg;*.tif;*.tiff"),))
      if path is None or path == "" : return
      self.data_soil["value"] = path
      self.data_soil["type"] = SOIL_MASK_TYPE[1]
      self.soil_entry.configure(state='normal')
      self.soil_entry.delete(0, ctk.END)
      self.soil_entry.insert(0, str(path))
      self.soil_entry.configure(state='disabled')
    elif res == SOIL_MASK_TYPE[2]:
      self.data_soil["value"] = None
      self.data_soil["type"] = SOIL_MASK_TYPE[2]
      self.soil_entry.configure(state='normal')
      self.soil_entry.delete(0, ctk.END)
      self.soil_entry.insert(0, SOIL_MASK_TYPE[2])
      self.soil_entry.configure(state='disabled')
  
  def select_roi(self):
    file_path = tk.filedialog.askopenfilename(filetypes=(("Archivo zip", "*.zip"),))
    if file_path is None or file_path == "" : return
    
    self.label.configure(text_color="white")
    
    self.entry.configure(state='normal')
    self.entry.delete(0, ctk.END)
    self.entry.insert(0, file_path)
    self.entry.configure(state='disabled')
    
    self.roi_path = file_path
  
  def select_img(self):
    file_path = tk.filedialog.askopenfilename(filetypes=(("Imágenes", "*.png;*.jpg;*.tif;*.tiff"),))
    if file_path is None or file_path == "" : return
    
    self.img_label.configure(text_color="white")
    
    self.img_entry.configure(state='normal')
    self.img_entry.delete(0, ctk.END)
    self.img_entry.insert(0, file_path)
    self.img_entry.configure(state='disabled')
    
    if hasattr(self, 'img_preview'): self.img_preview.destroy()
    self.img_preview = ImgOriginPreview(master=self.frame, src=(file_path))
    
    self.img_roi_path = file_path
    
    # Mostrar opciones de suelo
    self.soil_label.grid(row=6, column=0, padx=(10, 2), pady=(5,0), sticky="w")
    self.soil_entry.grid(row=7, column=0, padx=(10, 2), pady=0)
    self.soil_btn.grid(row=7, column=1, padx=(2, 10), pady=0)
    
  def destroy(self):
    super().destroy()
    
  def save(self):
    if self.roi_path is None:
      self.label.configure(text_color="#fa5252")
    if self.img_roi_path is None:
      self.img_label.configure(text_color="#fa5252")
    
    if self.roi_path is None or self.img_roi_path is None:
      self.shake()
      return
    
    data = {
      "id": str(uuid.uuid4()),
      "name": 'Roi Set - Undefined',
      "roi_path": self.roi_path,
      "image_path": self.img_roi_path,
      "image_type": self.type,
      "soil_data": json.dumps(self.data_soil),
      "updated_at": str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
      "created_at": str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
    }
    
    save_to_json(ROI_SET_PATH, data)
    
    self.destroy()
    self.master.view_roi_set(data["id"])

    
  
  def shake (self):
    for i in range(10):
      self.frame.place(relx=0.49, rely=0.5)
      self.frame.after(100, lambda: self.frame.place(relx=0.51, rely=0.5))
      self.frame.after(200, lambda: self.frame.place(relx=0.5, rely=0.5, anchor="center"))