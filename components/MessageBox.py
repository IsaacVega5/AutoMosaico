from CTkMessagebox import CTkMessagebox

def warning(*args, **kwargs):
  icon = 'assets/icons/warning.png'
  return CTkMessagebox(icon=icon, *args, **kwargs)

def error(*args, **kwargs):
  icon = 'assets/icons/error.png'
  return CTkMessagebox(icon=icon, *args, **kwargs)

def info(*args, **kwargs):
  icon = 'assets/icons/info.png'
  return CTkMessagebox(icon=icon, *args, **kwargs)

def check(*args, **kwargs):
  icon = 'assets/icons/check.png'
  return CTkMessagebox(icon=icon, *args, **kwargs)