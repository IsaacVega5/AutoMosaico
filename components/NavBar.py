import customtkinter as ctk
from PIL import Image

from components.iconLinkBtn import IconLinkBtn

class NavBar(ctk.CTkFrame):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.configure(
      fg_color = "#23272e",
      bg_color = "#1e2227",
      width= 50,
      corner_radius = 0
    )
    
    logo_img = Image.open("assets/logo.png")
    self.logo =ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(50, 50))
    self.label = ctk.CTkLabel(self, text="", image=self.logo)
    self.label.pack(padx=20, pady=(20, 0))
    
    rar_icon = Image.open("assets/icons/rar.png")
    self.add_button = ctk.CTkButton(self, text="Añadir Roi", image=ctk.CTkImage(rar_icon, size=(25, 25)), fg_color="#1a7ecf", hover_color="#209bff")
    self.add_button.configure(
      height=40,
      corner_radius=25,
      command = self.master.new_roi
    )
    self.add_button.pack(padx=10, pady=10)
    
    self.home = IconLinkBtn(master = self, action= lambda: self.master.view_home(), image = ctk.CTkImage(Image.open("assets/icons/home.png"), size=(20, 20)), text="Inicio")
    self.lista = IconLinkBtn(master = self, action= lambda: self.master.view_roi_set_list(), image = ctk.CTkImage(Image.open("assets/icons/rar.png"), size=(20, 20)), text="Lista")
    # self.settings = IconLinkBtn(master = self, action= lambda: self.master.view_home(), image = ctk.CTkImage(Image.open("assets/icons/settings.png"), size=(20, 20)), text="Ajustes")

    