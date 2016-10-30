import requests
from requests.auth import HTTPBasicAuth

res = requests.get('https://gateway.watsonplatform.net/conversation/api', auth=HTTPBasicAuth('1dbb9468-81e2-4175-b398-475d6e90343b', '1p7sZwgO8qNo'))

print res.headers
body={
 "input": {
    "text": "hi"
  }
}

res1 = requests.post('https://gateway.watsonplatform.net/conversation/api', body)

print res1
