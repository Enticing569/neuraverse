import base64
import time

import requests

key = ""
url = "https://client-api.arkoselabs.com/rtig/image?challenge=0&expires=1760445156&gameToken=172186e584460cde5.5083152705&sessionToken=138186e58442b2434.8747082305&signature=ed84bkgR7nBQTCejSflYg85lYkesnv5YJcVhkDDdyuw1munJvroq9Myo0vzbkrZIHxvt2TtVAoyt6AQAHq%2Fty%2FrVOLNGGntBMVEBk%2FErxCqawBbJxiUBQPgTcxCq0zeKYknYuLbAr1TDzwVjGNUAM6aI34D0l73BCldHTWS7Epp%2FtakgtESMhmnzi0Cpox4h6QFr7JTyqqcjMANpPH7g4QerKrfm1SQTG35FWQSTMcEZrg4aTzbHjYrN3ga6k5bE93t9wPOlIEimOlFUSIXteHCqiEXjVj4dWdqvFJRw5mprIow%2F73N6RvtUo%2B67h6AVa3bCawvAhxHpWr7rANDBBA%3D%3D"
response = requests.get(url)

ee = base64.b64encode((response.content))

payload = {
    "textinstructions": "Using the arrows, connect the same two icons with the dotted line as shown on the left",
    "click": "funcap2",
    "key": key,
    "method": "base64",
    "body": ee,
}
r = requests.post("http://api.cap.guru/in.php", data=payload)

time.sleep(10)

rt = r.text.split("|")
url = "http://api.cap.guru/res.php?key=" + key + "&id=" + rt[1]
print(url)
response = requests.get(url)


print(response.content)

time.sleep(1000)
