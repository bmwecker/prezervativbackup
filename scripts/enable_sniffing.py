import requests
import json
import urllib3

urllib3.disable_warnings()

URL = "https://45.148.118.5:31208/V0dEU3CRUVn1z3MgHn"
session = requests.Session()

# Login
login = session.post(f"{URL}/login", data={"username": "iYdrvxh6Mg", "password": "mjK6Afc7yi"}, verify=False)
if not login.json().get("success"):
    print("Login failed")
    exit(1)

# Get Inbounds
res = session.post(f"{URL}/panel/inbound/list", verify=False)
inbounds = res.json()["obj"]

for inbound in inbounds:
    # enable sniffing
    sniffing = inbound.get('sniffing')
    streamSettings = None
    try:
        settings_str = inbound.get('settings')
        stream_str = inbound.get('streamSettings')
        sniffing_str = inbound.get('sniffing')
        
        sniff_obj = json.loads(sniffing_str) if sniffing_str else {}
        sniff_obj["enabled"] = True
        sniff_obj["destOverride"] = ["http", "tls", "quic"]
        
        # update the inbound
        inbound['sniffing'] = json.dumps(sniff_obj)
        
        # send update
        update_res = session.post(f"{URL}/panel/inbound/update/{inbound['id']}", data=inbound, verify=False)
        print(f"Updated inbound {inbound['remark']}: {update_res.json()}")
    except Exception as e:
        print(f"Failed to update inbound {inbound.get('remark')}: {e}")

# Restart Xray
res_xray = session.post(f"{URL}/panel/setting/restart", verify=False)
print("Restarting Xray...", res_xray.json())
