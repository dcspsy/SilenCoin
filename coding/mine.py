import requests
s = requests.session()

while True:
    s.get('http://0.0.0.0:5000/mine')



