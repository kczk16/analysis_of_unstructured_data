import requests
from time import sleep

data = {}
response = requests.get('https://fcd.terra.dev/v1/txs?offset=0&limit=100&account=terra1jdt2wnfhgy4ptk6m5kxacyj0k6e8rc7e2ugulz')
next = eval(response.content)['next']

data[0] = str(response.content)
i = 1
while next:
    url = 'https://fcd.terra.dev/v1/txs?offset={}&limit=100&account=terra1jdt2wnfhgy4ptk6m' \
          '5kxacyj0k6e8rc7e2ugulz'.format(next)
    response = requests.get(url)
    try:
        data[i] = str(response.content)
        next = eval(response.content)['next']
        i += 1
    except NameError:
        next = 0
        pass
    sleep(1)

with open('data.txt', 'w') as f:
    f.write(str(data))
