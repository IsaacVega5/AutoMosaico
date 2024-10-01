import customtkinter as ctk

from utils import format_number

class ProgressBar(ctk.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, **kwargs)
    self.configure(fg_color="#23272e", width=300, height=40 , corner_radius = 0)
    
    self.label = ctk.CTkLabel(self, text="Procesando imágenes", anchor="w")
    self.label.pack(side="top", fill="x", padx=5, pady=5)
    
    self.console = ctk.CTkTextbox(self, width=300, height=100, activate_scrollbars=False, font=("Consolas", 11))
    self.console.pack(side="top", fill="both", padx=5, pady=0)
    
    self.progress_bar = ctk.CTkProgressBar(self, mode="determinate")
    self.progress_bar.pack(side="bottom", fill="x", padx=5, pady=(0,5))
    
    self.current = 0
    self.lower()
    
  def start(self):
    self.place(relx=0.5, rely=0.5, anchor="center")
  
  def stop(self):
    self.progress_bar.stop()
    self.place_forget()
  
  def set_max(self, value):
    self.max = value
  
  def console_log(self, text):
    self.console.insert('end', f"{text}")
    self.console.see('end')
  
  def console_clear(self):
    self.console.delete('1.0', 'end')
  
  def set(self, value):
    self.current = value
    self.progress_bar.set(value)
  
  def step(self, text):
    self.current += 1
    self.progress_bar.set(self.current / self.max)
    if text == None: return
    self.console.insert('end', f"{format_number(self.current, len(str(self.max)))} / {self.max}     {text}")
    self.console.see('end')