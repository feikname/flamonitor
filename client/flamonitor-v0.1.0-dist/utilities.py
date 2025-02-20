from typing import Union

def format_bytes(bytes):
  for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
    if bytes < 1024.0:
      break
    bytes /= 1024.0
  return f"{bytes:.2f} {unit}"

def get_formatted_localtime() -> str:
  import time
  struct_time_obj = time.localtime()
  return time.strftime("%Y-%m-%d %H:%M:%S", struct_time_obj)

def read_config(file_path: str) -> dict:
  file = open(file_path, "r")
  file_raw = file.read()

  import json
  data = json.loads(file_raw)

  return data

def prettify_data_to_json(data: Union[dict, list]) -> str:
  import json
  return json.dumps(data, indent=2, sort_keys=True)

def generate_random_hex(length=5):
  import uuid
  uuid4 = str(uuid.uuid4())[25:30]
  return uuid4

def is_file(filepath):
  import os
  try:
    if os.path.exists(filepath):
      print('ja tem salt!')
      return True
    return False
  except Exception as e:
    print(f"An error occurred: {e}")
    return False
    
def mysalt():
  import json
  file = None
  if(not is_file("salt.json")):
    file = open('salt.json', 'x')
    salt_json = { "salt": generate_random_hex() }
    salt_json = json.dumps(salt_json)
    file.write(salt_json)
    file.close()
  
  file = open('salt.json', 'r')
  conteudo = file.read()
  conteudo = json.loads(conteudo)
  return conteudo['salt']
