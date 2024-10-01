import customtkinter as ctk
from PIL import Image
from constants import IMG_TYPES

class SelectionPop(ctk.CTkFrame):
  def __init__(self,master, title, text, alternatives, subtitle=None, *args, **kwargs):
    super().__init__(master, *args, **kwargs)
    self.configure(corner_radius =0, fg_color="#282c34", bg_color="#282c34")
    self.place(relx=0.5, rely=0.5, anchor="center")
    
    self.subtitle = subtitle
    self.text = text
    self.alternatives = alternatives
    self.response = alternatives[0]
    
    self.title_frame = ctk.CTkFrame(self, fg_color="#23272e", corner_radius=0, height=10)
    self.title_frame.pack(side="top", fill ="x", padx=0, pady=0)
    
    self.icon = ctk.CTkImage(light_image=Image.open("assets/logo.png"), dark_image=Image.open("assets/logo.png"), size=(15,15))
    self.icon_label = ctk.CTkLabel(self.title_frame, text="", image=self.icon)
    self.icon_label.pack(side="left", padx=5, pady=5)
    
    self.title = ctk.CTkLabel(self.title_frame, text=title)
    self.title.pack(side="left", padx=5, pady=5)
    
    if isinstance(self.text, list):
      self.multi_render()
    else:
      self.one_render()
    
    self.btn_frame = ctk.CTkFrame(self, corner_radius=0)
    self.btn_frame.pack(side="bottom", fill ="x", padx=0, pady=0)
    
    self.accept_btn = ctk.CTkButton(self.btn_frame, text="Aceptar", command=self.accept, width=100)
    self.accept_btn.pack(side="right", padx=(5,10), pady=10)
    
    self.cancel_btn = ctk.CTkButton(self.btn_frame, text="Cancelar", command=self.cancel, width=100 , fg_color="#fa5252", hover_color="#ff6a53")
    self.cancel_btn.pack(side="right", padx=0, pady=10)
    
    self.wait_window(self)

  def one_render(self):
    self.label = ctk.CTkLabel(self, text=self.text)
    self.label.pack(side="top", padx=10, pady=10)
    
    self.alternatives_entry = ctk.CTkComboBox(self, values=self.alternatives, state="readonly")
    self.alternatives_entry.set(self.alternatives[0])
    self.alternatives_entry.pack(side="top", padx=10, pady=10, fill = "x")
    
  
  def multi_render(self):
    if self.subtitle != None:
      self.label = ctk.CTkLabel(self, text=self.subtitle)
      self.label.pack(side="top", padx=10, pady=10)
        
    self.alternatives_frame = ctk.CTkFrame(self, fg_color="#282c34")
    self.alternatives_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    
    self.alternatives_entries = []
    for i in range(len(self.text)):
      self.label = ctk.CTkLabel(self.alternatives_frame, text=self.text[i])
      self.label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
      
      alternatives_entry = ctk.CTkComboBox(self.alternatives_frame, values=self.alternatives[i], state="readonly")
      alternatives_entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
      
      alternatives_entry.set(self.alternatives[i][0])
      
      self.alternatives_entries.append(alternatives_entry)
  
  def get(self):
    return self.response
  
  def accept(self):
    if isinstance(self.text, list):
      self.response = [ entry.get() for entry in self.alternatives_entries ]
    else:
      self.response = self.alternatives_entry.get()
    
    self.place_forget()
    self.destroy()
  
  def cancel(self):
    self.response = None
    self.place_forget()
    self.destroy()

