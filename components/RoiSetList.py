import customtkinter as ctk

from components.roiSetElement import RoiSetElement

from controllers.roiSetController import get_all

class LastRoiSetList(ctk.CTkScrollableFrame):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    get_all('updated_at', 'asc')
    
    
    