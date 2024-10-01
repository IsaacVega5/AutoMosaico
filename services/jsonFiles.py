import json
from constants import ROI_SET_PATH

def save_to_json(path, data):
  json_array = read_json_file(path)
  
  json_array.append(data)

  json_object = json.dumps(json_array, indent=4)

  with open(path, "w") as outfile:
      outfile.write(json_object)
      
      
def read_json_file(path):
  try:
    with open(path) as json_file:
      data = json.load(json_file)
    return data
  except:
    create_json_file(path)
    return read_json_file(path)

def create_json_file(path):
  data = []
  json_object = json.dumps(data, indent=4)
  with open(path, "w") as outfile:
      outfile.write(json_object)
      
def get_by_id(path, id):
  json_array = read_json_file(path)
  for item in json_array:
    if item["id"] == id:
      return item
  return False

def edit_by_id(path, id, data):
  json_array = read_json_file(path)
  
  for item in json_array:
    if item["id"] == id:
      item.update(data)
  
  json_object = json.dumps(json_array, indent=4)
  with open(path, "w") as outfile:
    outfile.write(json_object)

