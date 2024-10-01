import json
from datetime import datetime
from services.jsonFiles import read_json_file, get_by_id
from constants import ROI_SET_PATH
import os

def get_all(name=None, order=None):
  result = read_json_file(ROI_SET_PATH)
  
  for item in result:
    item['updated_at'] = datetime.strptime(item['updated_at'], '%d/%m/%Y %H:%M:%S')
  
  if name == "created_at": result.sort(key=lambda x: x['created_at'])
  if name == "updated_at": result.sort(key=lambda x: x['updated_at'])
  if name == "name": result.sort(key=lambda x: x['name'])
  
  if order == "desc": result.reverse()
  return result

def get_by_id(id):
  data =  read_json_file(ROI_SET_PATH)
  for item in data:
    if item["id"] == id:
      return item
  return False

def delete_by_id(id):
  json_array = read_json_file(ROI_SET_PATH)
  
  for item in json_array:
    if item["id"] == id:
      json_array.remove(item)
  
  json_object = json.dumps(json_array, indent=4)
  with open(ROI_SET_PATH, "w") as outfile:
    outfile.write(json_object)

def edit_by_id(id, data):
  json_array = read_json_file(ROI_SET_PATH)
  
  for item in json_array:
    if item["id"] == id:
      item.update(data)
  
  json_object = json.dumps(json_array, indent=4)
  with open(ROI_SET_PATH, "w") as outfile:
    outfile.write(json_object)


def check_images(json_path=ROI_SET_PATH):
  json_array = read_json_file(json_path)
  
  for item in json_array:
    if not os.path.exists(item['image_path']) or not os.path.exists(item['roi_path']):
      json_array.remove(item)
  
  json_object = json.dumps(json_array, indent=4)
  with open(json_path, "w") as outfile:
    outfile.write(json_object)
