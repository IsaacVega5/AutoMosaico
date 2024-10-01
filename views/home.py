import customtkinter as ctk
from PIL import Image

from controllers.roiSetController import get_all
from constants import ROI_SET_PATH

from components.lastRoiSet import LastRoiSet
from components.roiSetElement import RoiSetElement

class Home(ctk.CTkScrollableFrame):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.configure(fg_color="#282c34", corner_radius = 0)
    
    roi_set_list = get_all('updated_at', 'desc')
    
    self.list_title = ctk.CTkLabel(self, text="Último Roi set", font=("Arial", 13, "bold"))
    self.list_title.pack( padx=10, pady=(10,0), expand=True, fill="x", anchor="w")
    
    if len(roi_set_list) > 0:
      self.lastRoiSet =  LastRoiSet(master = self, id=roi_set_list[0]["id"])
    else:
      ctk.CTkLabel(self, text="No hay Roi sets").pack( padx=10, pady=(10,0), expand=True, fill="x", anchor="w")
    
    self.list_title = ctk.CTkLabel(self, text="Últimos Roi sets modificados", font=("Arial", 13, "bold"))
    self.list_title.pack( padx=10, pady=(10,0), expand=True, fill="x", anchor="w")
    
    if len(roi_set_list) > 0:
      self.list_frame_render()
    else:
      ctk.CTkLabel(self, text="...").pack( padx=10, pady=(10,0), expand=True, fill="x", anchor="w")
    

    
  def destroy(self):
    super().destroy()
    
  def list_frame_render(self):
    try:
      self.list_frame.destroy()
    except:
      pass
    
    roi_set_list = get_all('updated_at', 'desc')   
    
    self.list_frame = ctk.CTkFrame(self, fg_color="#23272e", corner_radius=0)
    self.list_frame.pack(expand=True, padx=10, pady=(0,10))
    for i, roi_set in enumerate(roi_set_list[:10]):
      element = RoiSetElement(master=self.list_frame, id=roi_set["id"])
      element.pack(padx=0, pady=0, expand=True, fill="x")
  