from os import path
from json import load
from subprocess import run

config_path = "/domaindispatcher/config.json"
certificates_dir_path = "/domaindispatcher/certificates"
nginx_server_config_path = "/etc/nginx/conf.d/domaindispatcher.conf"

if not path.exists(config_path):
  print("Config file not found at " + config_path)
  exit(1)

with open(config_path) as config_file:
  config = load(config_file)

nginx_server = ""

def append(text, tab = 0):
  global nginx_server
  nginx_server += ("  "*tab + text + "\n")

for domain in config:
  append("server {")
  
  append("server_name " + domain["serverName"] + ";", 1)

  if "ssl" in domain:
    append("listen 443 ssl;", 1)
    append("ssl_certificate " + path.join(certificates_dir_path, domain["ssl"]["cert"]) + ";", 1)
    append("ssl_certificate_key " + path.join(certificates_dir_path, domain["ssl"]["key"]) + ";", 1)

  append("location / {", 1)
  append("proxy_pass " + domain["target"] + ";", 2)
  append("proxy_redirect default;", 2)
  append("}", 1)

  append("}")

with open(nginx_server_config_path, "w+") as file:
  file.write(nginx_server)

print("Nginx server config generated at " + nginx_server_config_path)
print("Starting nginx daemon...")

run(["nginx", "-g", "daemon off;"])