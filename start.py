from os import path, environ, path
from json import load
from subprocess import run

BASE_PATH = environ.get("DP_BASE_PATH")
if not BASE_PATH: BASE_PATH = "/domaindispatcher"
USING_CLOUDFLARE = environ.get("DP_USING_CLOUDFLARE") == "true"
NGINX_CONFIG_PATH = environ.get('DP_NGINX_CONFIG')
if not NGINX_CONFIG_PATH: NGINX_CONFIG_PATH = "/etc/nginx/conf.d/domaindispatcher.conf"

config_path = path.join(BASE_PATH, "config.json")
certificates_dir_path = path.join(BASE_PATH, "certificates")

if not path.exists(config_path):
  print("Config file not found at " + config_path)
  exit(1)

with open(config_path) as config_file:
  config = load(config_file)

nginx_server = ""

def append(text, tab = 0):
  global nginx_server
  nginx_server += ("  "*tab + text + "\n")

xRealIp = "http_cf_connecting_ip" if USING_CLOUDFLARE else "remote_addr"
xForwardedFor = "http_cf_connecting_ip" if USING_CLOUDFLARE else "proxy_add_x_forwarded_for"

for domain in config:
  append("server {")
  
  append("server_name " + domain["serverName"] + ";", 1)

  if "ssl" in domain:
    append("listen 443 ssl;", 1)
    append("ssl_certificate " + path.join(certificates_dir_path, domain["ssl"]["cert"]) + ";", 1)
    append("ssl_certificate_key " + path.join(certificates_dir_path, domain["ssl"]["key"]) + ";", 1)
  else:
    append("listen 80;", 1)

  append("location / {", 1)
  append("proxy_pass " + domain["target"] + "$request_uri;", 2)
  append("proxy_redirect " + domain["target"] + " /;", 2)
  append("proxy_set_header Host $host;", 2)
  append(f"proxy_set_header X-Real-IP ${xRealIp};", 2)
  append(f"proxy_set_header X-Forwarded-For ${xForwardedFor};", 2)
  append("proxy_set_header X-Forwarded-Proto $scheme;", 2)

  append("}", 1)

  append("}")

with open(NGINX_CONFIG_PATH, "w+") as file:
  file.write(nginx_server)

print("Nginx server config generated at " + NGINX_CONFIG_PATH)
print("Starting nginx daemon...")

run(["nginx", "-g", "daemon off;"])