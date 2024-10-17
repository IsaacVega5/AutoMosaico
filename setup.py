from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': [], 'include_files':['assets/']}

base = 'gui'

executables = [
    Executable(
        'main.py', 
        base=base,
        icon='assets/map.ico',
        target_name = 'AutoMosaico')
]

setup(name='AutoMosaico',
      version = '0.3.2',
      author='Isaac vega Salgado',
      author_email='isaacvega361@gmail.com',
      description = 'AutoMosaico',
      options = {'build_exe': build_options},
      executables = executables)
