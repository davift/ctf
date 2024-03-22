#!/usr/bin/python3

import requests

host, port = '127.0.0.1', 8080
HOST = 'http://%s:%s/' % (host, port)
#HOST = 'https://webhook.site/000000000000000000000'

# GET Empty + Auth + Redirect
r = requests.get(HOST, auth=('user', 'pass'), allow_redirects=False)

# GET Empty + Cert + Cookie
r = requests.get(HOST, cert='client.cert', cookies={"role": "admin"})

# GET Empty + Header + Timeout
r = requests.get(HOST, headers={"Host": "example.com"}, timeout=0.500)

# GET Parameter
r = requests.get(HOST, params={ 'parameter': "value" })

# POST Data
r = requests.post(HOST, data="any data can be placed here")

# POST Upload File
object = { 'file': open('flag.txt' ,'rb') }
r = requests.post(HOST, files=object)

# POST JSON
object = { 'parameter1': "value1", 'parameter2': "value2" }
r = requests.post(HOST, json=object)

# Print Response
print(r.text)

exit()
