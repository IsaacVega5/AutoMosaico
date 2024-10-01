import customtkinter as ctk
from PIL import Image

class IconLinkBtn(ctk.CTkButton):
  def __init__(self, action, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.action = action
    self.pack(side="top", padx=5, pady=5)
    self.configure(
      fg_color = "#23272e",
      hover_color = "#23272e",
      height = 40,
      command = self.button_click,
      width = 100,
      corner_radius = 25,
      compound = "left",
    )
    
  
  def button_click(self):
    self.action()