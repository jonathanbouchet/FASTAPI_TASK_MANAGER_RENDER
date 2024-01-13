import requests
url_public = "http://127.0.0.1:8000/items"
url_private = "http://127.0.0.1:8000/items/private"

headers1 = {"Content-Type": "application/json", "Accept":"application/json"}
headers2 = headers1.copy()
headers2.update({"X-Api-Key": "<x-api-key>"})

# testing the public route
requests.get(url = url_public, headers=headers1) # <Response [200]>
requests.get(url = url_public, headers=headers1).json() # [{'id': 1, 'name': 'item 1', 'description': 'some stuff'}]

# testing the private route
requests.get(url = url_private, headers=headers1).json() # {'detail': 'Not authenticated'}
requests.get(url = url_private, headers=headers2).json()# [{'id': 1, 'name': 'item 1', 'description': 'some stuff'}]