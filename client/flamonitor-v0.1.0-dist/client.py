import requests

from utilities import read_config, mysalt
from winutil import get_computer_info

clientVersion = "0.1.0"

config = read_config("clientsettings.json")
serverAddr = config['serverAddresses'][0]

automated_info=  get_computer_info()
handwritten_info = config['handwrittenInfo']

handwritten_info['salt'] = mysalt()

merged_info = {
  "clientVersion": clientVersion,
  "handwrittenInfo": handwritten_info,
  "automatedInfo": automated_info
}



print(merged_info)

requests.post(serverAddr, json=merged_info, headers={"Content-Type": "application/json"})
