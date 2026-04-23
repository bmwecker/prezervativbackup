import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://45.148.118.5:31208/V0dEU3CRUVn1z3MgHn"
USERNAME = "iYdrvxh6Mg"
PASSWORD = "mjK6Afc7yi"

session = requests.Session()

# Login
login_data = {
    "username": USERNAME,
    "password": PASSWORD
}
res = session.post(f"{URL}/login", data=login_data, verify=False)
if not res.json().get("success"):
    print("Login failed!")
    exit(1)

print("Logged in!")

# Get settings
res = session.post(f"{URL}/panel/setting/getDefaultJsonConfig", verify=False) # this fails sometimes
res = session.get(f"{URL}/panel/setting/all", verify=False)
if not res.json().get("success"):
    print("Failed to get settings!")
    exit(1)

settings = res.json()["obj"]
xray_config_str = settings["xrayTemplateConfig"]
xray_config = json.loads(xray_config_str)

# Add WARP to outbounds
warp_outbound = {
  "tag": "warp",
  "protocol": "wireguard",
  "settings": {
    "secretKey": "IE/8NZcrUo3laHNw7HyCJYscTtGSbptfbr0DxYDrznQ=",
    "address": [
      "172.16.0.2/32",
      "2606:4700:110:88a4:b86d:c587:db53:4112/128"
    ],
    "peers": [
      {
        "publicKey": "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=",
        "endpoint": "engage.cloudflareclient.com:2408"
      }
    ],
    "mtu": 1280
  }
}

# Only add if not present
if not any(ob.get("tag") == "warp" for ob in xray_config["outbounds"]):
    xray_config["outbounds"].insert(1, warp_outbound)

warp_routing = {
  "type": "field",
  "outboundTag": "warp",
  "domain": [
    "geosite:google",
    "domain:notebooklm.google",
    "domain:google.com",
    "geosite:openai",
    "geosite:anthropic",
    "geosite:netflix",
    "domain:claude.ai",
    "domain:withgoogle.com",
    "domain:huggingface.co"
  ]
}

# Only add if not present
if not any(r.get("outboundTag") == "warp" for r in xray_config["routing"]["rules"]):
    xray_config["routing"]["rules"].insert(1, warp_routing)

new_xray_config_str = json.dumps(xray_config, indent=2)

# Save settings
settings["xrayTemplateConfig"] = new_xray_config_str
res = session.post(f"{URL}/panel/setting/update", data=settings, verify=False)

if res.json().get("success"):
    print("Settings updated successfully!")
    # Restart Xray
    res = session.post(f"{URL}/panel/setting/restartPanel", verify=False) # Wait, it's /panel/setting/restart Panel or just xray restart?
    res_xray = session.post(f"{URL}/panel/setting/restart", verify=False) # restart XRAY 
    print("Restart Xray Response:", res_xray.json())
else:
    print("Failed to update settings:", res.text)
