import customtkinter as ctk
from PIL import Image

from constants import ORDER_BY

class SearchBar(ctk.CTkFrame):
  def __init__(self, on_search, on_order, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    self.search_entry = ctk.CTkEntry(self, placeholder_text="Buscar")
    self.search_entry.pack(side="left", padx=2, pady=10, fill="x", expand=True)
        
    self.order_select = ctk.CTkComboBox(self, values=ORDER_BY, width=150, state="readonly", command=on_order)
    self.order_select.set(ORDER_BY[0])
    self.order_select.pack(side="left", padx=2, pady=10)
    
    self.search_icon = Image.open("assets/icons/search.png")
    self.search_icon = ctk.CTkImage(light_image=self.search_icon, dark_image=self.search_icon, size=(20, 20))
    self.search_btn = ctk.CTkButton(self, image=self.search_icon, text="", width=40, height=20, command=on_search)
    self.search_btn.pack(side="left", padx=2, pady=10)
    