from datetime import datetime
from utils import get_name_full_from_path
def save_error(img_list, roi_path, roi_img, error = None):
  f = open('error_logs.md', 'a')
  
  f.write('<details>\n')
  f.write(f'<summary><strong>{datetime.now()}</strong></summary> \n\n')
  
  f.write('### Detalles\n\n')
  f.write(f'**ROI:** {roi_path}\n\n')
  f.write(f'**Imagen ROI:** {roi_img}\n\n')
  
  f.write('| Imagen | Tipo |\n')
  f.write('| --- | --- |\n')
  for item in img_list:
    type = item['type']
    name = get_name_full_from_path(item['path'])
    f.write(f'| {name} | {type} |\n')
  
  if error is not None:
    f.write('### Error\n\n')
    f.write("```PowerShell\n\n")
    f.write(f'{error}\n')
    f.write("```\n")
    f.write('</details>\n')
  
  