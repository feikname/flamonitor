import socket
import cpuinfo
import psutil
from utilities import format_bytes, get_formatted_localtime

def get_disk_usage():
  import os
  import win32api
  drive = os.path.splitdrive('C:\\')[0]
  _, total_space, free_space = win32api.GetDiskFreeSpaceEx(drive)
  used_space = total_space - free_space
  used_space = format_bytes(used_space)
  total_space = format_bytes(total_space)
  free_space = format_bytes(free_space)
  return {
    "total_space": total_space,
    "free_space": free_space,
    "used_space": used_space
  }

def get_users():
  import wmi
  lista = []
  c = wmi.WMI()
  for user in c.Win32_ComputerSystem():
    lista.append(user.UserName)
  return lista

def get_computer_info():
  cpu_model = cpuinfo.get_cpu_info()['brand_raw']
  total_memory = psutil.virtual_memory().total  / (1024 ** 3)
  total_memory = "{:.2f} GiB".format(total_memory)
  hostname = socket.gethostname()
  local_ip = socket.gethostbyname(hostname)
  disk_usage = get_disk_usage()
  _time = get_formatted_localtime()

  return {
    "total_memory": total_memory,
    "cpu_model": cpu_model,
    "hostname": hostname,
    "local_ip": local_ip,
    "disk_usage": disk_usage,
    "users": get_users(),
    "local_time": _time
  }
