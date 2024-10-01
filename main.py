import customtkinter as ctk
from multiprocessing import freeze_support

from components.NavBar import NavBar
from components.progressBar import ProgressBar

from views.home import Home
from views.roiSet import roiSet	
from views.newRoi import NewRoi
from views.roiSetList import RoiSetList
from controllers.roiSetController import check_images

import PIL
PIL.Image.MAX_IMAGE_PIXELS = 999999999999

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("assets/themes/main.json")

height, width = 500, 750

class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.geometry(f"{width}x{height}")
		self.minsize(width, height)
		self.resizable(False, False)
		self.iconbitmap("assets/map.ico")
	
		self.title("AutoMosaico")
		
		check_images()
		self.current_view = 'Inicio'
		
		self.NavBar = NavBar(self)
		self.NavBar.pack(side="left", fill="y")

		self.View_frame = ctk.CTkFrame(self, fg_color="#282c34")
		self.View_frame.pack(side="top", fill="both", expand=True)
  
		self.View = Home(self.View_frame)
		self.View.pack(side="top", fill="both", expand=True)

		self.progressBar = ProgressBar(self)
		
	def new_roi(self):
		self.NewRoi = NewRoi(self)
		self.NewRoi.place(x=0, y=0, relwidth=1, relheight=1)
  
	def view_roi_set(self, id):
		self.View_frame.destroy()
		self.View_frame = ctk.CTkFrame(self, fg_color="#282c34")
		self.View_frame.pack(side="top", fill="both", expand=True)
  
		self.View = roiSet(master=self.View_frame, id=id)
		self.View.pack(side="top", fill="both", expand=True)
  
	def view_home(self):
		self.current_view = 'Home'
		self.View_frame.destroy()
		self.View_frame = ctk.CTkFrame(self, fg_color="#282c34")
		self.View_frame.pack(side="top", fill="both", expand=True)

		# self.View.master.destroy()
		self.View = Home(self.View_frame)
		self.View.pack(side="top", fill="both", expand=True)

	def view_roi_set_list(self):
		self.current_view = 'RoiSetList'
		self.View_frame.destroy()
		self.View_frame = ctk.CTkFrame(self, fg_color="#282c34")
		self.View_frame.pack(side="top", fill="both", expand=True)

		self.View = RoiSetList(master=self.View_frame)
		self.View.pack(side="top", fill="both", expand=True)
  
	

if __name__ == "__main__":
	freeze_support()
	app = App()
	app.mainloop()