> [!WARNING]  
> This repository is now archived as I now use [Nginx Proxy Manager](https://nginxproxymanager.com/) for my homelab.

# DomainDispatcher

Web server redirecting traffic based server name

## Installation

Pull the docker image

```bash
docker pull ghcr.io/richarddorian/domaindispatcher:latest
```

Create the container, I recommend binding the container to the host network directly. The container should stop as there's no configuration file yet.

```bash
docker run -p 80:80 -p 443:443 -v /path/to/folder/on/host:/domaindispatcher --network host --name mycontainername ghcr.io/richarddorian/domaindispatcher
```

## Configuration

In `/path/to/folder/on/host` create (or copy from the following example) a file that will contain the config. The file name should be `config.json`.

```json
[
  {
    "serverName": "jellyfin.example.com",
    "target": "http://127.0.0.1:8096",
    "ssl": {
      "cert": "jellyfin.example.com.crt",
      "key": "jellyfin.example.com.key"
    }
  },
  {
    "serverName": "openspeedtest.example.com",
    "target": "http://127.0.0.1:8080",
    "ssl": {
      "cert": "openspeedtest.example.com.crt",
      "key": "openspeedtest.example.com.key"
    }
  }
]
```

The values for the `cert` and `key` attributes are relative to `/path/to/folder/on/host/certificates`. If you ommit the `ssl` object, the server will be listening on por `80` (only using the HTTP protocol). If it is present, the server will be listening on port `443` (only using the HTTPS protocol).
