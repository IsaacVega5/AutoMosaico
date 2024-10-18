import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import utils as ut
import math 
from components.MessageBox import warning

class SelectSoil(ctk.CTkToplevel):
  def __init__(self,img_path, select_soil = [None, None], *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.title("Seleccionar suelo")
    self.after(250, lambda: self.iconbitmap('assets/map.ico'))
    self.configure(fg_color="#23272e", corner_radius=0)
    
    self.img_path = img_path
    self.points = select_soil
    image = Image.open(img_path)
    new_width, new_height, self.resize_ratio = ut.get_new_size(image.size,(800, 800))
    self.new_height = new_height
    
    self.top_bar = ctk.CTkFrame(self, fg_color="#23272e", corner_radius=0)
    self.top_bar.pack(fill="x", padx=0, pady=0)
    
    self.resset_btn = ctk.CTkButton(self.top_bar, text="Reiniciar", command=self.reset, fg_color="#404754", hover_color="#5d677a", width=100)
    self.resset_btn.pack(side="left", padx=5, pady=5)
    
    save_img = ctk.CTkImage(light_image=Image.open("assets/icons/save.png"), dark_image=Image.open("assets/icons/save.png"), size=(20, 20))
    self.save_btn = ctk.CTkButton(self.top_bar, text="Guardar", image=save_img, command=self.save, width=100)
    self.save_btn.pack(side="right", padx=5, pady=5)
    
    self.img = ImageTk.PhotoImage(image.resize((new_width, new_height)))
    
    self.img_canvas = ctk.CTkCanvas(self, width=new_width, height=new_height)
    self.img_canvas.configure(highlightthickness=0)
    self.img_canvas.pack(side="left")
    
    self.img_preview_canvas = ctk.CTkCanvas(self, width=new_height, height=new_height)
    self.img_preview_canvas.configure(highlightthickness=0)
    self.img_preview_canvas.pack(side="right")
    self.img_preview_canvas.create_polygon(0, 0, 50, 50, fill='red', outline='red')
    
    self.img_canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
    self.img_canvas.bind("<Button-1>", self.get_point)
    self.img_canvas.bind("<Button-3>", self.update_last_point)
    self.img_canvas.bind("<Motion>", self.update_zoom)
    
    self.update()
    self.geometry(f"{new_width + new_height}x{new_height + self.top_bar.winfo_height()}")
    self.resizable(False, False)
    self.protocol("WM_DELETE_WINDOW", self.on_close)
    self.draw_points()
    self.set_preview()
    
  def update_zoom(self, event):
    x = event.x
    y = event.y

    resized_x = math.floor(x / self.resize_ratio)
    resized_y = math.floor(y / self.resize_ratio)
    
    # Calcula la región de la imagen que se debe zoom
    img = Image.open(self.img_path)
    left = resized_x - 50
    top = resized_y - 50
    right = resized_x + 50
    bottom = resized_y + 50

    # Dibuja los puntos en la imagen
    draw = ImageDraw.Draw(img, mode="RGBA")
    
    points = self.points
    if points[0] is not None and points[1] is not None:
      minx, miny = min(points[0][0], points[1][0]), min(points[0][1], points[1][1])
      maxx, maxy = max(points[0][0], points[1][0]), max(points[0][1], points[1][1])
      draw.rectangle([(minx, miny), (maxx, maxy)], fill=(255, 0, 0, 50), outline='red')
    
    for index, punto in enumerate(self.points):
      if punto is not None:
        if index == 0:
          draw.ellipse([(punto[0]-6, punto[1]-6), (punto[0]+6, punto[1]+6)], outline='red')
          draw.ellipse([(punto[0]-2, punto[1]-2), (punto[0]+2, punto[1]+2)], fill='red')
        if index == 1:
          draw.ellipse([(punto[0]-2, punto[1]-2), (punto[0]+2, punto[1]+2)], fill='red')

    # Crea una imagen de zoom
    zoom_img = img.crop((left, top, right, bottom))
    zoom_img = zoom_img.resize((100, 100))

    # Convierte la imagen a un formato que pueda ser utilizado por Tkinter
    zoom_img = ImageTk.PhotoImage(zoom_img)

    # Dibuja la imagen de zoom en el canvas
    self.img_canvas.delete("zoom_img")
    self.img_canvas.create_image(x, y, image=zoom_img, tag="zoom_img")
    self.img_canvas.image = zoom_img 

  def on_close(self):
    msg = warning(title="Advertencia", message="¿Seguro/a que desea cerrar sin guardar los cambios?", option_1 = "Continuar", option_2 = "Cancelar")
    if msg.get() == "Cancelar":
      return
    
    self.points = None
    self.destroy()
  
  def reset(self):
    self.points = [None, None]
    self.draw_points()
  
  def save(self):
    if self.points[0] is None or self.points[1] is None:
      msg = warning(title="Advertencia", message="No se ha seleccionado un area de suelo.\nSi guarda ahora el area de suelo se guardará como vacía.", option_1 = "Continuar", option_2 = "Cancelar")
      self.points = [None, None]
      if msg.get() == "Cancelar":
        return
    self.destroy()
  
  def get_point(self, event):
    x = math.floor(event.x / self.resize_ratio)
    y = math.floor(event.y / self.resize_ratio)
    
    if self.points[0] is None:
      self.points[0] = (x, y)
    else:
      self.points[1] = self.points[0]
      self.points[0] = (x, y)
    
    self.draw_points()
    self.set_preview()
    self.update_zoom(event=event)
  
  def update_last_point(self, event):
    x = math.floor(event.x / self.resize_ratio)
    y = math.floor(event.y / self.resize_ratio)
    self.points[0] = (x, y)

    self.draw_points()
    self.set_preview()
    self.update_zoom(event=event)
  
  def draw_points(self):
    self.img_canvas.delete("all")
    self.img_canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
    
    if self.points[1] is not None:
      x = self.points[0][0] * self.resize_ratio
      y = self.points[0][1] * self.resize_ratio
      x2 = self.points[1][0] * self.resize_ratio
      y2 = self.points[1][1] * self.resize_ratio
      self.img_canvas.create_rectangle(x, y, x2, y2, fill='red', outline='red', stipple='gray50')
      
    for index, point in enumerate(self.points):
      if point is not None:
        x = point[0] * self.resize_ratio
        y = point[1] * self.resize_ratio
        
        if index == 0:
          self.img_canvas.create_oval(x - 6, y - 6, x + 6, y + 6, outline="red")
          self.img_canvas.create_oval(x - 2, y - 2, x + 2, y + 2, outline="red", fill="red")
        if index == 1:
          self.img_canvas.create_oval(x - 2, y - 2, x + 2, y + 2, outline="red")
    
  def set_preview(self):
    points = self.points
    self.img_preview_canvas.delete("all")
    self.img_preview_canvas.create_rectangle(0, 0, self.new_height, self.new_height, fill='black', outline='black')
    
    if points[0] is None or points[1] is None: 
      return
    minx, miny = min(points[0][0], points[1][0]), min(points[0][1], points[1][1])
    maxx, maxy = max(points[0][0], points[1][0]), max(points[0][1], points[1][1])
    img = Image.open(self.img_path).crop((minx, miny, maxx, maxy))
    width, height, _ = ut.get_new_size(img.size, (self.new_height, self.new_height))
    if width == 0 or height == 0:
      return
    img = img.resize((width, height), resample=Image.BICUBIC)
    
    img_tk = ImageTk.PhotoImage(img)
    self.img_preview_canvas.create_image(self.new_height/2, self.new_height/2, anchor=tk.CENTER, image=img_tk)
    self.img_preview_canvas.image = img_tk
