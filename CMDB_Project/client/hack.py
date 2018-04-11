__author__ = 'Administrator'

import requests

response = requests.get(url='http://127.0.0.1:8000/api/asset.html',
                        headers={"OpenKey": "37bb63b2490c2c1a9f66314da913176c|1523464502.0716207"})
print(response.text)
