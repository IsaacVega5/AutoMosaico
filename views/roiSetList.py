import customtkinter as ctk
from datetime import datetime
from fuzzywuzzy import process

from components.searchBar import SearchBar
from components.roiSetElement import RoiSetElement

from controllers.roiSetController import get_all

class RoiSetList(ctk.CTkScrollableFrame):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    self.searchBar = SearchBar(master= self, on_search=self.on_search, on_order=self.on_order)
    self.searchBar.pack(side="top", fill="x", padx=10, pady=10)
    
    self.list_title = ctk.CTkLabel(self, text="Roi sets", font=("Arial", 13, "bold"))
    self.list_title.pack( padx=10, pady=(10,0), expand=True, fill="x", anchor="w")
    
    self.list_frame_render()
  
  
  def on_search(self):
    self.list_frame_render()
    
  def on_order(self, event):
    self.list_frame_render()
    
    
  def list_frame_render(self):
    try:
      self.list_frame.destroy()
    except:
      pass
    
    text = self.searchBar.search_entry.get()
    roi_set_list = get_all('updated_at', 'desc')
    roi_set_name = [i["name"] for i in roi_set_list]
    
    if text != "":
      roi_set_name = process.extractBests(text, choices=roi_set_name, score_cutoff=40, limit=10)
      roi_set_name = [i[0] for i in roi_set_name]
      roi_set_new_list = []
      
      for name in roi_set_name:
        for roi_set in roi_set_list:
          if name == roi_set["name"]:
            roi_set_new_list.append(roi_set)
            
      roi_set_list = roi_set_new_list
    
    if self.searchBar.order_select.get() == "ABC asc":
      roi_set_list.sort(key=lambda x: x["name"])
    elif self.searchBar.order_select.get() == "ABC desc":
      roi_set_list.sort(key=lambda x: x["name"], reverse=True)
    elif self.searchBar.order_select.get() == "Creación asc":
      roi_set_list.sort(key=lambda x: x["created_at"])
    elif self.searchBar.order_select.get() == "Creación desc":
      roi_set_list.sort(key=lambda x: x["created_at"], reverse=True)
    elif self.searchBar.order_select.get() == "Edición asc":
      roi_set_list.sort(key=lambda x: x["updated_at"])
    elif self.searchBar.order_select.get() == "Edición desc":
      roi_set_list.sort(key=lambda x: x["updated_at"], reverse=True)
    
    self.list_frame = ctk.CTkFrame(self, fg_color="#23272e", corner_radius=0)
    self.list_frame.pack(expand=True, padx=10, pady=(0,10))
    
    for i, roi_set in enumerate(roi_set_list):
      element = RoiSetElement(master=self.list_frame, id=roi_set["id"])
      element.pack(padx=0, pady=0, expand=True, fill="x")