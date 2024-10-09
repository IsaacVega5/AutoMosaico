import tkinter as tk
import customtkinter as ctk
from PIL import Image
from datetime import datetime
import threading
import os
import json
from CTkToolTip import CTkToolTip

from components.roiSetHeader import RoiSetHeader
from components.roiSetRarImg import RoiSetRarImg
from components.imageSelected import ImageSelected
from components.MessageBox import warning,error, check
from components.selectionPop import SelectionPop

from views.selectSoil import SelectSoil

from controllers.roiSetController import get_by_id, edit_by_id
from services.process import process
from services.excel import *
from services.logs import save_error
from utils import get_name_from_path, ellipsis_text
from constants import IMG_TYPES, EXPORT_TYPES, RGB_VALUES, ONE_CHANNEL_VALUES, SOIL_MASK_TYPE

class roiSet(ctk.CTkFrame):
  def __init__(self, id, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.configure(fg_color="#282c34", corner_radius = 0)
    
    self.id = id
    self.change_update_date()
    data = get_by_id(self.id)
    if data == False: return
    
    self.name = data["name"]
    self.img = data["image_path"]
    self.roi = data["roi_path"]
    self.type = data["image_type"]
    self.img_list = []
    self.select_soil = json.loads(data["soil_data"]) if "soil_data" in data and data["soil_data"] != "" else {"type" : SOIL_MASK_TYPE[0], "value" : [None, None]}
    # #* Objeto select soil, value puede ser un array con coordenadas o un path
    # self.select_soil = {
    #   "type" : SOIL_MASK_TYPE[0],
    #   "value" : self.select_soil
    # }
    
    self.header = RoiSetHeader(master=self, id=data['id'])
    
    self.body = ctk.CTkScrollableFrame(self, fg_color="#282c34")
    self.body.pack(side="top", fill="both", expand=True, padx=0, pady=0, ipadx=0, ipady=0)
    
    self.roiSetRarImg = RoiSetRarImg(master = self.body, img_path=self.img, roi_path=self.roi, img_type=self.type)
    
    self.add_new_img_title_frame = ctk.CTkFrame(self.body)
    self.add_new_img_title_frame.pack(side="top", fill="x", padx=5, pady=5)
    
    self.add_new_img_label = ctk.CTkLabel(self.add_new_img_title_frame, text="Añadir imágenes a analizar")
    self.add_new_img_label.pack(side="left", padx=5, pady=5)
    
    self.add_new_img_btn = ctk.CTkButton(self.add_new_img_title_frame, text="Añadir", command=self.add_new_img, width=100)
    self.add_new_img_btn.pack(side="right", padx=5, pady=5)
    
    self.clear_img_btn = ctk.CTkButton(self.add_new_img_title_frame, text="Eliminar", command=self.clear_img, width=100, fg_color="#fa5252", hover_color="#ff6a53")
    self.clear_img_btn.pack(side="right", padx=5, pady=5)
    
    self.images_frame = ctk.CTkFrame(self.body, fg_color="#23272e")
    self.images_frame.pack(side="top", fill="both", expand=True, padx=5, pady=0)
    
    self.footer = ctk.CTkFrame(self)
    self.footer.pack(side="bottom", padx=(10,5), pady=5, fill="both")
    
    self.get_soil_area_btn = ctk.CTkButton(self.footer, text="Suelo", fg_color="#404754", hover_color="#5d677a", width=100, command=self.get_soil_area)
    self.get_soil_area_btn.pack(side="left")
    
    if self.select_soil['type'] == SOIL_MASK_TYPE[0]:
      self.points_txt = ctk.CTkLabel(self.footer, text=(f"{str(self.select_soil['value'][0])} {str(self.select_soil['value'][1])}" if self.select_soil['value'] != [None, None] else "No se ha seleccionado un area de suelo"))
    elif self.select_soil['type'] == SOIL_MASK_TYPE[1]:
      self.points_txt = ctk.CTkLabel(self.footer, text=(f"{str(ellipsis_text(self.select_soil['value'], 50))}" if self.select_soil != "" else "No se ha seleccionado un area de suelo"))
    self.points_txt.pack(side="left", padx=5)
    self.points_txt_tool = CTkToolTip(self.points_txt, message=self.select_soil['value'], bg_color = "#23272e")
    
    excel_logo = ctk.CTkImage(light_image=Image.open("assets/icons/excel.png"), dark_image=Image.open("assets/icons/excel.png"), size=(20, 20))
    self.generate_btn = ctk.CTkButton(self.footer, text="Generar", command=self.click_generate_xslx, fg_color="#175935", hover_color="#0f783f", width=100, image=excel_logo)
    self.generate_btn.pack(side="right")
    
  def get_roi(self):
    return self.roi
  def get_img(self):
    return self.img
  
  def get_soil_area(self):
    type_soil = SelectionPop(master=self, title="Tipo de mascara", text="Seleccione el tipo de mascara que desea usar",
                             alternatives=SOIL_MASK_TYPE)
    
    if type_soil.get() is False: return
    if type_soil.get()['alternatives'] == SOIL_MASK_TYPE[0]:  
      soil_points = self.select_soil['value'] if self.select_soil['type'] == SOIL_MASK_TYPE[0] else [None, None]
      
      selectSoil = SelectSoil(master=self, img_path=self.img, select_soil=soil_points)
      selectSoil.after(250, selectSoil.lift)
      
      self.wait_window(selectSoil)
      points = selectSoil.points
      if points is None: return
      self.select_soil = {
        "type" : SOIL_MASK_TYPE[0],
        "value" : points
      }
      self.points_txt.configure(text=(f"{str(points[0])} {str(points[1])}" if points != [None, None] else "No se ha seleccionado un area de suelo"))
    elif type_soil.get()['alternatives'] == SOIL_MASK_TYPE[1]:
      path = tk.filedialog.askopenfilename(filetypes=(("Imágenes", "*.png;*.jpg;*.tif;*.tiff"),))
      self.select_soil = {
        "type" : SOIL_MASK_TYPE[1],
        "value" : path
      }
      self.points_txt.configure(text=(f"{str(path)}" if path != "" else "No se ha seleccionado un area de suelo"))
    
  def clear_img(self):
    alert = warning(title="Eliminar imágenes", message="¿Seguro/a que desea eliminar todas las imágenes?", option_1="Eliminar", option_2="Cancelar")
    if alert.get() == "Cancelar":
      return

    self.img_list = []
    self.render_img_list()
  
  def add_new_img(self):
    file_path = tk.filedialog.askopenfilenames(filetypes=(("Imágenes", "*.png;*.jpg;*.tif;*.tiff"),))
    if file_path is None or file_path == "" : return
    
    type = SelectionPop(master=self,
                         title="Tipo de imagen",
                         text="Seleccione el tipo de las imágenes que desea cargar",
                         alternatives=IMG_TYPES)
    if type.get() is False: return
    type = type.get()['alternatives']
    for file in file_path:
      img = {
        "path" : file,
        "type" : type,
      }
      self.img_list.insert(0, img)
    
    self.render_img_list()
  
  def click_generate_xslx(self):
    master = self.master.master
    export_form = SelectionPop(master,
                       "Generar xslx",
                       "¿De que forma desea exportar los datos?", 
                       EXPORT_TYPES,
                       checkVars={
                         "Incluir imagen original" : False,
                         "Remover el suelo" : False
                       })
    
    
    res = export_form.get()
    if res is False: return

    type = res['alternatives']
    origin = res['checks'][0]
    soil = res['checks'][1]
    
    value_export = None
    if type == EXPORT_TYPES[1]:
      value_export = SelectionPop(master,
                                  title="Generar xslx",
                                  subtitle="Seleccione el valor que desea exportar\npor cada tipo de imagen",
                                  text = IMG_TYPES,
                                  alternatives=[
                                    RGB_VALUES,
                                    ONE_CHANNEL_VALUES,
                                    ONE_CHANNEL_VALUES,
                                    ONE_CHANNEL_VALUES,
                                  ])

      if value_export.get() is False: return
      value_export = value_export.get()['alternatives']
    
    self.master.master.progressBar.start()
    threading.Thread(target=self.generate, args=(export_form.get()['alternatives'],value_export, origin, soil)).start()
      
    
  def generate(self, export_form, value_export, origin, soil):
    workbook, destiny_path = create_workbook()
    if destiny_path is None: return
    progress_bar = self.master.master.progressBar
    progress_bar.lift(aboveThis=None)
    img_list = self.img_list.copy()
    if origin: img_list.insert(0, {
        "path" : self.img,
        "type" : self.type,
      })
    
    values = process(roi_path=self.roi, img_roi_path=self.img, img_list = img_list, progress_bar = progress_bar, soil = self.select_soil if soil else None)
    to_export = {
      'RGB' : [],
      'Termal' : [],
      'OCN' : [],
      'RGN' : [],
    }
    for i,value in enumerate(values):
      if value['values'] is False: 
        save_error(self.img_list, self.roi, self.img)
        msg = error(title='Error', message='Error al generar el xlsx\n\nVerifique que los tipos coincidan con las imágenes y vuelva a intentarlo.\nSi el problema persiste contacte con el administrador.', option_1 = "Cancelar", option_2 = "Continuar")
        if msg.get() == 'Cancelar':
          self.master.master.progressBar.stop()
          return False
        else :
          continue
      
      if export_form == "Individual" : 
        name = value['type'] + ' - ' + get_name_from_path(value['path'])
        worksheet = add_worksheet(workbook, name)
        if value['type'] == 'RGB':
          add_table_headers(worksheet, ['Parc.','Name', 'Intensity', 'Hue', 'Saturation', 'Lightness', '*a', '*b', '*u', '*v', 'GA%', 'GGA%', 'CSI'])
        else:
          add_table_headers(worksheet, ['Parc.', 'Name', 'Area', 'Mean', 'Min', 'Max'])
        for i,result in enumerate(value['values']):
          add_table_row(worksheet, i+2, [i+1, *result])
      
      elif export_form == "Conjunto":
        to_export[value['type']].append({
          'name' : get_name_from_path(value['path']),
          'values' : value['values']
        })
        
    if export_form == "Conjunto":
      for index, type in enumerate(to_export):
        if len(to_export[type]) == 0: continue
        name = type
        worksheet = workbook.add_worksheet(type)
        
        if type == 'RGB':
          index_value = RGB_VALUES.index(value_export[index])
        else:
          index_value = ONE_CHANNEL_VALUES.index(value_export[index])
          
        n_parc = len(to_export[type][0]['values'])
        parc = [ i+1 for i in range(n_parc)]
        names = [ item[0] for item in to_export[type][0]['values']]
        
        add_table_column(worksheet, 0, 'Parc.', parc)
        add_table_column(worksheet, 1, 'Name', names)
        
        column = 2
        for img in to_export[type]:
          img_values = [ img['values'][i][index_value+1] for i in range(n_parc)]
          add_table_column(worksheet, column, img['name'], img_values)
          column += 1
    
    self.master.master.progressBar.stop()
    
    saved = False
    while not saved:
      try:
        save_workbook(workbook)
        saved = True
      except Exception as e:
        msg = error(title='Error', message=f'Error al guardar el archivo Excel. \n\nVerifique que no este abierto otro archivo con el mismo nombre.\nsi el error persiste contacte con el administrador.', option_1 = "Reintentar", option_2 = "Cancelar")
        if msg.get() != 'Reintentar':
          return None
    
    if destiny_path is None:
      return
  
    msg = check(title='Tarea finalizada', message='Se ha exportado la información correctamente', option_1 = "Abrir archivo", option_2 = "Aceptar")
    if msg.get() == 'Aceptar':
      return
      
    os.startfile(destiny_path)
  
  def get_soil_data(self):
    return self.select_soil
  
  def render_img_list(self):
    self.destroy_img()
    self.add_imgs_components()
    
  def destroy_img(self):
    for child in self.images_frame.winfo_children():
      child.destroy()
  
  def add_imgs_components(self):
    col = 0
    row = 0
    for i in range(len(self.img_list)):
      self.img_selected = ImageSelected(master=self.images_frame, image_path=self.img_list[i]["path"], type=self.img_list[i]["type"], index=i, soil_data = self.get_soil_data)
      self.img_selected.grid(row=row, column=col, padx=5, pady=5)
      col += 1
      if col >= 3:
        col = 0
        row += 1
  
  def change_img_type_by_index(self, index, type):
    self.img_list[index]["type"] = type
  
  def delete_img_by_index(self, index):
    self.img_list.pop(index)
    self.render_img_list()
  
  def destroy(self):
    super().destroy()
    
  def change_update_date(self):
    data = get_by_id(self.id)
    new_data = {
      "id": data["id"],
      "name": data["name"],
      "roi_path": data["roi_path"],
      "image_path": data["image_path"],
      "image_type": data["image_type"],
      "updated_at": str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
      "created_at": data["created_at"],
    }
    
    edit_by_id(self.id, new_data)
