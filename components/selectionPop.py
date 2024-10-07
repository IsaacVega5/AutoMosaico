import customtkinter as ctk
from PIL import Image
from constants import IMG_TYPES

class SelectionPop(ctk.CTkFrame):
  def __init__(self,master, title, text, alternatives, subtitle=None, checkVars=None, *args, **kwargs):
    """
    Creates a pop up window with a title, text, and options to respond with.
    
    Parameters
    ----------
    master : CTkWidget
      The widget that will be the parent of this popup window.
    
    title : str
      The title of the popup window.
    
    text : str or list
      The text to display in the popup window. If a list is given, it will be rendered as multiple lines.
    
    alternatives : list
      A list of strings that will be rendered as buttons to select from.
    
    subtitle : str
      A subtitle to display below the title.
    
    checkVars : dict
      A dictionary where the keys are the text to display next to a checkbox and the value is the initial state of the checkbox.
    
    *args, **kwargs : arguments
      Any additional arguments that will be passed to the CTkFrame constructor.
    
    Returns
    -------
    None
    
    Notes
    -----
    This function will block until the user selects an option and closes the window.
    The selected option can be accessed with the `get` function of the returned object.
    """
    super().__init__(master, *args, **kwargs)
    self.configure(corner_radius =0, fg_color="#282c34", bg_color="#282c34")
    self.place(relx=0.5, rely=0.5, anchor="center")
    
    self.subtitle = subtitle
    self.text = text
    self.alternatives = alternatives
    self.response = alternatives[0]
    self.continue_action = True
    
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
    
    if checkVars != None:

      self.checks = []
      for index, key in enumerate(checkVars.keys()):
        self.var = ctk.BooleanVar(master=self, value=checkVars[key])
        self.element = ctk.CTkCheckBox(self, text=key, variable=self.var, onvalue=True, offvalue=False, height=5, checkbox_height=16, checkbox_width=16, corner_radius= 0)
        self.element.pack(side="top", fill="x", padx=10, pady=(0,10))
        self.checks.append({
          "key": index,
          "element": self.element,
          "var": self.var
        })
    
    
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
    """
    Gets the response from the popup window. If the popup window had checkboxes, the response will include a "checks" key with a list of boolean values corresponding to the state of each checkbox. If the popup window did not have checkboxes, the response will only have an "alternatives" key with the selected option from the popup window.
    
    Returns
    -------
    dict
      A dictionary with the response from the popup window.
    """
    if not self.continue_action: return False
    res = self.response
    res = {
      "alternatives": self.response
    }
    checks = []
    if hasattr(self, "checks"):
      for check in self.checks:
        if check["var"].get():
          checks.append(True)
        else:
          checks.append(False)
      res['checks'] = checks
    return res
  
  def accept(self):
    if isinstance(self.text, list):
      self.response = [ entry.get() for entry in self.alternatives_entries ]
    else:
      self.response = self.alternatives_entry.get()
    
    self.place_forget()
    self.destroy()
  
  def cancel(self):
    self.continue_action = False
    self.place_forget()
    self.destroy()

