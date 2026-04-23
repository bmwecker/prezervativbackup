import urllib.request
import json
import datetime
import random
import base64
import time

def generate_warp_config():
    # Generate keys
    try:
        import cryptography.hazmat.primitives.asymmetric.x25519 as x25519
        from cryptography.hazmat.primitives import serialization
        priv = x25519.X25519PrivateKey.generate()
        pub = priv.public_key()
        priv_bytes = priv.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        pub_bytes = pub.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        priv_b64 = base64.b64encode(priv_bytes).decode('utf-8')
        pub_b64 = base64.b64encode(pub_bytes).decode('utf-8')
    except ImportError:
        return "Install cryptography module: pip install cryptography"

    # Register
    install_id = "".join(random.choices("0123456789abcdef", k=22))
    body = {
        "key": pub_b64,
        "install_id": install_id,
        "fcm_token": install_id + ":APA91b" + "".join(random.choices("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=134)),
        "tos": datetime.datetime.now().isoformat() + "+02:00",
        "model": "PC",
        "locale": "en_US"
    }

    req = urllib.request.Request(
        "https://api.cloudflareclient.com/v0a2158/reg",
        data=json.dumps(body).encode('utf-8'),
        headers={
            "User-Agent": "okhttp/3.12.1",
            "Content-Type": "application/json",
            "CF-Client-Version": "a-6.10-2158"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            account_type = res.get("account_type", "free")
            config = res.get("config", {})
            peers = config.get("peers", [{}])
            peer = peers[0]
            
            client_v4 = config.get("interface", {}).get("addresses", {}).get("v4", "")
            client_v6 = config.get("interface", {}).get("addresses", {}).get("v6", "")
            
            print("WARP WireGuard Configuration:")
            print("-----------------------------")
            print(f"[Interface]")
            print(f"PrivateKey = {priv_b64}")
            print(f"Address = {client_v4}/32, {client_v6}/128")
            print("DNS = 1.1.1.1")
            print("MTU = 1280")
            print(f"\n[Peer]")
            print(f"PublicKey = {peer.get('public_key', '')}")
            print(f"Endpoint = {peer.get('endpoint', {}).get('host','')}")
            print("AllowedIPs = 0.0.0.0/0, ::/0")
            print("-----------------------------")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    generate_warp_config()
