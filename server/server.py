import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from utilities import get_formatted_localtime, read_config, prettify_data_to_json
import sqlite3

db = sqlite3.connect("computers.db")
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS computers_v1 (
        computer_name_on_sticker TEXT,
        salt TEXT,
        location_room TEXT,
        location_additional_info TEXT,
        machine_type TEXT,
        network_connected_to TEXT,
        received_from_ip TEXT,
        received_at TEXT,
        cpu_model TEXT,
        disk_usage_free TEXT,
        disk_usage_total TEXT,
        disk_usage_used TEXT,
        windows_hostname TEXT,
        windows_local_ip TEXT,
        windows_local_time TEXT,
        computer_memory TEXT,
        windows_users_json TEXT,
        flamonitor_version TEXT,
        PRIMARY KEY (computer_name_on_sticker, salt) 
    );
''')

read_config("serversettings.json")

# key is handwrittenInfo.computerNameOnSticker+' '+salt
computers = {}

def update_computer_data(key, data):
  insert_data = [(
    {
      "computer_name_on_sticker": data['handwrittenInfo']['computerNameOnSticker'],
      "salt": data['handwrittenInfo']['salt'],
      "location_room": data['handwrittenInfo']['location']['room'],
      "location_additional_info": data['handwrittenInfo']['location']['additionalInfo'],
      "machine_type": data['handwrittenInfo']['machineType'],
      "network_connected_to": data['handwrittenInfo']['networkConnectedTo'],
      "received_from_ip": data['metadata']['received_from_ip'],
      "received_at": data['metadata']['updated_at'],
      "cpu_model": data['automatedInfo']['cpu_model'],
      "disk_usage_free": data['automatedInfo']['disk_usage']['free_space'],
      "disk_usage_total": data['automatedInfo']['disk_usage']['total_space'],
      "disk_usage_used": data['automatedInfo']['disk_usage']['used_space'],
      "windows_hostname": data['automatedInfo']['hostname'],
      "windows_local_ip": data['automatedInfo']['local_ip'],
      "windows_local_time": data['automatedInfo']['local_time'],
      "computer_memory": data['automatedInfo']['total_memory'],
      "windows_users_json": json.dumps(data['automatedInfo']['users']),
      "flamonitor_version": "0.1.0 probably"
    }
  )]

  insert_query = """
    INSERT INTO computers_v1 VALUES(
      :computer_name_on_sticker, 
      :salt,
      :location_room,
      :location_additional_info,
      :machine_type,
      :network_connected_to,
      :received_from_ip,
      :received_at,
      :cpu_model,
      :disk_usage_free,
      :disk_usage_total,
      :disk_usage_used,
      :windows_hostname,
      :windows_local_ip,
      :windows_local_time,
      :computer_memory,
      :windows_users_json,
      :flamonitor_version
    )
    ON CONFLICT (computer_name_on_sticker, salt) DO UPDATE SET
      location_room = EXCLUDED.location_room,
      location_additional_info = EXCLUDED.location_additional_info,
      machine_type = EXCLUDED.machine_type,
      network_connected_to = EXCLUDED.network_connected_to,
      received_from_ip = EXCLUDED.received_from_ip,
      received_at = EXCLUDED.received_at,
      cpu_model = EXCLUDED.cpu_model,
      disk_usage_free = EXCLUDED.disk_usage_free,
      disk_usage_total = EXCLUDED.disk_usage_total,
      disk_usage_used = EXCLUDED.disk_usage_used,
      windows_hostname = EXCLUDED.windows_hostname,
      windows_local_ip = EXCLUDED.windows_local_ip,
      windows_local_time = EXCLUDED.windows_local_time,
      computer_memory = EXCLUDED.computer_memory,
      windows_users_json = EXCLUDED.windows_users_json,
      flamonitor_version = EXCLUDED.flamonitor_version
    ;
"""
  cursor.executemany(insert_query, insert_data)
  db.commit()

  print(key, 'was updated with', prettify_data_to_json(insert_data))

  # with open('computers.json', "w") as file:
  #   file.write(prettify_data_to_json(computers))

class MyHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    content_length = int(self.headers['Content-Length'])  # Get the size of data
    post_data = self.rfile.read(content_length)  # Read the data

    try:
      # Attempt to parse JSON data
      data = json.loads(post_data.decode('utf-8'))

      metadata = {
        'received_from_ip': self.client_address[0],
        'updated_at': get_formatted_localtime()
      }
      data['metadata'] = metadata

      key = data['handwrittenInfo']['computerNameOnSticker']
      key += ' '
      key +=data['handwrittenInfo']['salt']

      update_computer_data(key, data)

      # Respond with a success message (200 OK) and the received data
      self.send_response(200)
      self.send_header('Content-type', 'application/json') # Indicate JSON response
      self.end_headers()
      response_message = json.dumps({"message": "POST request received and processed", "data": data}) #include data in response
      self.wfile.write(response_message.encode('utf-8'))

    except Exception as e: # Catch any other error
      self.send_response(500)  # Internal Server Error
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      error_message = json.dumps({"error": str(e)}) # Return error details
      self.wfile.write(error_message.encode('utf-8'))
      print(f"An error occurred: {e}")


def run(server_class=HTTPServer, handler_class=MyHandler, port=8000):
  server_address = ('', port)  # Listen on all available interfaces
  httpd = server_class(server_address, handler_class)
  print(f'Starting http server on port {port}...')
  httpd.serve_forever()

if __name__ == '__main__':
  run()
